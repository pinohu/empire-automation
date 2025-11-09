# 🔐 Credentials Checklist

## ✅ Already Configured

### Google Workspace
- ✅ **Service Account Credentials**: `credentials/uplifted-record-477622-b7-f25455bd0df5.json`
- ✅ **Spreadsheet ID**: `1LnDX6u0V5ows33BJyVSohc4tZIBwmut5LnEU8mMWfWk`
- ✅ **Status**: Fully functional - Sheets, Calendar, Gmail APIs working

---

## 🔴 Critical - Required for Core Functionality

### 1. AgenticFlow (AI Agents)

**Priority**: 🔴 **CRITICAL** - System cannot execute tasks without this

**What you need:**
- `AGENTICFLOW_API_KEY` - Your AgenticFlow API key
- `AGENTICFLOW_MASTER_ORCHESTRATOR_ID` - Master Orchestrator agent ID
- `AGENTICFLOW_PROFESSIONAL_SERVICES_ID` - Professional Services agent ID
- `AGENTICFLOW_MARKETING_ID` - Marketing agent ID
- `AGENTICFLOW_FINANCIAL_ID` - Financial agent ID
- `AGENTICFLOW_DIRECTORY_MANAGER_ID` - Directory Manager agent ID
- `AGENTICFLOW_ENTITY_COMPLIANCE_ID` - Entity Compliance agent ID
- `AGENTICFLOW_CLIENT_SUCCESS_ID` - Client Success agent ID

**How to get:**
1. Login to AgenticFlow.com
2. Go to Settings → API Keys
3. Generate API key
4. Create 7 agents (see agent configurations in documentation)
5. Copy each agent's ID

**Add to `.env`:**
```bash
AGENTICFLOW_API_KEY=your_api_key_here
AGENTICFLOW_MASTER_ORCHESTRATOR_ID=agent_id_123
AGENTICFLOW_PROFESSIONAL_SERVICES_ID=agent_id_456
# ... (other agent IDs)
```

**Impact if missing:** 
- ❌ Cannot execute Day 1 tasks
- ❌ Cannot generate daily briefings
- ❌ Agents cannot delegate tasks
- ⚠️ System will run but agents won't function

---

## 🟡 Important - Required for Key Features

### 2. SuiteDash (CRM & Project Management)

**Priority**: 🟡 **IMPORTANT** - Needed for client/project management

**What you need:**
- `SUITEDASH_API_KEY` - Your SuiteDash API key
- `SUITEDASH_BASE_URL` - Your SuiteDash account URL (optional)

**How to get:**
1. Login to SuiteDash
2. Go to Settings → API
3. Generate API key
4. Note your account URL (e.g., `https://your-account.suitedash.com`)

**Add to `.env`:**
```bash
SUITEDASH_API_KEY=your_api_key_here
SUITEDASH_BASE_URL=https://your-account.suitedash.com/api
```

**Impact if missing:**
- ❌ Cannot create clients in SuiteDash
- ❌ Cannot create projects
- ❌ Cannot generate invoices
- ⚠️ Client onboarding workflow will be limited

---

### 3. Emailit (Email Marketing)

**Priority**: 🟡 **IMPORTANT** - Needed for email sequences

**What you need:**
- `EMAILIT_API_KEY` - Your Emailit API key
- `EMAILIT_BASE_URL` - Emailit API URL (optional, defaults to `https://api.emailit.com`)

**How to get:**
1. Login to Emailit
2. Go to Settings → API
3. Generate API key

**Add to `.env`:**
```bash
EMAILIT_API_KEY=your_api_key_here
EMAILIT_BASE_URL=https://api.emailit.com
```

**Impact if missing:**
- ❌ Cannot send email sequences
- ❌ Cannot add leads to nurture campaigns
- ⚠️ Lead processing workflow will be limited

---

## 🟢 Optional - Enhanced Features

### 4. Brilliant Directories

**Priority**: 🟢 **OPTIONAL** - Only if using directory features

**What you need:**
- `BRILLIANT_DIRECTORIES_API_KEY` - Your Brilliant Directories API key
- `BRILLIANT_DIRECTORIES_BASE_URL` - Your directory domain API URL

**How to get:**
1. Login to Brilliant Directories
2. Go to Settings → API/Integrations
3. Generate API key

**Add to `.env`:**
```bash
BRILLIANT_DIRECTORIES_API_KEY=your_api_key_here
BRILLIANT_DIRECTORIES_BASE_URL=https://your-directory-domain.com/api/v2
```

**Impact if missing:**
- ⚠️ Directory member onboarding workflow will be limited
- ✅ System works fine without it

---

### 5. Formaloo (Forms)

**Priority**: 🟢 **OPTIONAL** - Only if using form features

**What you need:**
- `FORMALOO_API_KEY` - Your Formaloo API key
- `FORMALOO_BASE_URL` - Formaloo API URL (optional)

**How to get:**
1. Login to Formaloo
2. Go to Settings → API
3. Generate API key

**Add to `.env`:**
```bash
FORMALOO_API_KEY=your_api_key_here
FORMALOO_BASE_URL=https://api.formaloo.com
```

**Impact if missing:**
- ⚠️ Form-based workflows will be limited
- ✅ System works fine without it

---

### 6. KonnectzIT Webhook Secret

**Priority**: 🟢 **OPTIONAL** - For webhook security

