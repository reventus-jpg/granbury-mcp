"""Granbury LTC Manual — MCP server (easiest shareable version).

Run it on a public HTTPS host, then send people this link:
    https://your-api-domain.com/mcp

Recipients add it in ChatGPT as:
    Plugins -> Add -> Add custom MCP server
    Name: Granbury LTC Manual
    Server URL: https://your-api-domain.com/mcp
    Authentication: No authentication

The server listens at /mcp when run with the streamable-http transport.
Set FASTMCP_HOST=0.0.0.0 and FASTMCP_PORT to your host's port.
"""
import json

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("granbury-ltc-manual", stateless_http=True, json_response=True)

SECTIONS = [
    {"id": "governance", "title": "Governance and Administrator Responsibilities",
     "keywords": ["governing body", "administrator", "oversight", "accountability"],
     "summary": "Who governs the facility, what the administrator is accountable for, and how decisions and oversight are documented."},
    {"id": "licensing", "title": "Licensing, Regulations, and Survey Readiness",
     "keywords": ["HHSC", "CMS", "survey", "plan of correction", "F-tags", "Texas"],
     "summary": "Texas HHSC long-term care regulation, federal CMS requirements, survey preparation, and plans of correction."},
    {"id": "staffing", "title": "Staffing and Organizational Structure",
     "keywords": ["staffing ratios", "DON", "scheduling", "coverage"],
     "summary": "Organizational chart, nursing leadership, staffing, and coverage for a Granbury, Hood County facility."},
    {"id": "admissions", "title": "Admissions, Assessment, and Care Planning",
     "keywords": ["MDS", "care plan", "admission", "interdisciplinary team"],
     "summary": "Admission criteria, resident assessment, MDS, and interdisciplinary care planning."},
    {"id": "infection-control", "title": "Infection Prevention and Control",
     "keywords": ["hand hygiene", "PPE", "isolation", "outbreak"],
     "summary": "Hand hygiene, PPE, isolation precautions, surveillance, and outbreak response."},
    {"id": "emergency", "title": "Safety and Emergency Preparedness",
     "keywords": ["tornado", "heat", "flooding", "winter ice", "emergency plan", "Hood County"],
     "summary": "Hood County emergency coordination, including tornadoes, heat, flooding, and winter ice."},
    {"id": "qapi", "title": "Quality Assurance and Performance Improvement",
     "keywords": ["QAPI", "quality indicators", "audits", "root cause"],
     "summary": "Quality indicators, audits, root-cause analysis, and continuous improvement."},
    {"id": "resident-rights", "title": "Resident Rights and Family Engagement",
     "keywords": ["resident rights", "privacy", "grievances", "advance directives"],
     "summary": "Resident rights, dignity, privacy, grievances, advance directives, and family communication."},
]


@mcp.tool()
def search_manual(q: str) -> str:
    """Search the Granbury long-term care manual by keyword.

    Use this for any question about the manual, e.g. 'infection control',
    'QAPI', 'survey', or 'emergency'.
    """
    q = q.lower()
    hits = [s for s in SECTIONS
            if q in s["title"].lower() or q in s["summary"].lower()
            or any(q in k for k in s["keywords"])]
    return json.dumps({"query": q, "results": hits})


@mcp.tool()
def list_sections() -> str:
    """List all sections of the Granbury long-term care manual."""
    return json.dumps({"sections": SECTIONS})


@mcp.tool()
def get_section(section_id: str) -> str:
    """Get one manual section by its id, e.g. 'infection-control' or 'qapi'."""
    for s in SECTIONS:
        if s["id"] == section_id:
            return json.dumps(s)
    return json.dumps({"error": "Section not found", "section_id": section_id})


if __name__ == "__main__":
    # Listens at http://HOST:PORT/mcp
    # On a host like Render, set:
    #   FASTMCP_HOST=0.0.0.0
    #   FASTMCP_PORT=$PORT
    mcp.run(transport="streamable-http")
