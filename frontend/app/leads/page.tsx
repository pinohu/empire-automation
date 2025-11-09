// app/leads/page.tsx - Lead Pipeline
"use client"

import { useEffect, useState, useCallback } from "react"
import { apiClient, type Lead } from "@/lib/api-client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogClose } from "@/components/ui/dialog"

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [refreshing, setRefreshing] = useState(false)
  const [editingLead, setEditingLead] = useState<Lead | null>(null)
  const [showLeadDialog, setShowLeadDialog] = useState(false)
  const [leadForm, setLeadForm] = useState({ name: "", email: "", phone: "", source: "", status: "new", score: "0" })

  const fetchData = useCallback(async () => {
    setRefreshing(true)
    console.log('[Leads] Fetching data...')
    
    const res = await apiClient.get<Lead[]>("/api/v1/leads")
    console.log('[Leads] Response:', res)
    
    if (res.error) console.error('[Leads] Error:', res.error)
    if (res.data) setLeads(Array.isArray(res.data) ? res.data : [])
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

  const newLeads = leads.filter(l => l.status === 'new')
  const qualifiedLeads = leads.filter(l => l.status === 'qualified')
  const convertedLeads = leads.filter(l => l.status === 'won')

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">🎯 Lead Pipeline</h1>
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

      {/* Metrics */}
      <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Total Leads
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{leads.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              New Leads
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{newLeads.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Qualified
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{qualifiedLeads.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Converted
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{convertedLeads.length}</div>
          </CardContent>
        </Card>
      </div>

      {/* Leads Table */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>📋 All Leads</CardTitle>
          <Button 
            onClick={() => {
              setEditingLead(null)
              setLeadForm({ name: "", email: "", phone: "", source: "", status: "new", score: "0" })
              setShowLeadDialog(true)
            }}
            size="sm"
          >
            + Add Lead
          </Button>
        </CardHeader>
        <CardContent>
          {leads.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="px-4 py-2 text-left">Name</th>
                    <th className="px-4 py-2 text-left">Email</th>
                    <th className="px-4 py-2 text-left">Phone</th>
                    <th className="px-4 py-2 text-left">Source</th>
                    <th className="px-4 py-2 text-left">Score</th>
                    <th className="px-4 py-2 text-left">Status</th>
                    <th className="px-4 py-2 text-left">Assigned To</th>
                    <th className="px-4 py-2 text-left">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {leads.map((lead) => (
                    <tr key={lead.id} className="border-b">
                      <td className="px-4 py-2 font-medium">{lead.name}</td>
                      <td className="px-4 py-2">{lead.email || 'N/A'}</td>
                      <td className="px-4 py-2">{lead.phone || 'N/A'}</td>
                      <td className="px-4 py-2">{lead.source}</td>
                      <td className="px-4 py-2">
                        {lead.score ? (
                          <span className={`rounded px-2 py-1 text-xs ${
                            lead.score >= 80 ? 'bg-green-100 text-green-800' :
                            lead.score >= 60 ? 'bg-yellow-100 text-yellow-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {lead.score}
                          </span>
                        ) : 'N/A'}
                      </td>
                      <td className="px-4 py-2">
                        <span className="rounded bg-blue-100 px-2 py-1 text-xs text-blue-800">
                          {lead.status}
                        </span>
                      </td>
                      <td className="px-4 py-2">{lead.assigned_to || 'N/A'}</td>
                      <td className="px-4 py-2">
                        <div className="flex gap-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => {
                              setEditingLead(lead)
                              setLeadForm({
                                name: lead.name || "",
                                email: lead.email || "",
                                phone: lead.phone || "",
                                source: lead.source,
                                status: lead.status,
                                score: String(lead.score || 0)
                              })
                              setShowLeadDialog(true)
                            }}
                          >
                            ✏️ Edit
                          </Button>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={async () => {
                              if (confirm(`Delete lead "${lead.name}"?`)) {
                                const res = await apiClient.delete(`/api/v1/leads/${lead.id}`)
                                if (!res.error) {
                                  fetchData()
                                } else {
                                  alert(`Error: ${res.error}`)
                                }
                              }
                            }}
                          >
                            🗑️ Delete
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-500">No leads found</p>
          )}
        </CardContent>
      </Card>

      {/* Lead Edit Dialog */}
      <Dialog open={showLeadDialog} onOpenChange={setShowLeadDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editingLead ? "Edit Lead" : "Add Lead"}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Name</label>
              <Input
                value={leadForm.name}
                onChange={(e) => setLeadForm({ ...leadForm, name: e.target.value })}
                placeholder="Lead name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <Input
                type="email"
                value={leadForm.email}
                onChange={(e) => setLeadForm({ ...leadForm, email: e.target.value })}
                placeholder="lead@example.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Phone</label>
              <Input
                value={leadForm.phone}
                onChange={(e) => setLeadForm({ ...leadForm, phone: e.target.value })}
                placeholder="(555) 123-4567"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Source *</label>
              <Input
                value={leadForm.source}
                onChange={(e) => setLeadForm({ ...leadForm, source: e.target.value })}
                placeholder="Lead source"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Status</label>
              <select
                value={leadForm.status}
                onChange={(e) => setLeadForm({ ...leadForm, status: e.target.value })}
                className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
              >
                <option value="new">New</option>
                <option value="contacted">Contacted</option>
                <option value="qualified">Qualified</option>
                <option value="proposal_sent">Proposal Sent</option>
                <option value="negotiating">Negotiating</option>
                <option value="won">Won</option>
                <option value="lost">Lost</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Score (0-100)</label>
              <Input
                type="number"
                min="0"
                max="100"
                value={leadForm.score}
                onChange={(e) => setLeadForm({ ...leadForm, score: e.target.value })}
                placeholder="0"
              />
            </div>
          </div>
          <DialogFooter>
            <DialogClose onClick={() => setShowLeadDialog(false)}>Cancel</DialogClose>
            <Button
              onClick={async () => {
                if (!leadForm.source) {
                  alert("Source is required")
                  return
                }
                const data = {
                  ...leadForm,
                  score: parseInt(leadForm.score) || 0
                }
                const res = editingLead
                  ? await apiClient.put(`/api/v1/leads/${editingLead.id}`, data)
                  : await apiClient.post("/api/v1/leads", data)
                if (!res.error) {
                  setShowLeadDialog(false)
                  fetchData()
                } else {
                  alert(`Error: ${res.error}`)
                }
              }}
            >
              {editingLead ? "Update" : "Create"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

