// app/page.tsx - Overview Dashboard
"use client"

import { useEffect, useState, useCallback } from "react"
import { apiClient, type DailyBriefing, type FinancialDashboard } from "@/lib/api-client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function OverviewPage() {
  const [briefing, setBriefing] = useState<DailyBriefing | null>(null)
  const [financial, setFinancial] = useState<FinancialDashboard | null>(null)
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [refreshing, setRefreshing] = useState(false)

  const fetchData = useCallback(async () => {
    setRefreshing(true)
    console.log('[Overview] Fetching data...')
    
    const [briefingRes, financialRes] = await Promise.all([
      apiClient.get<DailyBriefing>("/api/v1/daily-briefing"),
      apiClient.get<FinancialDashboard>("/api/v1/financial/dashboard"),
    ])
    
    console.log('[Overview] Briefing response:', briefingRes)
    console.log('[Overview] Financial response:', financialRes)
    
    if (briefingRes.error) {
      console.error('[Overview] Briefing error:', briefingRes.error)
    }
    if (financialRes.error) {
      console.error('[Overview] Financial error:', financialRes.error)
    }
    
    if (briefingRes.data) setBriefing(briefingRes.data)
    if (financialRes.data) setFinancial(financialRes.data)
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

  // Show error if API failed
  const hasError = !briefing && !financial

  const goal = 10000000
  const revenue = financial?.total_revenue || 0
  const progress = Math.min((revenue / goal) * 100, 100)

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">📊 Dashboard Overview</h1>
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
      
      {hasError && (
        <div className="mb-4 rounded-lg bg-yellow-50 border border-yellow-200 p-4">
          <p className="text-yellow-800">
            ⚠️ Unable to connect to API. Please ensure the backend is running on http://localhost:8000
          </p>
          <p className="text-sm text-yellow-600 mt-2">
            Check browser console (F12) for detailed error messages.
          </p>
        </div>
      )}

      {/* Key Metrics */}
      <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Day of 90-Day Plan
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              Day {briefing?.day_number || 1}
            </div>
            <p className="text-sm text-gray-500">
              {90 - (briefing?.day_number || 1)} days remaining
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Revenue YTD
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${revenue.toLocaleString()}
            </div>
            <p className="text-sm text-gray-500">
              {typeof progress === 'number' ? progress.toFixed(1) : '0.0'}% to $10M goal
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Active Projects
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {briefing?.metrics.active_projects || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Active Leads
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {briefing?.metrics.active_leads || 0}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Progress Bar */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>🎯 Progress Toward $10M Goal</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="mb-2 flex justify-between text-sm">
            <span>Current: ${revenue.toLocaleString()}</span>
            <span>Goal: ${goal.toLocaleString()}</span>
          </div>
          <div className="h-4 w-full overflow-hidden rounded-full bg-gray-200">
            <div
              className="h-full bg-blue-600 transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </CardContent>
      </Card>

      {/* Today's Tasks */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>📋 Today's Tasks</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div>
              <div className="text-2xl font-bold">{briefing?.total_tasks || 0}</div>
              <div className="text-sm text-gray-500">Total Tasks</div>
            </div>
            <div>
              <div className="text-2xl font-bold">{briefing?.pending_tasks || 0}</div>
              <div className="text-sm text-gray-500">Pending</div>
            </div>
            <div>
              <div className="text-2xl font-bold">{briefing?.completed_tasks || 0}</div>
              <div className="text-sm text-gray-500">Completed</div>
            </div>
          </div>
          {briefing?.priority_tasks && briefing.priority_tasks.length > 0 && (
            <div>
              <h4 className="font-semibold mb-2">Priority Tasks:</h4>
              <ul className="list-disc list-inside space-y-1">
                {briefing.priority_tasks.slice(0, 5).map((task, idx) => (
                  <li key={idx} className="text-sm">
                    {task.description} (Priority: {task.priority})
                  </li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Financial Snapshot */}
      <Card>
        <CardHeader>
          <CardTitle>💰 Financial Snapshot</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-4 gap-4">
            <div>
              <div className="text-sm text-gray-500">Total Revenue</div>
              <div className="text-xl font-bold">
                ${financial?.total_revenue.toLocaleString() || 0}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Total Expenses</div>
              <div className="text-xl font-bold">
                ${financial?.total_expenses.toLocaleString() || 0}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Net Profit</div>
              <div className="text-xl font-bold">
                ${financial?.net_profit.toLocaleString() || 0}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Transactions</div>
              <div className="text-xl font-bold">
                {financial?.transaction_count || 0}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
