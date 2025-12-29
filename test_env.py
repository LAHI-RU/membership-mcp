import mcp
import fastapi
import pydantic
from dotenv import load_dotenv
import os

load_dotenv()

# We will just print the string "Imported" if it works
print("✅ MCP Package imported successfully") 
print("✅ FastAPI Version:", fastapi.__version__)
print("✅ Database Path Configured:", os.getenv("DB_PATH"))
print("🚀 Environment is ready!")