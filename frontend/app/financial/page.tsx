// app/financial/page.tsx - Financial Dashboard
"use client"

import { useEffect, useState, useCallback } from "react"
import { apiClient, type FinancialDashboard, type Transaction } from "@/lib/api-client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function FinancialPage() {
  const [dashboard, setDashboard] = useState<FinancialDashboard | null>(null)
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [refreshing, setRefreshing] = useState(false)

  const fetchData = useCallback(async () => {
    setRefreshing(true)
    console.log('[Financial] Fetching data...')
    
    const [dashboardRes, transactionsRes] = await Promise.all([
      apiClient.get<FinancialDashboard>("/api/v1/financial/dashboard"),
      apiClient.get<Transaction[]>("/api/v1/financial/transactions?limit=50"),
    ])
    
    console.log('[Financial] Dashboard response:', dashboardRes)
    console.log('[Financial] Transactions response:', transactionsRes)
    
    if (dashboardRes.error) console.error('[Financial] Dashboard error:', dashboardRes.error)
    if (transactionsRes.error) console.error('[Financial] Transactions error:', transactionsRes.error)
    
    if (dashboardRes.data) setDashboard(dashboardRes.data)
    if (transactionsRes.data) setTransactions(Array.isArray(transactionsRes.data) ? transactionsRes.data : [])
    setLastUpdated(new Date())
    setLoading(false)
    setRefreshing(false)
  }, [])

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [fetchData])

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">💰 Financial Dashboard</h1>
        <div className="flex items-center gap-4">
          {lastUpdated && (
            <span className="text-sm text-gray-500">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </span>
          )}
          <Button 
            onClick={fetchData} 
            disabled={refreshing}
            variant="outline"
            size="sm"
          >
            {refreshing ? "🔄 Refreshing..." : "🔄 Refresh"}
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Total Revenue
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${dashboard?.total_revenue.toLocaleString() || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Total Expenses
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${dashboard?.total_expenses.toLocaleString() || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Net Profit
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${dashboard?.net_profit.toLocaleString() || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Transactions
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dashboard?.transaction_count || 0}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Revenue by Entity */}
      {dashboard?.revenue_by_entity && Object.keys(dashboard.revenue_by_entity).length > 0 && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>📈 Revenue by Entity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {Object.entries(dashboard.revenue_by_entity).map(([entity, amount]) => (
                <div key={entity} className="flex justify-between">
                  <span>{entity}</span>
                  <span className="font-semibold">${amount.toLocaleString()}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Expenses by Category */}
      {dashboard?.expense_by_category && Object.keys(dashboard.expense_by_category).length > 0 && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>💸 Expenses by Category</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {Object.entries(dashboard.expense_by_category).map(([category, amount]) => (
                <div key={category} className="flex justify-between">
                  <span>{category}</span>
                  <span className="font-semibold">${amount.toLocaleString()}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Recent Transactions */}
      <Card>
        <CardHeader>
          <CardTitle>📋 Recent Transactions</CardTitle>
        </CardHeader>
        <CardContent>
          {transactions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="px-4 py-2 text-left">Date</th>
                    <th className="px-4 py-2 text-left">Type</th>
                    <th className="px-4 py-2 text-left">Amount</th>
                    <th className="px-4 py-2 text-left">Category</th>
                    <th className="px-4 py-2 text-left">Description</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.map((transaction) => (
                    <tr key={transaction.id} className="border-b">
                      <td className="px-4 py-2">
                        {new Date(transaction.date).toLocaleDateString()}
                      </td>
                      <td className="px-4 py-2">
                        <span className={`rounded px-2 py-1 text-xs ${
                          transaction.type === 'revenue' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {transaction.type}
                        </span>
                      </td>
                      <td className="px-4 py-2 font-semibold">
                        ${transaction.amount.toLocaleString()}
                      </td>
                      <td className="px-4 py-2">{transaction.category || 'N/A'}</td>
                      <td className="px-4 py-2">{transaction.description || 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-500">No transactions found</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

