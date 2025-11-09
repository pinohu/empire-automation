# 🚀 Quick Start Guide - Web Frontend

## Start the Web Application

### Step 1: Start the Backend API

```bash
cd empire-automation
uvicorn empire_automation.api.main:app --reload
```

Backend will run on: **http://localhost:8000**

### Step 2: Start the Frontend

Open a new terminal:

```bash
cd empire-automation/frontend
npm install
npm run dev
```

Frontend will run on: **http://localhost:3000**

### Step 3: Access the Dashboard

Open your browser and go to: **http://localhost:3000**

---

## 🎯 Available Pages

1. **Overview** (`/`) - Main dashboard with key metrics
2. **90-Day Plan** (`/plan`) - Task tracking and progress
3. **Financial** (`/financial`) - Revenue and expense tracking
4. **Clients & Projects** (`/clients`) - Client and project management
5. **Lead Pipeline** (`/leads`) - Lead management and conversion
6. **Agent Status** (`/agents`) - AI agent performance monitoring

---

## 📱 Features

- ✅ **Real-time Data** - Auto-refreshes every 5 minutes
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Type-safe** - Full TypeScript support
- ✅ **Modern UI** - Clean, professional interface
- ✅ **Sidebar Navigation** - Easy access to all pages

---

## 🔧 Troubleshooting

### Frontend won't start
- Make sure Node.js 20+ is installed: `node --version`
- Run `npm install` in the frontend directory
- Check for port conflicts (default port 3000)

### API connection errors
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS is configured in backend

### No data showing
- Check backend API is responding: http://localhost:8000/api/health
- **IMPORTANT:** Backend must be running! See `START_BACKEND_SIMPLE.md` or double-click `START_BACKEND.bat`
- Verify database is initialized
- Check browser console for errors

---

## 📝 Environment Setup

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

**You're all set!** 🎉

The web frontend provides a complete interface to view, access, and control all Empire Automation features.

