import os
import re
import json
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
import asyncio
from rich.console import Console
from rich.panel import Panel


async def generate_with_timeout(client, prompt, console, timeout=10):
    """Generate content with a timeout"""
    try:
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
            ),
            timeout=timeout
        )
        return response
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return None

async def get_llm_response(client, prompt, console):
    """Get response from LLM with timeout"""
    response = await generate_with_timeout(client, prompt, console)
    if response and response.text:
        return response.text.strip()
    return None

async def build_prompt(tools_description, problem):
    system_prompt = """You are a mathematical reasoning and Windows tools agent that solves problems step by step.
You follow structured reasoning and use tools as needed.

Available Tools:""" + f"\n{tools_description}\n" + """Task Flow:
First, break the problem into logical steps using show_reasoning.

For each step that involves a computation, use calculate.

After calculating, verify each result using verify.

After all steps are completed, use check_consistency to ensure the steps align logically.

Once verified, Perform the windows interaction actions and return the final answer using FINAL_ANSWER and at the end check consistency

Fallback Behavior:
If calculate fails or gives an unexpected result, re-analyze the expression using show_reasoning and attempt a corrected calculate.

If verify fails, report the mismatch and suggest a fix using show_reasoning.

If check_consistency fails, re-evaluate the steps with show_reasoning and correct the errors.

If uncertain at any step, respond with exactly. 
FUNCTION_CALL: {"name": function_name, "args": {"param1": value1, "param2": value2, ...}}
FINAL_ANSWER: [answer]

Important : Do not use backticks, markdown formatting, or code blocks in your reply.

Example Interaction:
User: Solve (2 + 3) * 4  
Assistant: FUNCTION_CALL: {
  "name": "show_reasoning",
  "args": {
    "steps": [
      {"description": "Solve inside parentheses: 2 + 3", "type": "arithmetic"},
      {"description": "Multiply the result by 4", "type": "arithmetic"}
    ]
  }
}  
User: Next step?  
Assistant: FUNCTION_CALL: {"name": "calculate", "args": {"expression": "2 + 3"}}  
User: Result is 5.  
Assistant: FUNCTION_CALL: {"name": "verify", "args": {"expression": "2 + 3", "expected": 5}}  
User: Verified.  
Assistant: FUNCTION_CALL: {"name": "calculate", "args": {"expression": "5 * 4"}}  
User: Result is 20.  
Assistant: FUNCTION_CALL: {"name": "verify", "args": {"expression": "(2 + 3) * 4", "expected": 20}}  
User: Verified.  
Assistant: FUNCTION_CALL: {"name": "open_paint", "args": {}} 
User: Opened Paint Window.
Assistant: FUNCTION_CALL: FUNCTION_CALL: {
  "name": "check_consistency",
  "args": {"steps": ["2 + 3 = 5", "5 * 4 = 20"]}
} 
User: Steps are consistent.  
Assistant: FINAL_ANSWER: [20]
"""
    # Initialize conversation
    return f"{system_prompt}\n\nSolve this problem step by step: {problem}"