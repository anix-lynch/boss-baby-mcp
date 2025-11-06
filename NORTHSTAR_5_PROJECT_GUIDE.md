# 🌟 Northstar 5 Project - Complete Guide for GitHub Copilot

## 🎯 What is Northstar 5?

**Northstar 5** is a comprehensive suite of **5 interoperable MCP-based projects** that demonstrate mastery across AI data architecture, ETL, cloud deployment, orchestration, and visualization. Each project stands alone but connects through shared assets for a unified ecosystem under the **ZeroShot.dev** brand.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                ZeroShot.dev Brand                      │
│                                                     │
│  ┌─────────────┬─────────────┬─────────────┐    │
│  │ Resume MCP  │ Certificates │ Northstar 5 │    │
│  │ (Core)      │ (Data)      │ (Projects)  │    │
│  └─────────────┴─────────────┴─────────────┘    │
│                ↓                                   │
│  ┌─────────────────────────────────────────────┐    │
│  │        Shared Assets Layer              │    │
│  │ • resume.mcp.json                   │    │
│  │ • rulebook.yaml                     │    │
│  │ • duckdb_local.db                   │    │
│  │ • shortlist.csv / discard.csv          │    │
│  │ • sync_data.sh                      │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 The 5 Projects

### 1️⃣ Resume MCP (Boss Baby grown-up)
**Purpose**: Core intelligence layer that turns your resume into a machine-readable knowledge graph
**Role**: Central "brain" MCP – applies AI reasoning to job-skill matching

**Where to look**: 
- `boss_babyv1/resume_mcp_v2.py` - Main MCP server
- `boss_babyv1/resume.yaml` - Resume data
- `boss_babyv1/unified_mcp.py` - Unified access point

**Key Features**:
- Job ranking with ATS-style scoring
- Semantic matching vs. resume.mcp
- Feedback loop from discard.csv to retrain rulebook.yaml

### 2️⃣ Mocktailverse (AWS ETL)
**Purpose**: Serverless AWS data-engineering pipeline proving backend automation
**Role**: AWS Cloud ETL MCP

**Where to look**:
- `s3_setup.sh` - S3 bucket configuration
- `lambda/transform.py` - Lambda transformation code
- `dynamodb_schema.json` - Database schema
- `etl_log.txt` - Pipeline execution logs

**Tech Stack**: AWS S3, Lambda, DynamoDB, boto3, CLI-first

### 3️⃣ Cocktailverse (GCP ETL)
**Purpose**: GCP mirror of Mocktailverse using Cloud Functions, GCS, and BigQuery
**Role**: GCP Cloud ETL MCP

**Where to look**:
- `gcf/transform.py` - Cloud Function transformation code
- `bq/schema.json` - BigQuery table schema
- `api/test_harness.py` - API testing framework

**Tech Stack**: GCS, Cloud Functions, BigQuery, FastAPI

### 4️⃣ Dynamic Resume (Full-Stack)
**Purpose**: Turns Resume MCP outputs into a live, interactive web resume
**Role**: Frontend visualization MCP

**Where to look**:
- `app/pages/index.js` or `app.py` - Main application
- `components/` - UI components (SkillChart, JobMatchTable, ProjectTimeline)
- `backend/api_sync.py` - Backend synchronization
- `vercel.json` or `Procfile` - Deployment configuration

**Tech Stack**: Next.js/Streamlit, DuckDB, Vercel

### 5️⃣ Marketing Analytics Dashboard (ETL + Visualization)
**Purpose**: Real-world marketing analytics ETL project with KPI computation and visualization
**Role**: Marketing ETL MCP

**Where to look**:
- `data/raw/google_ads.csv` - Google Ads data
- `data/raw/facebook_ads.csv` - Facebook Ads data
- `data/clean/unified_ads.csv` - Cleaned merged data
- `dashboard/app.py` - Streamlit dashboard
- `run_pipeline.sh` - Pipeline execution script

**Tech Stack**: DuckDB, Streamlit, Plotly, Pandas, Requests

## 🔗 Shared Assets (The Glue)

### Core Files
- **`resume.mcp.json`** - Single source of truth for skills and identity
- **`rulebook.yaml`** - Evolving keyword bias logic
- **`duckdb_local.db`** - Central data lake for all projects

### Data Files
- **`shortlist.csv`** - Top ~5 job matches
- **`discard.csv`** - ~95 rejected jobs with feedback
- **`sync_data.sh`** - Bridges projects for daily updates

