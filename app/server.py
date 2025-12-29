from mcp.server.fastmcp import FastMCP
from app.database import get_db_connection
import json
from datetime import datetime

# Initialize FastMCP
mcp = FastMCP("membership")

# --- HELPER FUNCTION ---
def format_members(rows):
    """
    Helper to convert database rows into a list of dictionaries.
    This makes the data easy for the AI to read (JSON format).
    """
    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "expiry_date": row["expiry_date"],
            "status": row["status"]
        })
    return json.dumps(results, indent=2)

# --- TOOLS ---

@mcp.tool()
async def list_expired_members(limit: int = 10) -> str:
    """
    Lists members whose membership has expired.
    
    Args:
        limit: Max number of records to return (default 10).
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    conn = get_db_connection()
    try:
        # Added LIMIT ? to the query
        query = "SELECT * FROM members WHERE expiry_date < ? AND status = 'active' LIMIT ?"
        cursor = conn.execute(query, (today, limit))
        rows = cursor.fetchall()
        
        if not rows:
            return "No expired members found."
            
        return format_members(rows)
    finally:
        conn.close()

@mcp.tool()
async def get_total_members() -> str:
    """
    Returns the count of all members in the database.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT COUNT(*) as count FROM members")
        result = cursor.fetchone()
        return f"Total members: {result['count']}"
    finally:
        conn.close()

@mcp.tool()
async def get_member_by_id(member_id: int) -> str:
    """
    Fetches details of a specific member by their numeric ID.
    
    Args:
        member_id: The unique ID of the member.
    """
    conn = get_db_connection()
    try:
        # We use ? as a placeholder to prevent SQL Injection
        cursor = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        row = cursor.fetchone()
        
        if row is None:
            return f"Member with ID {member_id} not found."
            
        return format_members([row])
    finally:
        conn.close()

# Allow running directly via 'uvicorn app.server:mcp'