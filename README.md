# Boss Baby MCP

A comprehensive Model Context Protocol (MCP) server that provides access to resume data and certificate information from the github-cert-showcase repository.

## 🚀 Features

### Resume MCP (`resume_mcp_v2.py`)
- Access resume data via `/resume` endpoint
- Job matching functionality with ATS-style scoring via `/match` endpoint
- Skills and experience analysis

### Certificates MCP (`certificates_mcp.py`)
- Access all certificate data via `/certificates` endpoint
- Filter by type: Coursera, diplomas, languages, badges
- Search certificates by keyword, ID, or issuer
- Repository information access

### Northstar 5 MCP (`northstar_mcp.py`)
- Access 5 interoperable MCP projects via `/northstar` endpoint
- Individual project details by ID via `/northstar/project` endpoint
- Project search and filtering capabilities
- Technology stack summary across all projects
- AI agent plan and roadmap information
- Interoperability matrix showing project connections

### Unified MCP (`unified_mcp.py`)
- Combined access to resume, certificates, and Northstar data
- Profile summary with integrated information
- Universal search across all data sources

## 📁 Repository Structure

```
boss_babyv1/
├── __init__.py              # Package initialization
├── resume_mcp_v2.py         # Resume MCP server
├── resume.yaml              # Resume data
├── certificates_mcp.py       # Certificates MCP server
├── certificates.yaml        # Certificate data from github-cert-showcase
└── unified_mcp.py          # Unified MCP server
```

## 🛠️ Installation

1. Install required dependencies:
```bash
pip install PyYAML
```

2. Clone the repository:
```bash
git clone https://github.com/anix-lynch/boss-baby-mcp.git
cd boss-baby-mcp
```

## 📖 Usage

### Resume MCP

```bash
# Get full resume
python boss_babyv1/resume_mcp_v2.py --endpoint resume

# Match job description
python boss_babyv1/resume_mcp_v2.py --endpoint match --job-description "AI Engineer position"
```

### Certificates MCP

```bash
# Get all certificates
python boss_babyv1/certificates_mcp.py --endpoint certificates

# Get Coursera certificates only
python boss_babyv1/certificates_mcp.py --endpoint coursera

# Search certificates
python boss_babyv1/certificates_mcp.py --endpoint search --query "Python"

# Get certificate by ID
python boss_babyv1/certificates_mcp.py --endpoint id --id "9BZ13BA5RR8P"

# Get certificates by issuer
python boss_babyv1/certificates_mcp.py --endpoint issuer --issuer "IBM"
```

### Unified MCP

```bash
# Get combined profile
python boss_babyv1/unified_mcp.py --endpoint profile

# Get all data
python boss_babyv1/unified_mcp.py --endpoint all

# Universal search
python boss_babyv1/unified_mcp.py --endpoint search --query "Machine Learning"

# Get Northstar data via unified MCP
python boss_babyv1/unified_mcp.py --endpoint northstar

# Get Northstar projects via unified MCP
python boss_babyv1/unified_mcp.py --endpoint projects

# Search Northstar projects via unified MCP
python boss_babyv1/unified_mcp.py --endpoint northstar-search --query "AWS"
```

## 📊 Data Sources

### Resume Data
- Personal information and contact details
- Skills and competencies
- Work experience
- Project portfolio

### Certificate Data
- **15 Coursera certificates** from IBM, Meta, and Google
- Academic diplomas (BA and MBA)
- Language certifications (JLPT N1, TOEIC)
- Verified badges from Credly
- Repository information linking to github-cert-showcase

### Northstar 5 Project Data
- **5 interoperable MCP projects** with full specifications
- Project details including purpose, stack, and deliverables
- AI agent orchestration plan with short and long-term goals
- Shared assets and interoperability matrix
- Technology stack summary across all projects

## 🔧 API Endpoints

### Resume Endpoints
- `GET /resume` - Full resume data
- `POST /match` - Job description matching

### Certificate Endpoints
- `GET /certificates` - All certificate data
- `GET /certificates/coursera` - Coursera certificates
- `GET /certificates/diplomas` - Academic diplomas
- `GET /certificates/languages` - Language certifications
- `GET /certificates/badges` - Verified badges
- `GET /certificates/repo` - Repository information
- `POST /certificates/search` - Search certificates
- `POST /certificates/id` - Get certificate by ID
- `POST /certificates/issuer` - Get certificates by issuer

### Unified Endpoints
- `GET /all` - All data from both modules
- `GET /profile` - Combined profile summary
- `POST /search` - Universal search

## 🎯 Integration with github-cert-showcase

This MCP server integrates data from the [github-cert-showcase](https://github.com/anix-lynch/github-cert-showcase) repository, providing programmatic access to:

- Certificate metadata and file paths
- Verification URLs for badges
- Academic achievements
- Language proficiency certifications

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Note**: This MCP server is designed to work with Model Context Protocol clients and can be integrated into AI workflows for accessing professional profile and certification data.