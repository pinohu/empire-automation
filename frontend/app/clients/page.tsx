// app/clients/page.tsx - Clients & Projects
"use client"

import { useEffect, useState, useCallback } from "react"
import { apiClient, type Client, type Project } from "@/lib/api-client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogClose } from "@/components/ui/dialog"

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([])
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [refreshing, setRefreshing] = useState(false)
  const [editingClient, setEditingClient] = useState<Client | null>(null)
  const [editingProject, setEditingProject] = useState<Project | null>(null)
  const [showClientDialog, setShowClientDialog] = useState(false)
  const [showProjectDialog, setShowProjectDialog] = useState(false)
  const [clientForm, setClientForm] = useState({ name: "", email: "", phone: "", source: "", status: "active" })
  const [projectForm, setProjectForm] = useState({ client_id: "", entity_id: "", type: "other", status: "prospect", revenue: "0" })

  const fetchData = useCallback(async () => {
    setRefreshing(true)
    console.log('[Clients] Fetching data...')
    
    const [clientsRes, projectsRes] = await Promise.all([
      apiClient.get<Client[]>("/api/v1/clients"),
      apiClient.get<Project[]>("/api/v1/projects"),
    ])
    
    console.log('[Clients] Clients response:', clientsRes)
    console.log('[Clients] Projects response:', projectsRes)
    
    if (clientsRes.error) console.error('[Clients] Clients error:', clientsRes.error)
    if (projectsRes.error) console.error('[Clients] Projects error:', projectsRes.error)
    
    if (clientsRes.data) setClients(Array.isArray(clientsRes.data) ? clientsRes.data : [])
    if (projectsRes.data) setProjects(Array.isArray(projectsRes.data) ? projectsRes.data : [])
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

  const activeProjects = projects.filter(p => 
    p.status === 'active' || p.status === 'prospect'
  )
  const totalRevenue = projects.reduce((sum, p) => sum + p.revenue, 0)
  const avgLTV = clients.length > 0
    ? clients.reduce((sum, c) => sum + c.lifetime_value, 0) / clients.length
    : 0

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">👥 Clients & Projects</h1>
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
              Total Clients
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{clients.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Active Projects
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeProjects.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Total Project Revenue
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${totalRevenue.toLocaleString()}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Avg Lifetime Value
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${avgLTV.toLocaleString()}</div>
          </CardContent>
        </Card>
      </div>

      {/* Clients Table */}
      <Card className="mb-8">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>👥 Clients</CardTitle>
          <Button 
            onClick={() => {
              setEditingClient(null)
              setClientForm({ name: "", email: "", phone: "", source: "", status: "active" })
              setShowClientDialog(true)
            }}
            size="sm"
          >
            + Add Client
          </Button>
        </CardHeader>
        <CardContent>
          {clients.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="px-4 py-2 text-left">Name</th>
                    <th className="px-4 py-2 text-left">Email</th>
                    <th className="px-4 py-2 text-left">Phone</th>
                    <th className="px-4 py-2 text-left">Status</th>
                    <th className="px-4 py-2 text-left">Source</th>
                    <th className="px-4 py-2 text-left">LTV</th>
                    <th className="px-4 py-2 text-left">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {clients.map((client) => (
                    <tr key={client.id} className="border-b">
                      <td className="px-4 py-2 font-medium">{client.name}</td>
                      <td className="px-4 py-2">{client.email || 'N/A'}</td>
                      <td className="px-4 py-2">{client.phone || 'N/A'}</td>
                      <td className="px-4 py-2">
                        <span className="rounded bg-blue-100 px-2 py-1 text-xs text-blue-800">
                          {client.status}
                        </span>
                      </td>
                      <td className="px-4 py-2">{client.source || 'N/A'}</td>
                      <td className="px-4 py-2">${client.lifetime_value.toLocaleString()}</td>
                      <td className="px-4 py-2">
                        <div className="flex gap-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => {
                              setEditingClient(client)
                              setClientForm({
                                name: client.name,
                                email: client.email || "",
                                phone: client.phone || "",
                                source: client.source || "",
                                status: client.status
                              })
                              setShowClientDialog(true)
                            }}
                          >
                            ✏️ Edit
                          </Button>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={async () => {
                              if (confirm(`Delete client "${client.name}"?`)) {
                                const res = await apiClient.delete(`/api/v1/clients/${client.id}`)
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
            <p className="text-gray-500">No clients found</p>
          )}
        </CardContent>
      </Card>

      {/* Projects Table */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>📁 Active Projects</CardTitle>
          <Button 
            onClick={() => {
              setEditingProject(null)
              setProjectForm({ client_id: "", entity_id: "", type: "other", status: "prospect", revenue: "0" })
              setShowProjectDialog(true)
            }}
            size="sm"
          >
            + Add Project
          </Button>
        </CardHeader>
        <CardContent>
          {projects.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="px-4 py-2 text-left">Type</th>
                    <th className="px-4 py-2 text-left">Status</th>
                    <th className="px-4 py-2 text-left">Revenue</th>
                    <th className="px-4 py-2 text-left">Margin</th>
                    <th className="px-4 py-2 text-left">Start Date</th>
                    <th className="px-4 py-2 text-left">End Date</th>
                    <th className="px-4 py-2 text-left">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {projects.map((project) => (
                    <tr key={project.id} className="border-b">
                      <td className="px-4 py-2">{project.type}</td>
                      <td className="px-4 py-2">
                        <span className={`rounded px-2 py-1 text-xs ${
                          project.status === 'completed' ? 'bg-green-100 text-green-800' :
                          project.status === 'active' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {project.status}
                        </span>
                      </td>
                      <td className="px-4 py-2 font-semibold">
                        ${typeof project.revenue === 'number' ? project.revenue.toLocaleString() : parseFloat(String(project.revenue || 0)).toLocaleString()}
                      </td>
                      <td className="px-4 py-2">
                        {project.margin ? `${project.margin}%` : 'N/A'}
                      </td>
                      <td className="px-4 py-2">
                        {project.start_date 
                          ? new Date(project.start_date).toLocaleDateString()
                          : 'N/A'}
                      </td>
                      <td className="px-4 py-2">
                        {project.end_date 
                          ? new Date(project.end_date).toLocaleDateString()
                          : 'N/A'}
                      </td>
                      <td className="px-4 py-2">
                        <div className="flex gap-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => {
                              setEditingProject(project)
                              setProjectForm({
                                client_id: project.client_id,
                                entity_id: project.entity_id,
                                type: project.type,
                                status: project.status,
                                revenue: String(project.revenue || 0)
                              })
                              setShowProjectDialog(true)
                            }}
                          >
                            ✏️ Edit
                          </Button>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={async () => {
                              if (confirm("Delete this project?")) {
                                const res = await apiClient.delete(`/api/v1/projects/${project.id}`)
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
            <p className="text-gray-500">No projects found</p>
          )}
        </CardContent>
      </Card>

      {/* Client Edit Dialog */}
      <Dialog open={showClientDialog} onOpenChange={setShowClientDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editingClient ? "Edit Client" : "Add Client"}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Name *</label>
              <Input
                value={clientForm.name}
                onChange={(e) => setClientForm({ ...clientForm, name: e.target.value })}
                placeholder="Client name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <Input
                type="email"
                value={clientForm.email}
                onChange={(e) => setClientForm({ ...clientForm, email: e.target.value })}
                placeholder="client@example.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Phone</label>
              <Input
                value={clientForm.phone}
                onChange={(e) => setClientForm({ ...clientForm, phone: e.target.value })}
                placeholder="(555) 123-4567"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Source</label>
              <Input
                value={clientForm.source}
                onChange={(e) => setClientForm({ ...clientForm, source: e.target.value })}
                placeholder="Lead source"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Status</label>
              <select
                value={clientForm.status}
                onChange={(e) => setClientForm({ ...clientForm, status: e.target.value })}
                className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
              >
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="lead">Lead</option>
              </select>
            </div>
          </div>
          <DialogFooter>
            <DialogClose onClick={() => setShowClientDialog(false)}>Cancel</DialogClose>
            <Button
              onClick={async () => {
                if (!clientForm.name) {
                  alert("Name is required")
                  return
                }
                const res = editingClient
                  ? await apiClient.put(`/api/v1/clients/${editingClient.id}`, clientForm)
                  : await apiClient.post("/api/v1/clients", clientForm)
                if (!res.error) {
                  setShowClientDialog(false)
                  fetchData()
                } else {
                  alert(`Error: ${res.error}`)
                }
              }}
            >
              {editingClient ? "Update" : "Create"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Project Edit Dialog */}
      <Dialog open={showProjectDialog} onOpenChange={setShowProjectDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editingProject ? "Edit Project" : "Add Project"}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Client ID *</label>
              <Input
                value={projectForm.client_id}
                onChange={(e) => setProjectForm({ ...projectForm, client_id: e.target.value })}
                placeholder="Client UUID"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Entity ID *</label>
              <Input
                value={projectForm.entity_id}
                onChange={(e) => setProjectForm({ ...projectForm, entity_id: e.target.value })}
                placeholder="Entity UUID"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Type</label>
              <select
                value={projectForm.type}
                onChange={(e) => setProjectForm({ ...projectForm, type: e.target.value })}
                className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
              >
                <option value="TC">Transaction Coordination</option>
                <option value="mortgage">Mortgage</option>
                <option value="tax">Tax</option>
                <option value="notary">Notary</option>
                <option value="ux_consulting">UX Consulting</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Status</label>
              <select
                value={projectForm.status}
                onChange={(e) => setProjectForm({ ...projectForm, status: e.target.value })}
                className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
              >
                <option value="prospect">Prospect</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Revenue</label>
              <Input
                type="number"
                value={projectForm.revenue}
                onChange={(e) => setProjectForm({ ...projectForm, revenue: e.target.value })}
                placeholder="0"
              />
            </div>
          </div>
          <DialogFooter>
            <DialogClose onClick={() => setShowProjectDialog(false)}>Cancel</DialogClose>
            <Button
              onClick={async () => {
                if (!projectForm.client_id || !projectForm.entity_id) {
                  alert("Client ID and Entity ID are required")
                  return
                }
                const data = {
                  ...projectForm,
                  revenue: parseFloat(projectForm.revenue) || 0
                }
                const res = editingProject
                  ? await apiClient.put(`/api/v1/projects/${editingProject.id}`, data)
                  : await apiClient.post("/api/v1/projects", data)
                if (!res.error) {
                  setShowProjectDialog(false)
                  fetchData()
                } else {
                  alert(`Error: ${res.error}`)
                }
              }}
            >
              {editingProject ? "Update" : "Create"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

