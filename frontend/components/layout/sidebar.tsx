// components/layout/sidebar.tsx
"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"

const navigation = [
  { name: "Overview", href: "/", icon: "📊" },
  { name: "90-Day Plan", href: "/plan", icon: "📅" },
  { name: "Financial", href: "/financial", icon: "💰" },
  { name: "Clients & Projects", href: "/clients", icon: "👥" },
  { name: "Lead Pipeline", href: "/leads", icon: "🎯" },
  { name: "Agent Status", href: "/agents", icon: "🤖" },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="flex h-screen w-64 flex-col bg-gray-900 text-white">
      <div className="flex h-16 items-center justify-center border-b border-gray-800">
        <h1 className="text-xl font-bold">🚀 Empire Automation</h1>
      </div>
      <nav className="flex-1 space-y-1 px-2 py-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center space-x-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-gray-300 hover:bg-gray-800 hover:text-white"
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span>{item.name}</span>
            </Link>
          )
        })}
      </nav>
      <div className="border-t border-gray-800 p-4">
        <p className="text-xs text-gray-400">Empire Automation v0.1.0</p>
      </div>
    </div>
  )
}

