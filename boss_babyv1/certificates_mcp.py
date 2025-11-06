#!/usr/bin/env python3
"""
Certificates MCP - Exposes certificate and badge data via MCP endpoints
"""

import json
import yaml
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

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

class CertificatesMCP:
    """Certificates MCP Server providing certificate data and search capabilities"""
    
    def __init__(self, certificates_path: str = "certificates.yaml"):
        self.certificates_path = Path(certificates_path)
        self.certificates_data = None
        self.load_certificates()
    
    def load_certificates(self):
        """Load certificates data from YAML file"""
        try:
            if self.certificates_path.exists():
                with open(self.certificates_path, 'r') as f:
                    self.certificates_data = yaml.safe_load(f)
                logger.info(f"Loaded certificates from {self.certificates_path}")
            else:
                logger.error(f"Certificates file not found at {self.certificates_path}")
                self.certificates_data = {}
        except Exception as e:
            logger.error(f"Error loading certificates: {e}")
            self.certificates_data = {}
    
    def get_all_certificates(self) -> Dict[str, Any]:
        """MCP endpoint: /certificates - returns all certificate data"""
        logger.info("Certificates endpoint accessed")
        return {
            "status": "success",
            "data": self.certificates_data,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_coursera_certificates(self) -> Dict[str, Any]:
        """MCP endpoint: /certificates/coursera - returns Coursera certificates"""
        logger.info("Coursera certificates endpoint accessed")
        coursera_certs = self.certificates_data.get("certificates", {}).get("coursera", [])
        return {
            "status": "success",
            "data": coursera_certs,
            "count": len(coursera_certs),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_diplomas(self) -> Dict[str, Any]:
        """MCP endpoint: /certificates/diplomas - returns diploma information"""
        logger.info("Diplomas endpoint accessed")
        diplomas = self.certificates_data.get("diplomas", [])
        return {
            "status": "success",
            "data": diplomas,
            "count": len(diplomas),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_language_certificates(self) -> Dict[str, Any]:
        """MCP endpoint: /certificates/languages - returns language certificates"""
        logger.info("Language certificates endpoint accessed")
        languages = self.certificates_data.get("languages", [])
        return {
            "status": "success",
            "data": languages,
            "count": len(languages),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_badges(self) -> Dict[str, Any]:
        """MCP endpoint: /certificates/badges - returns verified badges"""
        logger.info("Badges endpoint accessed")
        badges = self.certificates_data.get("badges", [])
        return {
            "status": "success",
            "data": badges,
            "count": len(badges),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_repository_info(self) -> Dict[str, Any]:
        """MCP endpoint: /certificates/repo - returns repository information"""
        logger.info("Repository info endpoint accessed")
        repo_info = self.certificates_data.get("repository_info", {})
        return {
            "status": "success",
            "data": repo_info,
            "timestamp": datetime.now().isoformat()
        }
    
    def search_certificates(self, query: str) -> Dict[str, Any]:
        """MCP endpoint: /certificates/search - search certificates by keyword"""
        logger.info(f"Search endpoint accessed with query: {query}")
        
        if not self.certificates_data:
            return {"status": "error", "message": "No certificate data available"}
        
        query_lower = query.lower()
        results = []
        
        # Search in Coursera certificates
        for cert in self.certificates_data.get("certificates", {}).get("coursera", []):
            if (query_lower in cert.get("title", "").lower() or 
                query_lower in cert.get("issuer", "").lower() or
                query_lower in cert.get("id", "").lower()):
                results.append({"type": "coursera", "data": cert})
        
        # Search in other certificates
        for cert in self.certificates_data.get("certificates", {}).get("other", []):
            if (query_lower in cert.get("title", "").lower() or 
                query_lower in cert.get("issuer", "").lower()):
                results.append({"type": "other", "data": cert})
        
        # Search in diplomas
        for diploma in self.certificates_data.get("diplomas", []):
            if query_lower in diploma.get("title", "").lower():
                results.append({"type": "diploma", "data": diploma})
        
        # Search in language certificates
        for lang in self.certificates_data.get("languages", []):
            if (query_lower in lang.get("title", "").lower() or 
                query_lower in lang.get("language", "").lower()):
                results.append({"type": "language", "data": lang})
        
        # Search in badges
        for badge in self.certificates_data.get("badges", []):
            if (query_lower in badge.get("title", "").lower() or 
                query_lower in badge.get("issuer", "").lower()):
                results.append({"type": "badge", "data": badge})
        
        return {
            "status": "success",
            "query": query,
            "results": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_certificate_by_id(self, cert_id: str) -> Dict[str, Any]:
        """MCP endpoint: /certificates/id - get certificate by ID"""
        logger.info(f"Get by ID endpoint accessed with ID: {cert_id}")
        
        # Search in Coursera certificates by ID
        for cert in self.certificates_data.get("certificates", {}).get("coursera", []):
            if cert.get("id") == cert_id:
                return {
                    "status": "success",
                    "data": {"type": "coursera", "certificate": cert},
                    "timestamp": datetime.now().isoformat()
                }
        
        return {
            "status": "error",
            "message": f"Certificate with ID {cert_id} not found",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_certificates_by_issuer(self, issuer: str) -> Dict[str, Any]:
        """MCP endpoint: /certificates/issuer - get certificates by issuer"""
        logger.info(f"Get by issuer endpoint accessed with issuer: {issuer}")
        
        issuer_lower = issuer.lower()
        results = []
        
        # Search in Coursera certificates
        for cert in self.certificates_data.get("certificates", {}).get("coursera", []):
            if issuer_lower in cert.get("issuer", "").lower():
                results.append({"type": "coursera", "data": cert})
        
        # Search in other certificates
        for cert in self.certificates_data.get("certificates", {}).get("other", []):
            if issuer_lower in cert.get("issuer", "").lower():
                results.append({"type": "other", "data": cert})
        
        # Search in badges
        for badge in self.certificates_data.get("badges", []):
            if issuer_lower in badge.get("issuer", "").lower():
                results.append({"type": "badge", "data": badge})
        
        return {
            "status": "success",
            "issuer": issuer,
            "results": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        }

# MCP Server simulation
class MCPServer:
    """Simple MCP server simulation for certificates"""
    
    def __init__(self):
        self.certificates_mcp = CertificatesMCP()
    
    def handle_request(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle MCP requests"""
        if endpoint == "/certificates":
            return self.certificates_mcp.get_all_certificates()
        elif endpoint == "/certificates/coursera":
            return self.certificates_mcp.get_coursera_certificates()
        elif endpoint == "/certificates/diplomas":
            return self.certificates_mcp.get_diplomas()
        elif endpoint == "/certificates/languages":
            return self.certificates_mcp.get_language_certificates()
        elif endpoint == "/certificates/badges":
            return self.certificates_mcp.get_badges()
        elif endpoint == "/certificates/repo":
            return self.certificates_mcp.get_repository_info()
        elif endpoint == "/certificates/search":
            if not data or "query" not in data:
                return {"status": "error", "message": "query required"}
            return self.certificates_mcp.search_certificates(data["query"])
        elif endpoint == "/certificates/id":
            if not data or "id" not in data:
                return {"status": "error", "message": "id required"}
            return self.certificates_mcp.get_certificate_by_id(data["id"])
        elif endpoint == "/certificates/issuer":
            if not data or "issuer" not in data:
                return {"status": "error", "message": "issuer required"}
            return self.certificates_mcp.get_certificates_by_issuer(data["issuer"])
        else:
            return {"status": "error", "message": "Unknown endpoint"}

# CLI interface for testing
def main():
    """CLI interface for testing MCP endpoints"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Certificates MCP Server")
    parser.add_argument("--endpoint", choices=[
        "certificates", "coursera", "diplomas", "languages", "badges", "repo", "search", "id", "issuer"
    ], required=True, help="MCP endpoint to call")
    parser.add_argument("--query", help="Search query (for search endpoint)")
    parser.add_argument("--id", help="Certificate ID (for id endpoint)")
    parser.add_argument("--issuer", help="Issuer name (for issuer endpoint)")
    parser.add_argument("--certificates-path", default="certificates.yaml", help="Path to certificates.yaml file")
    
    args = parser.parse_args()
    
    # Initialize MCP server
    mcp_server = MCPServer()
    
    # Map endpoint names to API endpoints
    endpoint_map = {
        "certificates": "/certificates",
        "coursera": "/certificates/coursera",
        "diplomas": "/certificates/diplomas",
        "languages": "/certificates/languages",
        "badges": "/certificates/badges",
        "repo": "/certificates/repo",
        "search": "/certificates/search",
        "id": "/certificates/id",
        "issuer": "/certificates/issuer"
    }
    
    endpoint = endpoint_map[args.endpoint]
    data = {}
    
    if args.endpoint == "search" and args.query:
        data["query"] = args.query
    elif args.endpoint == "id" and args.id:
        data["id"] = args.id
    elif args.endpoint == "issuer" and args.issuer:
        data["issuer"] = args.issuer
    
    result = mcp_server.handle_request(endpoint, data if data else None)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()