// app/plan/page.tsx - 90-Day Plan
"use client"

import { useEffect, useState, useCallback } from "react"
import { apiClient, type PlanProgress, type Task } from "@/lib/api-client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function PlanPage() {
  const [progress, setProgress] = useState<PlanProgress | null>(null)
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [refreshing, setRefreshing] = useState(false)

  const fetchData = useCallback(async () => {
    setRefreshing(true)
    console.log('[Plan] Fetching data...')
    
    const [progressRes, tasksRes] = await Promise.all([
      apiClient.get<PlanProgress>("/api/v1/90-day-plan/progress"),
      apiClient.get<Task[]>("/api/v1/90-day-plan/today"),
    ])
    
    console.log('[Plan] Progress response:', progressRes)
    console.log('[Plan] Tasks response:', tasksRes)
    
    if (progressRes.error) {
      console.error('[Plan] Progress error:', progressRes.error)
    } else if (progressRes.data) {
      setProgress(progressRes.data)
    }
    
    if (tasksRes.error) {
      console.error('[Plan] Tasks error:', tasksRes.error)
    } else if (tasksRes.data) {
      setTasks(Array.isArray(tasksRes.data) ? tasksRes.data : [])
    }
    
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
        <h1 className="text-3xl font-bold">📅 90-Day Plan Progress</h1>
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

      {/* Progress Overview */}
      <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Total Tasks
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{progress?.total_tasks || 0}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Completed
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{progress?.completed_tasks || 0}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              In Progress
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{progress?.in_progress_tasks || 0}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-gray-500">
              Pending
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{progress?.pending_tasks || 0}</div>
          </CardContent>
        </Card>
      </div>

      {/* Completion Progress */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Overall Completion</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="mb-2 flex justify-between text-sm">
            <span>{typeof progress?.completion_percentage === 'number' ? progress.completion_percentage.toFixed(1) : '0.0'}% Complete</span>
            <span>Day {progress?.current_day || 1} of 90</span>
          </div>
          <div className="h-4 w-full overflow-hidden rounded-full bg-gray-200">
            <div
              className="h-full bg-green-600 transition-all"
              style={{ width: `${progress?.completion_percentage || 0}%` }}
            />
          </div>
        </CardContent>
      </Card>

      {/* Today's Tasks */}
      <Card>
        <CardHeader>
          <CardTitle>📋 Today's Tasks</CardTitle>
        </CardHeader>
        <CardContent>
          {tasks.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="px-4 py-2 text-left">Description</th>
                    <th className="px-4 py-2 text-left">Status</th>
                    <th className="px-4 py-2 text-left">Agent</th>
                    <th className="px-4 py-2 text-left">Hours</th>
                    <th className="px-4 py-2 text-left">Cost</th>
                  </tr>
                </thead>
                <tbody>
                  {tasks.map((task) => (
                    <tr key={task.id} className="border-b">
                      <td className="px-4 py-2">{task.description}</td>
                      <td className="px-4 py-2">
                        <select
                          value={task.status}
                          onChange={async (e) => {
                            // Note: Task update endpoint would need to be added to backend
                            // For now, this is a placeholder that shows the UI is ready
                            const newStatus = e.target.value
                            alert(`Task status update would be sent to backend. Status: ${newStatus}`)
                            // await apiClient.put(`/api/v1/90-day-plan/tasks/${task.id}`, { status: newStatus })
                            // fetchData()
                          }}
                          className={`rounded px-2 py-1 text-xs border ${
                            task.status === 'completed' ? 'bg-green-100 text-green-800 border-green-300' :
                            task.status === 'in_progress' ? 'bg-blue-100 text-blue-800 border-blue-300' :
                            'bg-gray-100 text-gray-800 border-gray-300'
                          }`}
                        >
                          <option value="pending">Pending</option>
                          <option value="in_progress">In Progress</option>
                          <option value="completed">Completed</option>
                        </select>
                      </td>
                      <td className="px-4 py-2">{task.agent_assigned || 'N/A'}</td>
                      <td className="px-4 py-2">{task.estimated_hours || 0}</td>
                      <td className="px-4 py-2">${typeof task.cost === 'number' ? task.cost.toFixed(2) : (task.cost ? parseFloat(String(task.cost)).toFixed(2) : '0.00')}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-500">No tasks found for today</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

