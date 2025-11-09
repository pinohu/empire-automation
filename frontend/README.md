# Empire Automation Frontend

Modern Next.js web frontend for the Empire Automation system.

## Features

- 📊 **Overview Dashboard** - Key metrics, progress tracking, and daily briefings
- 📅 **90-Day Plan** - Task management and progress visualization
- 💰 **Financial Dashboard** - Revenue, expenses, and transaction tracking
- 👥 **Clients & Projects** - Client management and project tracking
- 🎯 **Lead Pipeline** - Lead management and conversion tracking
- 🤖 **Agent Status** - AI agent performance and task monitoring

## Tech Stack

- **Next.js 16** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **React 19** - Latest React features

## Getting Started

### Prerequisites

- Node.js 20+ installed
- FastAPI backend running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.local.example .env.local

# Edit .env.local and set NEXT_PUBLIC_API_URL if needed
```

### Development

```bash
# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Overview dashboard
│   ├── plan/              # 90-Day Plan page
│   ├── financial/         # Financial dashboard
│   ├── clients/           # Clients & Projects page
│   ├── leads/             # Lead Pipeline page
│   └── agents/            # Agent Status page
├── components/            # React components
│   ├── ui/               # UI components (Button, Card, etc.)
│   └── layout/           # Layout components (Sidebar)
├── lib/                  # Utilities
│   └── api-client.ts     # API client for FastAPI backend
└── public/              # Static assets
```

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000` by default.

All API endpoints use the `/api/v1/` prefix:
- `/api/v1/daily-briefing` - Daily briefing data
- `/api/v1/financial/dashboard` - Financial metrics
- `/api/v1/90-day-plan/progress` - Plan progress
- `/api/v1/clients` - Client data
- `/api/v1/projects` - Project data
- `/api/v1/leads` - Lead data

## Features

### Real-time Updates
- Auto-refreshes data every 5 minutes
- Manual refresh available via browser refresh

### Responsive Design
- Mobile-friendly layout
- Works on all screen sizes

### Type Safety
- Full TypeScript support
- Type-safe API client

## Environment Variables

Create `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development

### Adding New Pages

1. Create a new file in `app/` directory
2. Use the API client from `lib/api-client.ts`
3. Add navigation link in `components/layout/sidebar.tsx`

### Styling

- Uses Tailwind CSS utility classes
- Custom components in `components/ui/`
- Consistent design system

## Troubleshooting

### API Connection Issues

- Ensure FastAPI backend is running on port 8000
- Check CORS settings in backend
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`

### Build Errors

- Run `npm install` to ensure dependencies are installed
- Check TypeScript errors with `npm run lint`

## License

Proprietary - All rights reserved
