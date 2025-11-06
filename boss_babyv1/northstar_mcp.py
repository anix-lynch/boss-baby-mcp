#!/usr/bin/env python3
"""
Northstar 5 MCP - Exposes Northstar project suite data via MCP endpoints
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

class NorthstarMCP:
    """Northstar 5 MCP Server providing project suite data and management capabilities"""
    
    def __init__(self, northstar_path: str = "northstar_5_mcp.yaml"):
        self.northstar_path = Path(northstar_path)
        self.northstar_data = None
        self.load_northstar()
    
    def load_northstar(self):
        """Load Northstar data from YAML file"""
        try:
            if self.northstar_path.exists():
                with open(self.northstar_path, 'r') as f:
                    self.northstar_data = yaml.safe_load(f)
                logger.info(f"Loaded Northstar suite from {self.northstar_path}")
            else:
                logger.error(f"Northstar file not found at {self.northstar_path}")
                self.northstar_data = {}
        except Exception as e:
            logger.error(f"Error loading Northstar data: {e}")
            self.northstar_data = {}
    
    def get_northstar_suite(self) -> Dict[str, Any]:
        """MCP endpoint: /northstar - returns full Northstar suite data"""
        logger.info("Northstar suite endpoint accessed")
        return {
            "status": "success",
            "data": self.northstar_data,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_projects(self) -> Dict[str, Any]:
        """MCP endpoint: /northstar/projects - returns all projects"""
        logger.info("Northstar projects endpoint accessed")
        projects = self.northstar_data.get("northstar_suite", {}).get("projects", [])
        return {
            "status": "success",
            "data": projects,
            "count": len(projects),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_project_by_id(self, project_id: int) -> Dict[str, Any]:
        """MCP endpoint: /northstar/project - get specific project by ID"""
        logger.info(f"Northstar project endpoint accessed for ID: {project_id}")
        
        projects = self.northstar_data.get("northstar_suite", {}).get("projects", [])
        
        for project in projects:
            if project.get("id") == project_id:
                return {
                    "status": "success",
                    "data": project,
                    "timestamp": datetime.now().isoformat()
                }
        
        return {
            "status": "error",
            "message": f"Project with ID {project_id} not found",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_shared_assets(self) -> Dict[str, Any]:
        """MCP endpoint: /northstar/assets - returns shared assets"""
        logger.info("Northstar shared assets endpoint accessed")
        assets = self.northstar_data.get("northstar_suite", {}).get("shared_assets", [])
        return {
            "status": "success",
            "data": assets,
            "count": len(assets),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_ai_agent_plan(self) -> Dict[str, Any]:
        """MCP endpoint: /northstar/ai-plan - returns AI agent plan"""
        logger.info("Northstar AI agent plan endpoint accessed")
        ai_plan = self.northstar_data.get("northstar_suite", {}).get("ai_agent_plan", [])
        return {
            "status": "success",
            "data": ai_plan,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_stack_summary(self) -> Dict[str, Any]:
        """MCP endpoint: /northstar/stack - returns technology stack summary"""
        logger.info("Northstar stack summary endpoint accessed")
        
        projects = self.northstar_data.get("northstar_suite", {}).get("projects", [])
        stack_summary = {}
        
        for project in projects:
            project_id = project.get("id")
            stack = project.get("stack", [])
            stack_summary[f"project_{project_id}"] = {
                "name": project.get("name"),
                "stack": stack,
                "mcp_role": project.get("mcp_role")
            }
        
        # Get unique technologies across all projects
        all_techs = set()
        for stack_info in stack_summary.values():
            all_techs.update(stack_info.get("stack", []))
        
        return {
            "status": "success",
            "data": {
                "by_project": stack_summary,
                "unique_technologies": sorted(list(all_techs)),
                "total_projects": len(projects)
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def get_project_roadmap(self) -> Dict[str, Any]:
        """MCP endpoint: /northstar/roadmap - returns project roadmap"""
        logger.info("Northstar roadmap endpoint accessed")
        
        projects = self.northstar_data.get("northstar_suite", {}).get("projects", [])
        roadmap = []
        
        for project in projects:
            roadmap.append({
                "id": project.get("id"),
                "name": project.get("name"),
                "purpose": project.get("purpose"),
                "mcp_role": project.get("mcp_role"),
                "stack": project.get("stack"),
                "deliverables": project.get("deliverables", []),
                "stretch_goals": project.get("stretch", [])
            })
        
        return {
            "status": "success",
            "data": roadmap,
            "timestamp": datetime.now().isoformat()
        }
    
    def search_projects(self, query: str) -> Dict[str, Any]:
        """MCP endpoint: /northstar/search - search projects by keyword"""
        logger.info(f"Northstar search endpoint accessed with query: {query}")
        
        if not self.northstar_data:
            return {"status": "error", "message": "No Northstar data available"}
        
        query_lower = query.lower()
        projects = self.northstar_data.get("northstar_suite", {}).get("projects", [])
        results = []
        
        for project in projects:
            # Search in name, purpose, stack, and mcp_role
            searchable_text = " ".join([
                project.get("name", ""),
                project.get("purpose", ""),
                " ".join(project.get("stack", [])),
                project.get("mcp_role", "")
            ]).lower()
            
            if query_lower in searchable_text:
                # Calculate relevance score
                score = 0
                if query_lower in project.get("name", "").lower():
                    score += 10
                if query_lower in project.get("purpose", "").lower():
                    score += 5
                if any(query_lower in tech.lower() for tech in project.get("stack", [])):
                    score += 3
                if query_lower in project.get("mcp_role", "").lower():
                    score += 7
                
                results.append({
                    "project": project,
                    "relevance_score": score
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return {
            "status": "success",
            "query": query,
            "results": [r["project"] for r in results],
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_interop_matrix(self) -> Dict[str, Any]:
        """MCP endpoint: /northstar/interop - returns interoperability matrix"""
        logger.info("Northstar interoperability endpoint accessed")
        
        projects = self.northstar_data.get("northstar_suite", {}).get("projects", [])
        shared_assets = self.northstar_data.get("northstar_suite", {}).get("shared_assets", [])
        
        # Build interoperability matrix
        interop_matrix = {}
        for i, project1 in enumerate(projects):
            for j, project2 in enumerate(projects):
                if i <= j:  # Only upper triangle
                    key = f"{project1.get('id')}-{project2.get('id')}"
                    interop_matrix[key] = {
                        "project1": project1.get("name"),
                        "project2": project2.get("name"),
                        "shared_assets": shared_assets,
                        "connection_type": "direct" if i == j else "via_shared_assets"
                    }
        
        return {
            "status": "success",
            "data": {
                "matrix": interop_matrix,
                "shared_assets": shared_assets,
                "total_connections": len(interop_matrix)
            },
            "timestamp": datetime.now().isoformat()
        }

# MCP Server simulation
class MCPServer:
    """Simple MCP server simulation for Northstar"""
    
    def __init__(self):
        self.northstar_mcp = NorthstarMCP()
    
    def handle_request(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle MCP requests"""
        if endpoint == "/northstar":
            return self.northstar_mcp.get_northstar_suite()
        elif endpoint == "/northstar/projects":
            return self.northstar_mcp.get_projects()
        elif endpoint == "/northstar/project":
            if not data or "id" not in data:
                return {"status": "error", "message": "project id required"}
            return self.northstar_mcp.get_project_by_id(int(data["id"]))
        elif endpoint == "/northstar/assets":
            return self.northstar_mcp.get_shared_assets()
        elif endpoint == "/northstar/ai-plan":
            return self.northstar_mcp.get_ai_agent_plan()
        elif endpoint == "/northstar/stack":
            return self.northstar_mcp.get_stack_summary()
        elif endpoint == "/northstar/roadmap":
            return self.northstar_mcp.get_project_roadmap()
        elif endpoint == "/northstar/search":
            if not data or "query" not in data:
                return {"status": "error", "message": "query required"}
            return self.northstar_mcp.search_projects(data["query"])
        elif endpoint == "/northstar/interop":
            return self.northstar_mcp.get_interop_matrix()
        else:
            return {"status": "error", "message": "Unknown endpoint"}

