import asyncio
from app.server import mcp

async def test_my_tools():
    print("🧪 STARTING MANUAL TOOL TESTS...\n")

    # TEST 1: Count Members
    print("--- Test 1: Calling 'get_total_members' ---")
    # We call the function directly as if we were the server
    result_count = await mcp.call_tool("get_total_members", {})
    print(f"Output: {result_count}")
    
    # TEST 2: List Expired Members
    print("\n--- Test 2: Calling 'list_expired_members' ---")
    result_expired = await mcp.call_tool("list_expired_members", {})
    print(f"Output: {result_expired}")

    # TEST 3: Get Member by ID
    # We pass the arguments exactly how the AI would send them
    print("\n--- Test 3: Calling 'get_member_by_id' (ID=1) ---")
    result_id = await mcp.call_tool("get_member_by_id", {"member_id": 1})
    print(f"Output: {result_id}")

    # TEST 4: Get Non-Existent Member
    print("\n--- Test 4: Calling 'get_member_by_id' (ID=999) ---")
    result_missing = await mcp.call_tool("get_member_by_id", {"member_id": 999})
    print(f"Output: {result_missing}")

    print("\n✅ TESTS COMPLETE.")

if __name__ == "__main__":
    asyncio.run(test_my_tools())