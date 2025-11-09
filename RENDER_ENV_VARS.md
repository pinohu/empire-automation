# 🔐 Render Environment Variables Checklist

Copy these environment variables to your Render Web Service:

## Required Variables

```
DATABASE_URL=<from-postgresql-service-internal-url>
CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app
PLAN_START_DATE=2024-01-01
ENVIRONMENT=production
```

## API Keys (Copy from your local .env file)

```
AGENTICFLOW_API_KEY=<your-key>
SUITEDASH_API_KEY=<your-key>
SUITEDASH_API_AUTH_CREDENTIAL=<your-credential>
EMAILIT_API_KEY=<your-key>
BRILLIANT_DIRECTORIES_API_KEY=<your-key>
FORMALOO_API_KEY=<your-key>
FORMALOO_API_SECRET=<your-secret>
ANTHROPIC_API_KEY=<your-key>
```

## Other Configuration

```
GOOGLE_CREDENTIALS_FILE=credentials/google-service-account.json
GOOGLE_SHEETS_ID=<your-id>
REDIS_URL=redis://localhost:6379/0
NOTIFICATION_CHANNEL=log
LOG_LEVEL=INFO
```

## How to Add in Render

1. Go to your Web Service in Render Dashboard
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add each variable one by one
5. Click **"Save Changes"**

---

**Note**: `DATABASE_URL` will be automatically provided by Render when you link the PostgreSQL service, but you can also add it manually.