# CLI interface for testing
def main():
    """CLI interface for testing MCP endpoints"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Northstar 5 MCP Server")
    parser.add_argument("--endpoint", choices=[
        "northstar", "projects", "project", "assets", "ai-plan", "stack", "roadmap", "search", "interop"
    ], required=True, help="MCP endpoint to call")
    parser.add_argument("--id", type=int, help="Project ID (for project endpoint)")
    parser.add_argument("--query", help="Search query (for search endpoint)")
    parser.add_argument("--northstar-path", default="northstar_5_mcp.yaml", help="Path to northstar_5_mcp.yaml file")
    
    args = parser.parse_args()
    
    # Initialize MCP server
    mcp_server = MCPServer()
    
    # Map endpoint names to API endpoints
    endpoint_map = {
        "northstar": "/northstar",
        "projects": "/northstar/projects",
        "project": "/northstar/project",
        "assets": "/northstar/assets",
        "ai-plan": "/northstar/ai-plan",
        "stack": "/northstar/stack",
        "roadmap": "/northstar/roadmap",
        "search": "/northstar/search",
        "interop": "/northstar/interop"
    }
    
    endpoint = endpoint_map[args.endpoint]
    data = {}
    
    if args.endpoint == "project" and args.id is not None:
        data["id"] = args.id
    elif args.endpoint == "search" and args.query:
        data["query"] = args.query
    
    result = mcp_server.handle_request(endpoint, data if data else None)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()