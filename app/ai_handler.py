import os
import json
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
from app.server import mcp

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_tools_for_openai():
    """
    Fetches tools from the MCP server and converts them 
    to the format OpenAI expects.
    """
    # await the async function to get the list of tools
    mcp_tools = await mcp.list_tools()
    
    openai_tools = []
    for tool in mcp_tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                # MCP uses 'inputSchema', OpenAI expects 'parameters'
                "parameters": tool.inputSchema 
            }
        })
    return openai_tools

async def chat_with_ai(user_query: str):
    """
    The main loop:
    1. Send user query to OpenAI + List of Tools.
    2. OpenAI decides if it needs to call a tool.
    3. If yes, we execute the tool locally and send the result back.
    4. OpenAI generates the final answer.
    """
    messages = [{"role": "user", "content": user_query}]

    # 1. Fetch tools safely inside the async loop
    tools_list = await get_tools_for_openai()

    # --- ROUND 1: Ask OpenAI ---
    response = client.chat.completions.create(
        model="gpt-4o",  # or gpt-3.5-turbo
        messages=messages,
        tools=tools_list,
        tool_choice="auto" 
    )
    
    response_message = response.choices[0].message
    messages.append(response_message)

    # --- ROUND 2: Check for Tool Calls ---
    if response_message.tool_calls:
        # print(f"🤖 AI wants to use tools: {len(response_message.tool_calls)}")
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # print(f"🔧 Calling Tool: {function_name} with {function_args}")
            
            # EXECUTING THE MCP TOOL
            # We call the tool using mcp.call_tool
            tool_result = await mcp.call_tool(function_name, function_args)
            
            # Add the tool result to the conversation history
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(tool_result),
            })

        # --- ROUND 3: Final Answer ---
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return final_response.choices[0].message.content
    
    else:
        return response_message.content