### Configuration
- **`.env.global`** - Shared credentials (Supabase/AWS/GCP)
- **`README.md`** - Master architecture overview

## 🤖 AI Agent Plan

### Short-term (Light Orchestration)
- **Tools**: Claude Code, Cursor, ChatGPT SDK
- **Scope**: Resume MCP + Dynamic Resume only
- **Focus**: File sync, ranking, summarization

### Long-term (Advanced Orchestration)
- **Tools**: LangChain/LangGraph/CrewAI
- **Target Projects**: [1, 4] - Resume MCP + Dynamic Resume
- **Focus**: Skill evolution tasks

### Reasoning Layers
1. **Skill inference** → Resume MCP
2. **Job enrichment** → Resume MCP  
3. **Front-end sync** → Dynamic Resume
4. **Feedback learning** → rulebook.yaml tuning

## 📍 Where to Find Everything

### GitHub Repository
**Primary Location**: `https://github.com/anix-lynch/boss-baby-mcp`

### Directory Structure
```
boss_babyv1/
├── northstar_5_mcp.yaml      # ← Northstar configuration
├── northstar_mcp.py           # ← Northstar MCP server
├── unified_mcp.py             # ← All-in-one access point
├── resume_mcp_v2.py          # ← Resume intelligence
├── resume.yaml                # ← Resume data
├── certificates_mcp.py          # ← Certificate access
├── certificates.yaml           # ← Certificate data
└── README.md                   # ← Complete documentation
```

### MCP Endpoints (All Accessible via `unified_mcp.py`)

#### Northstar 5 Endpoints
```bash
# Get full Northstar suite
python boss_babyv1/unified_mcp.py --endpoint northstar

# Get all 5 projects
python boss_babyv1/unified_mcp.py --endpoint projects

# Get specific project (1-5)
python boss_babyv1/unified_mcp.py --endpoint project --project-id 1

# Get technology stack summary
python boss_babyv1/unified_mcp.py --endpoint stack

# Search projects by keyword
python boss_babyv1/unified_mcp.py --endpoint northstar-search --query "ETL"

# Get interoperability matrix
python boss_babyv1/unified_mcp.py --endpoint interop
```

#### Resume & Certificate Endpoints
```bash
# Get combined profile
python boss_babyv1/unified_mcp.py --endpoint profile

# Get all certificates
python boss_babyv1/unified_mcp.py --endpoint certificates

# Search across all data
python boss_babyv1/unified_mcp.py --endpoint search --query "Python"
```

## 🎯 End Goal

**Demonstrate a production-grade, end-to-end AI data-engineering ecosystem** that:
- Evolves your resume automatically
- Ranks real jobs intelligently  
- Visualizes live insights dynamically
- Runs locally or in cloud
- Operates under ZeroShot.dev identity

## 💡 Quick Start for GitHub Copilot

1. **"What are the 5 Northstar projects?"**
   - They're Resume MCP, Mocktailverse, Cocktailverse, Dynamic Resume, and Marketing Analytics Dashboard

2. **"Where can I find the project specifications?"**
   - In `boss_babyv1/northstar_5_mcp.yaml` for complete details
   - Access via `python boss_babyv1/unified_mcp.py --endpoint northstar`

3. **"What's the shared architecture?"**
   - All projects share `resume.mcp.json`, `rulebook.yaml`, and `duckdb_local.db`
   - Connected through `sync_data.sh` for daily updates

4. **"How do I access the MCP endpoints?"**
   - Use `boss_babyv1/unified_mcp.py` as the main entry point
   - 15+ endpoints available for all data sources

5. **"What's the brand identity?"**
   - ZeroShot.dev - CLI-first, agent-assisted, cloud-agnostic approach

## 🔮 Future Expansion

### Planned Branches
- `/northstar/archive/` - Frozen older experiments
- `/northstar/mcp_registry.yaml` - Quick tool ingestion summary
- `/northstar/docs/` - Diagrams + Mermaid charts
- `/northstar/.warp/` - Prebuilt CLI workflows
- `/northstar/.cursor/` - Context config for Claude Code

---

**TL;DR**: Northstar 5 is 5 interoperable MCP projects (Resume, AWS ETL, GCP ETL, Full-Stack, Marketing Analytics) that share data through `resume.mcp.json` and `duckdb_local.db`, all accessible via `boss_babyv1/unified_mcp.py` at `https://github.com/anix-lynch/boss-baby-mcp`.