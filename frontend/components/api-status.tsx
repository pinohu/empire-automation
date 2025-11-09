// components/api-status.tsx
"use client"

import { useEffect, useState } from "react"
import { apiClient } from "@/lib/api-client"

export function ApiStatus() {
  const [status, setStatus] = useState<"checking" | "connected" | "disconnected">("checking")
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function checkApi() {
      try {
        // Use fetch directly with timeout
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout
        
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
        const response = await fetch(`${apiUrl}/api/health`, {
          signal: controller.signal,
          method: "GET",
        })
        
        clearTimeout(timeoutId)
        
        if (response.ok) {
          const data = await response.json()
          setStatus("connected")
          setError(null)
        } else {
          setStatus("disconnected")
          setError(`HTTP ${response.status}`)
        }
      } catch (err) {
        if (err instanceof Error && err.name === "AbortError") {
          setStatus("disconnected")
          setError("Request timeout - backend not responding")
        } else {
          setStatus("disconnected")
          setError(err instanceof Error ? err.message : "Connection failed")
        }
      }
    }

    checkApi()
    const interval = setInterval(checkApi, 30000) // Check every 30 seconds
    return () => clearInterval(interval)
  }, [])

  return (
    <div className={`px-4 py-2 text-sm ${
      status === "connected" ? "bg-green-100 text-green-800" :
      status === "disconnected" ? "bg-red-100 text-red-800" :
      "bg-yellow-100 text-yellow-800"
    }`}>
      {status === "checking" && "🔄 Checking API connection..."}
      {status === "connected" && "✅ API Connected"}
      {status === "disconnected" && (
        <div>
          <span className="font-semibold">❌ API Disconnected</span>
          {error && <span className="ml-2">- {error}</span>}
          <div className="mt-1 text-xs">
            Start backend: <code className="bg-gray-200 px-1 rounded">cd empire-automation && python start_api.py</code>
          </div>
        </div>
      )}
    </div>
  )
}

