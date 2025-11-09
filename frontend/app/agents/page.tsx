// app/agents/page.tsx - Agent Status
"use client"

import { useEffect, useState, useCallback } from "react"
import { apiClient, type Task } from "@/lib/api-client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

const AGENTS = [
  { id: "master-orchestrator", name: "Master Orchestrator", icon: "🎯" },
  { id: "professional-services", name: "Professional Services", icon: "💼" },
  { id: "marketing", name: "Marketing & Lead Gen", icon: "📢" },
  { id: "financial", name: "Financial Operations", icon: "💰" },
  { id: "directory-manager", name: "Directory Manager", icon: "📁" },
  { id: "entity-compliance", name: "Entity Compliance", icon: "📋" },
  { id: "client-success", name: "Client Success", icon: "✅" },
]

export default function AgentsPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [refreshing, setRefreshing] = useState(false)

  const fetchData = useCallback(async () => {
    setRefreshing(true)
    console.log('[Agents] Fetching data...')
    
    const res = await apiClient.get<Task[]>("/api/v1/90-day-plan/today")
    console.log('[Agents] Response:', res)
    
    if (res.error) console.error('[Agents] Error:', res.error)
    if (res.data) setTasks(Array.isArray(res.data) ? res.data : [])
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

  const tasksByAgent: Record<string, Task[]> = {}
  tasks.forEach(task => {
    const agent = task.agent_assigned || 'unassigned'
    if (!tasksByAgent[agent]) tasksByAgent[agent] = []
    tasksByAgent[agent].push(task)
  })

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">🤖 Agent Status</h1>
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

      {/* Agent Overview */}
      <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3">
        {AGENTS.map((agent) => {
          const agentTasks = tasksByAgent[agent.id] || []
          const completed = agentTasks.filter(t => t.status === 'completed').length
          const total = agentTasks.length
          return (
            <Card key={agent.id}>
              <CardHeader>
                <CardTitle className="text-lg">
                  {agent.icon} {agent.name}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {completed}/{total} tasks
                </div>
                <div className="text-sm text-gray-500">
                  {total > 0 ? `${(typeof completed === 'number' && typeof total === 'number' ? (completed/total*100).toFixed(0) : '0')}% complete` : 'No tasks'}
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Escalated Items */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>⚠️ Escalated Items</CardTitle>
        </CardHeader>
        <CardContent>
          {tasks.filter(t => t.owner_required).length > 0 ? (
            <div className="space-y-2">
              {tasks.filter(t => t.owner_required).map((task) => (
                <div key={task.id} className="rounded bg-yellow-50 p-3">
                  <div className="font-medium">{task.description}</div>
                  <div className="text-sm text-gray-600">
                    Agent: {task.agent_assigned || 'Unassigned'} | 
                    Reason: Owner action required
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No escalated items - all agents operating smoothly!</p>
          )}
        </CardContent>
      </Card>

      {/* Agent Performance */}
      <Card>
        <CardHeader>
          <CardTitle>📊 Agent Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="px-4 py-2 text-left">Agent</th>
                  <th className="px-4 py-2 text-left">Total Tasks</th>
                  <th className="px-4 py-2 text-left">Completed</th>
                  <th className="px-4 py-2 text-left">Completion Rate</th>
                </tr>
              </thead>
              <tbody>
                {AGENTS.map((agent) => {
                  const agentTasks = tasksByAgent[agent.id] || []
                  const completed = agentTasks.filter(t => t.status === 'completed').length
                  const total = agentTasks.length
                  return (
                    <tr key={agent.id} className="border-b">
                      <td className="px-4 py-2">{agent.name}</td>
                      <td className="px-4 py-2">{total}</td>
                      <td className="px-4 py-2">{completed}</td>
                      <td className="px-4 py-2">
                        {total > 0 ? `${(typeof completed === 'number' && typeof total === 'number' ? (completed/total*100).toFixed(1) : '0.0')}%` : '0%'}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

