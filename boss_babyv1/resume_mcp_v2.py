#!/usr/bin/env python3
"""
Resume MCP v2 - Exposes resume data and matching capabilities via MCP endpoints
"""

import json
import yaml
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

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

class ResumeMCP:
    """Resume MCP Server providing resume data and matching capabilities"""
    
    def __init__(self, resume_path: str = "resume.yaml"):
        self.resume_path = Path(resume_path)
        self.resume_data = None
        self.load_resume()
    
    def load_resume(self):
        """Load resume data from YAML file"""
        try:
            if self.resume_path.exists():
                with open(self.resume_path, 'r') as f:
                    self.resume_data = yaml.safe_load(f)
                logger.info(f"Loaded resume from {self.resume_path}")
            else:
                # Create sample resume if none exists
                self.create_sample_resume()
                logger.info(f"Created sample resume at {self.resume_path}")
        except Exception as e:
            logger.error(f"Error loading resume: {e}")
            self.resume_data = {}
    
    def create_sample_resume(self):
        """Create a sample resume.yaml for testing"""
        sample_resume = {
            "personal_info": {
                "name": "Anix Lynch",
                "title": "AI Engineer & Data Scientist",
                "email": "anix@example.com",
                "linkedin": "linkedin.com/in/anixlynch",
                "github": "github.com/anix-lynch"
            },
            "summary": "AI Engineer specializing in machine learning pipelines, data engineering, and automation systems.",
            "skills": [
                "Python", "Machine Learning", "Data Engineering", 
                "ETL", "Open Source", "AI", "Marketing", "Dashboard",
                "APIs", "Automation", "Cloud Computing"
            ],
            "experience": [
                {
                    "title": "AI Engineer",
                    "company": "Tech Company",
                    "duration": "2022-Present",
                    "description": "Built ML pipelines and automated data systems"
                }
            ],
            "projects": [
                {
                    "name": "AI Agent System",
                    "tech": ["Python", "ML", "APIs"],
                    "description": "Automated decision-making system"
                }
            ]
        }
        
        with open(self.resume_path, 'w') as f:
            yaml.dump(sample_resume, f, default_flow_style=False)
        
        self.resume_data = sample_resume
    
    def get_resume(self) -> Dict[str, Any]:
        """MCP endpoint: /resume - returns full resume data"""
        logger.info("Resume endpoint accessed")
        return {
            "status": "success",
            "data": self.resume_data,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_match_score(self, job_description: str) -> Dict[str, Any]:
        """MCP endpoint: /match - returns ATS-style match score"""
        logger.info(f"Match endpoint accessed for job: {job_description[:100]}...")
        
        if not self.resume_data:
            return {"status": "error", "message": "No resume data available"}
        
        # Extract keywords from resume
        resume_text = json.dumps(self.resume_data).lower()
        resume_skills = self.resume_data.get("skills", [])
        
        # Positive and negative keyword lists
        positive_keywords = ["open source", "etl", "ai", "marketing", "dashboard", "python", "machine learning"]
        negative_keywords = ["enterprise", "terraform", "snowflake", "legacy"]
        
        job_text = job_description.lower()
        
        # Calculate positive score
        positive_score = 0
        for keyword in positive_keywords:
            if keyword in job_text:
                positive_score += 1
        
        # Calculate negative score
        negative_score = 0
        for keyword in negative_keywords:
            if keyword in job_text:
                negative_score += 1
        
        # Skill matching
        skill_matches = 0
        for skill in resume_skills:
            if skill.lower() in job_text:
                skill_matches += 1
        
        skill_match_percentage = (skill_matches / len(resume_skills)) * 100 if resume_skills else 0
        
        # Overall score calculation
        base_score = skill_match_percentage
        positive_bonus = positive_score * 10
        negative_penalty = negative_score * 15
        
        final_score = min(100, max(0, base_score + positive_bonus - negative_penalty))
        
        result = {
            "status": "success",
            "match_score": round(final_score, 2),
            "skill_match_percentage": round(skill_match_percentage, 2),
            "positive_keywords_found": positive_score,
            "negative_keywords_found": negative_score,
            "skills_matched": skill_matches,
            "total_skills": len(resume_skills),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Match score calculated: {final_score:.2f}")
        return result

# MCP Server simulation
class MCPServer:
    """Simple MCP server simulation"""
    
    def __init__(self):
        self.resume_mcp = ResumeMCP()
    
    def handle_request(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle MCP requests"""
        if endpoint == "/resume":
            return self.resume_mcp.get_resume()
        elif endpoint == "/match":
            if not data or "job_description" not in data:
                return {"status": "error", "message": "job_description required"}
            return self.resume_mcp.get_match_score(data["job_description"])
        else:
            return {"status": "error", "message": "Unknown endpoint"}

# CLI interface for testing
def main():
    """CLI interface for testing MCP endpoints"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Resume MCP v2 Server")
    parser.add_argument("--endpoint", choices=["resume", "match"], required=True, help="MCP endpoint to call")
    parser.add_argument("--job-description", help="Job description for matching (required for match endpoint)")
    parser.add_argument("--resume-path", default="resume.yaml", help="Path to resume.yaml file")
    
    args = parser.parse_args()
    
    # Initialize MCP server
    mcp_server = MCPServer()
    
    if args.endpoint == "resume":
        result = mcp_server.handle_request("/resume")
        print(json.dumps(result, indent=2))
    
    elif args.endpoint == "match":
        if not args.job_description:
            print("Error: --job-description required for match endpoint")
            return
        
        result = mcp_server.handle_request("/match", {"job_description": args.job_description})
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()