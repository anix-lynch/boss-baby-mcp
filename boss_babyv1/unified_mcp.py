#!/usr/bin/env python3
"""
Unified MCP - Exposes both resume and certificate data via MCP endpoints
"""

import json
import yaml
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Import the existing MCP modules
from resume_mcp_v2 import ResumeMCP
from certificates_mcp import CertificatesMCP
from northstar_mcp import NorthstarMCP

# Setup logging
def setup_logging():
    """Setup logging to Monica logs directory"""
    log_dir = Path.home() / "Monica" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "ai_actions.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class UnifiedMCP:
    """Unified MCP Server providing both resume and certificate data"""
    
    def __init__(self, resume_path: str = "resume.yaml", certificates_path: str = "certificates.yaml", northstar_path: str = "northstar_5_mcp.yaml"):
        self.resume_mcp = ResumeMCP(resume_path)
        self.certificates_mcp = CertificatesMCP(certificates_path)
        self.northstar_mcp = NorthstarMCP(northstar_path)
        logger.info("Unified MCP initialized with resume, certificates, and northstar modules")
    
    def get_all_data(self) -> Dict[str, Any]:
        """MCP endpoint: /all - returns all available data"""
        logger.info("All data endpoint accessed")
        return {
            "status": "success",
            "data": {
                "resume": self.resume_mcp.resume_data,
                "certificates": self.certificates_mcp.certificates_data,
                "northstar": self.northstar_mcp.northstar_data
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def get_profile_summary(self) -> Dict[str, Any]:
        """MCP endpoint: /profile - returns a combined profile summary"""
        logger.info("Profile summary endpoint accessed")
        
        # Extract key information from resume
        resume_data = self.resume_mcp.resume_data or {}
        personal_info = resume_data.get("personal_info", {})
        skills = resume_data.get("skills", [])
        experience = resume_data.get("experience", [])
        projects = resume_data.get("projects", [])
        
        # Extract key information from certificates
        cert_data = self.certificates_mcp.certificates_data or {}
        coursera_certs = cert_data.get("certificates", {}).get("coursera", [])
        diplomas = cert_data.get("diplomas", [])
        languages = cert_data.get("languages", [])
        badges = cert_data.get("badges", [])
        
        # Extract key information from Northstar
        northstar_data = self.northstar_mcp.northstar_data or {}
        northstar_suite = northstar_data.get("northstar_suite", {})
        projects = northstar_suite.get("projects", [])
        shared_assets = northstar_suite.get("shared_assets", [])
        
        # Count certificates by issuer
        issuer_counts = {}
        for cert in coursera_certs:
            issuer = cert.get("issuer", "Unknown")
            issuer_counts[issuer] = issuer_counts.get(issuer, 0) + 1
        
        # Get unique skills from certificates
        cert_skills = set()
        for cert in coursera_certs:
            title = cert.get("title", "").lower()
            if "python" in title:
                cert_skills.add("Python")
            if "machine learning" in title or "ml" in title:
                cert_skills.add("Machine Learning")
            if "data" in title:
                cert_skills.add("Data Analysis")
            if "sql" in title:
                cert_skills.add("SQL")
            if "ai" in title or "genai" in title:
                cert_skills.add("AI/GenAI")
        
        # Combine skills
        all_skills = list(set(skills + list(cert_skills)))
        
        profile_summary = {
            "personal_info": personal_info,
            "summary": resume_data.get("summary", ""),
            "skills": all_skills,
            "experience_count": len(experience),
            "project_count": len(projects),
            "education": {
                "diplomas": diplomas,
                "language_certificates": languages
            },
            "certifications": {
                "coursera_count": len(coursera_certs),
                "issuers": issuer_counts,
                "badges": badges
            },
            "repository_info": cert_data.get("repository_info", {}),
            "northstar_suite": {
                "brand": northstar_suite.get("brand"),
                "total_projects": northstar_suite.get("total_projects"),
                "mission": northstar_suite.get("mission"),
                "projects_count": len(projects),
                "shared_assets_count": len(shared_assets),
                "projects": [{"id": p.get("id"), "name": p.get("name"), "mcp_role": p.get("mcp_role")} for p in projects]
            }
        }
        
        return {
            "status": "success",
            "data": profile_summary,
            "timestamp": datetime.now().isoformat()
        }
    
    def search_all(self, query: str) -> Dict[str, Any]:
        """MCP endpoint: /search - search across both resume and certificates"""
        logger.info(f"Universal search endpoint accessed with query: {query}")
        
        # Search in resume
        resume_text = json.dumps(self.resume_mcp.resume_data).lower()
        resume_matches = []
        if query.lower() in resume_text:
            resume_matches.append({"type": "resume", "matched": True})
        
        # Search in certificates
        cert_results = self.certificates_mcp.search_certificates(query)
        cert_matches = cert_results.get("results", [])
        
        # Search in Northstar projects
        northstar_results = self.northstar_mcp.search_projects(query)
        northstar_matches = northstar_results.get("results", [])
        
        all_results = (
            resume_matches +
            [{"type": r["type"], "data": r["data"]} for r in cert_matches] +
            [{"type": "northstar", "data": project} for project in northstar_matches]
        )
        
        return {
            "status": "success",
            "query": query,
            "results": all_results,
            "count": len(all_results),
            "timestamp": datetime.now().isoformat()
        }

# Unified MCP Server
class UnifiedMCPServer:
    """Unified MCP Server handling both resume and certificates endpoints"""
    
    def __init__(self):
        self.unified_mcp = UnifiedMCP()
        logger.info("Unified MCP Server initialized")
    
    def handle_request(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle MCP requests for both resume and certificates"""
        
        # Resume endpoints
        if endpoint == "/resume":
            return self.unified_mcp.resume_mcp.get_resume()
        elif endpoint == "/match":
            if not data or "job_description" not in data:
                return {"status": "error", "message": "job_description required"}
            return self.unified_mcp.resume_mcp.get_match_score(data["job_description"])
        
        # Certificate endpoints
        elif endpoint == "/certificates":
            return self.unified_mcp.certificates_mcp.get_all_certificates()
        elif endpoint == "/certificates/coursera":
            return self.unified_mcp.certificates_mcp.get_coursera_certificates()
        elif endpoint == "/certificates/diplomas":
            return self.unified_mcp.certificates_mcp.get_diplomas()
        elif endpoint == "/certificates/languages":
            return self.unified_mcp.certificates_mcp.get_language_certificates()
        elif endpoint == "/certificates/badges":
            return self.unified_mcp.certificates_mcp.get_badges()
        elif endpoint == "/certificates/repo":
            return self.unified_mcp.certificates_mcp.get_repository_info()
        elif endpoint == "/certificates/search":
            if not data or "query" not in data:
                return {"status": "error", "message": "query required"}
            return self.unified_mcp.certificates_mcp.search_certificates(data["query"])
        elif endpoint == "/certificates/id":
            if not data or "id" not in data:
                return {"status": "error", "message": "id required"}
            return self.unified_mcp.certificates_mcp.get_certificate_by_id(data["id"])
        elif endpoint == "/certificates/issuer":
            if not data or "issuer" not in data:
                return {"status": "error", "message": "issuer required"}
            return self.unified_mcp.certificates_mcp.get_certificates_by_issuer(data["issuer"])
        
        # Northstar endpoints
        elif endpoint == "/northstar":
            return self.unified_mcp.northstar_mcp.get_northstar_suite()
        elif endpoint == "/northstar/projects":
            return self.unified_mcp.northstar_mcp.get_projects()
        elif endpoint == "/northstar/project":
            if not data or "id" not in data:
                return {"status": "error", "message": "project id required"}
            return self.unified_mcp.northstar_mcp.get_project_by_id(int(data["id"]))
        elif endpoint == "/northstar/assets":
            return self.unified_mcp.northstar_mcp.get_shared_assets()
        elif endpoint == "/northstar/ai-plan":
            return self.unified_mcp.northstar_mcp.get_ai_agent_plan()
        elif endpoint == "/northstar/stack":
            return self.unified_mcp.northstar_mcp.get_stack_summary()
        elif endpoint == "/northstar/roadmap":
            return self.unified_mcp.northstar_mcp.get_project_roadmap()
        elif endpoint == "/northstar/search":
            if not data or "query" not in data:
                return {"status": "error", "message": "query required"}
            return self.unified_mcp.northstar_mcp.search_projects(data["query"])
        elif endpoint == "/northstar/interop":
            return self.unified_mcp.northstar_mcp.get_interop_matrix()
        
        # Unified endpoints
        elif endpoint == "/all":
            return self.unified_mcp.get_all_data()
        elif endpoint == "/profile":
            return self.unified_mcp.get_profile_summary()
        elif endpoint == "/search":
            if not data or "query" not in data:
                return {"status": "error", "message": "query required"}
            return self.unified_mcp.search_all(data["query"])
        
        else:
            return {"status": "error", "message": "Unknown endpoint"}

# CLI interface for testing
def main():
    """CLI interface for testing unified MCP endpoints"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified MCP Server")
    parser.add_argument("--endpoint", choices=[
        "resume", "match", "certificates", "coursera", "diplomas", "languages",
        "badges", "repo", "cert-search", "cert-id", "cert-issuer", "all", "profile", "search",
        "northstar", "projects", "project", "assets", "ai-plan", "stack", "roadmap", "northstar-search", "interop"
    ], required=True, help="MCP endpoint to call")
    parser.add_argument("--job-description", help="Job description for matching (required for match endpoint)")
    parser.add_argument("--query", help="Search query (for search endpoints)")
    parser.add_argument("--id", help="Certificate ID (for cert-id endpoint)")
    parser.add_argument("--issuer", help="Issuer name (for cert-issuer endpoint)")
    parser.add_argument("--project-id", type=int, help="Project ID (for project endpoint)")
    parser.add_argument("--resume-path", default="resume.yaml", help="Path to resume.yaml file")
    parser.add_argument("--certificates-path", default="certificates.yaml", help="Path to certificates.yaml file")
    parser.add_argument("--northstar-path", default="northstar_5_mcp.yaml", help="Path to northstar_5_mcp.yaml file")
    
    args = parser.parse_args()
    
    # Initialize unified MCP server
    mcp_server = UnifiedMCPServer()
    
    # Map endpoint names to API endpoints
    endpoint_map = {
        "resume": "/resume",
        "match": "/match",
        "certificates": "/certificates",
        "coursera": "/certificates/coursera",
        "diplomas": "/certificates/diplomas",
        "languages": "/certificates/languages",
        "badges": "/certificates/badges",
        "repo": "/certificates/repo",
        "cert-search": "/certificates/search",
        "cert-id": "/certificates/id",
        "cert-issuer": "/certificates/issuer",
        "all": "/all",
        "profile": "/profile",
        "search": "/search",
        "northstar": "/northstar",
        "projects": "/northstar/projects",
        "project": "/northstar/project",
        "assets": "/northstar/assets",
        "ai-plan": "/northstar/ai-plan",
        "stack": "/northstar/stack",
        "roadmap": "/northstar/roadmap",
        "northstar-search": "/northstar/search",
        "interop": "/northstar/interop"
    }
    
    endpoint = endpoint_map[args.endpoint]
    data = {}
    
    if args.endpoint == "match" and args.job_description:
        data["job_description"] = args.job_description
    elif args.endpoint in ["cert-search", "search"] and args.query:
        data["query"] = args.query
    elif args.endpoint == "cert-id" and args.id:
        data["id"] = args.id
    elif args.endpoint == "cert-issuer" and args.issuer:
        data["issuer"] = args.issuer
    elif args.endpoint == "project" and args.project_id is not None:
        data["id"] = args.project_id
    elif args.endpoint in ["northstar-search", "search"] and args.query:
        data["query"] = args.query
    
    result = mcp_server.handle_request(endpoint, data if data else None)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()