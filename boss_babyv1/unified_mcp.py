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
    
    def __init__(self, resume_path: str = "resume.yaml", certificates_path: str = "certificates.yaml"):
        self.resume_mcp = ResumeMCP(resume_path)
        self.certificates_mcp = CertificatesMCP(certificates_path)
        logger.info("Unified MCP initialized with resume and certificates modules")
    
    def get_all_data(self) -> Dict[str, Any]:
        """MCP endpoint: /all - returns all available data"""
        logger.info("All data endpoint accessed")
        return {
            "status": "success",
            "data": {
                "resume": self.resume_mcp.resume_data,
                "certificates": self.certificates_mcp.certificates_data
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
            "repository_info": cert_data.get("repository_info", {})
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
        
        all_results = resume_matches + [{"type": r["type"], "data": r["data"]} for r in cert_matches]
        
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
        "badges", "repo", "cert-search", "cert-id", "cert-issuer", "all", "profile", "search"
    ], required=True, help="MCP endpoint to call")
    parser.add_argument("--job-description", help="Job description for matching (required for match endpoint)")
    parser.add_argument("--query", help="Search query (for search endpoints)")
    parser.add_argument("--id", help="Certificate ID (for cert-id endpoint)")
    parser.add_argument("--issuer", help="Issuer name (for cert-issuer endpoint)")
    parser.add_argument("--resume-path", default="resume.yaml", help="Path to resume.yaml file")
    parser.add_argument("--certificates-path", default="certificates.yaml", help="Path to certificates.yaml file")
    
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
        "search": "/search"
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
    
    result = mcp_server.handle_request(endpoint, data if data else None)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()