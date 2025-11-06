"""
Boss Baby v1 - Resume MCP System
Provides resume data and job matching capabilities via MCP endpoints
"""

from .resume_mcp_v2 import ResumeMCP, MCPServer

__version__ = "2.0.0"
__author__ = "Anix Lynch"

__all__ = ["ResumeMCP", "MCPServer"]