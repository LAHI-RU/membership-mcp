# Membership MCP

Membership MCP is a small Model Context Protocol (MCP) service plus a Streamlit chat UI for querying a membership database with AI assistance. The MCP server exposes database-aware tools (list expired members, count members, look up a member by ID) that the OpenAI chat loop calls when needed.

## Features
- MCP tools for membership data: list expired members, total count, fetch by ID.
- SQLite-backed storage with easy seeding for demos.
- Streamlit chat UI that routes questions through OpenAI and the MCP tools.
- Simple test scripts to verify environment and tool behavior.

## Architecture
- `app/server.py`: FastMCP server defining the membership tools.
- `app/database.py`: SQLite connection + schema initialization.
- `app/ai_handler.py`: Bridges OpenAI chat completions with MCP tools.
- `frontend.py`: Streamlit chat client for interactive queries.
- `seed_data.py`: Seeds `members.db` with sample members.
- `test_env.py` / `test_tools.py`: Quick checks for env setup and tool responses.

## Requirements
- Python 3.10+
- An OpenAI API key with access to `gpt-4o` (set in `.env`)
- `pip install -r requirements.txt`

## Setup
1. Create and activate a virtual environment.
   ```bash
   python -m venv venv
   ./venv/Scripts/activate  # Windows
   ```
2. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables in `.env` (do not commit secrets):
   ```env
   DB_PATH=members.db
   LOG_LEVEL=INFO
   OPENAI_API_KEY=your-api-key
   ```
4. Initialize the database (creates the `members` table).
   ```bash
   python app/database.py
   ```
5. (Optional) Seed demo data.
   ```bash
   python seed_data.py
   ```

## Running the MCP server
Start the MCP server with uvicorn:
```bash
uvicorn app.server:mcp --host 0.0.0.0 --port 8000 --reload
```
This hosts the MCP endpoint that OpenAI and the Streamlit client call.

## Running the Streamlit UI
In a separate shell with the virtual environment active:
```bash
streamlit run frontend.py
```
Ask questions like “How many members do we have?” or “List expired members”. The app will invoke MCP tools automatically when OpenAI requests them.

## Testing and verification
- Environment sanity check: `python test_env.py`
- Manual tool checks (runs MCP tools directly): `python test_tools.py`

## Project layout
```
app/
  ai_handler.py      # OpenAI <-> MCP bridge
  database.py        # SQLite connection and schema init
  server.py          # FastMCP tool definitions
frontend.py          # Streamlit chat UI
seed_data.py         # Sample data loader
members.db           # Local SQLite database (generated/seeded)
requirements.txt
.env                 # Local config (not for commit)
```