**What you need:**
- `KONNECTZIT_WEBHOOK_SECRET` - Webhook signature secret

**How to get:**
1. Login to KonnectzIT
2. Go to Workflow Settings → Webhook Security
3. Generate webhook secret (if available)

**Add to `.env`:**
```bash
KONNECTZIT_WEBHOOK_SECRET=your_webhook_secret_here
```

**Impact if missing:**
- ⚠️ Webhooks will work but without signature verification
- ✅ System works fine without it (less secure)

---

### 7. Anthropic API Key

**Priority**: 🟢 **OPTIONAL** - Only if using Claude directly (not via AgenticFlow)

**What you need:**
- `ANTHROPIC_API_KEY` - Your Anthropic/Claude API key

**How to get:**
1. Go to console.anthropic.com
2. Sign up/login
3. Go to API Keys
4. Create new key

**Add to `.env`:**
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

**Impact if missing:**
- ✅ Not needed if using AgenticFlow (which handles Claude)
- ⚠️ Only needed if you want direct Claude API access

---

## 📋 Priority Summary

### Must Have (System Won't Work Properly)
1. ✅ **Google Workspace** - Already configured
2. 🔴 **AgenticFlow** - Required for agent execution

### Should Have (Key Features)
3. 🟡 **SuiteDash** - For CRM functionality
4. 🟡 **Emailit** - For email marketing

### Nice to Have (Enhanced Features)
5. 🟢 **Brilliant Directories** - For directory management
6. 🟢 **Formaloo** - For form automation
7. 🟢 **KonnectzIT Webhook Secret** - For security
8. 🟢 **Anthropic** - Only if not using AgenticFlow

---

## 🚀 Quick Setup Order

### Phase 1: Minimum Viable (Can launch Day 1)
1. ✅ Google Workspace (DONE)
2. 🔴 AgenticFlow API key + 7 agents

### Phase 2: Full Functionality
3. 🟡 SuiteDash API key
4. 🟡 Emailit API key

### Phase 3: Enhanced Features
5. 🟢 Brilliant Directories API key
6. 🟢 Formaloo API key
7. 🟢 KonnectzIT webhook secret

---

## 📝 Complete `.env` Template

```bash
# ============================================
# CRITICAL - Required for Core Functionality
# ============================================

# Google Workspace (✅ CONFIGURED)
GOOGLE_CREDENTIALS_FILE=credentials/uplifted-record-477622-b7-f25455bd0df5.json
GOOGLE_SHEETS_ID=1LnDX6u0V5ows33BJyVSohc4tZIBwmut5LnEU8mMWfWk

# AgenticFlow (🔴 REQUIRED)
AGENTICFLOW_API_KEY=your_agenticflow_api_key_here
AGENTICFLOW_MASTER_ORCHESTRATOR_ID=master-orchestrator
AGENTICFLOW_PROFESSIONAL_SERVICES_ID=professional-services
AGENTICFLOW_MARKETING_ID=marketing-lead-gen
AGENTICFLOW_FINANCIAL_ID=financial-operations
AGENTICFLOW_DIRECTORY_MANAGER_ID=directory-manager
AGENTICFLOW_ENTITY_COMPLIANCE_ID=entity-compliance
AGENTICFLOW_CLIENT_SUCCESS_ID=client-success

# ============================================
# IMPORTANT - Key Features
# ============================================

# SuiteDash (🟡 IMPORTANT)
SUITEDASH_API_KEY=your_suitedash_api_key_here
SUITEDASH_BASE_URL=https://your-account.suitedash.com/api

# Emailit (🟡 IMPORTANT)
EMAILIT_API_KEY=your_emailit_api_key_here
EMAILIT_BASE_URL=https://api.emailit.com

# ============================================
# OPTIONAL - Enhanced Features
# ============================================

# Brilliant Directories (🟢 OPTIONAL)
BRILLIANT_DIRECTORIES_API_KEY=your_brilliant_directories_api_key_here
BRILLIANT_DIRECTORIES_BASE_URL=https://your-directory-domain.com/api/v2

# Formaloo (🟢 OPTIONAL)
FORMALOO_API_KEY=your_formaloo_api_key_here
FORMALOO_BASE_URL=https://api.formaloo.com

# KonnectzIT (🟢 OPTIONAL - Security)
KONNECTZIT_WEBHOOK_SECRET=your_webhook_secret_here

# Anthropic (🟢 OPTIONAL - Only if not using AgenticFlow)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# ============================================
# DATABASE (Optional - defaults to SQLite)
# ============================================
DATABASE_URL=sqlite:///./empire.db
```

---

## ✅ Current Status

- ✅ **Google Workspace**: Fully configured and tested
- 🔴 **AgenticFlow**: **NEEDED NEXT** - Required for Day 1 execution
- 🟡 **SuiteDash**: Needed for client management
- 🟡 **Emailit**: Needed for email sequences
- 🟢 **Others**: Optional enhancements

---

## 🎯 Next Steps

1. **Get AgenticFlow API key** (CRITICAL)
2. **Create 7 agents in AgenticFlow platform**
3. **Add Agent IDs to `.env`**
4. **Test agent execution**
5. **Then add SuiteDash and Emailit** (for full functionality)

**You can launch Day 1 with just Google Workspace + AgenticFlow!**

