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

console = Console()

# Load environment variables and setup Gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

async def generate_with_timeout(client, prompt, timeout=10):
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

async def get_llm_response(client, prompt):
    """Get response from LLM with timeout"""
    response = await generate_with_timeout(client, prompt)
    if response and response.text:
        return response.text.strip()
    return None

async def main():
    try:
        console.print(Panel("Chain of Thought Calculator + Paint", border_style="cyan"))

        server_params = StdioServerParameters(
            command="python",
            args=["cot_tools.py"]
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                print("Requesting tool list...")
                tools_result = await session.list_tools()
                tools = tools_result.tools
                print(f"Successfully retrieved {len(tools)} tools")

                # Create system prompt with available tools
                print("Creating system prompt...")
                print(f"Number of tools: {len(tools)}")
                
                try:
                    # First, let's inspect what a tool object looks like
                    # if tools:
                    #     print(f"First tool properties: {dir(tools[0])}")
                    #     print(f"First tool example: {tools[0]}")
                    
                    tools_description = []
                    for i, tool in enumerate(tools):
                        try:
                            # Get tool properties
                            params = tool.inputSchema
                            desc = getattr(tool, 'description', 'No description available')
                            name = getattr(tool, 'name', f'tool_{i}')
                            
                            # Format the input schema in a more readable way
                            if 'properties' in params:
                                param_details = []
                                for param_name, param_info in params['properties'].items():
                                    param_type = param_info.get('type', 'unknown')
                                    param_details.append(f"{param_name}: {param_type}")
                                params_str = ', '.join(param_details)
                            else:
                                params_str = 'no parameters'

                            tool_desc = f"{i+1}. {name}({params_str}) - {desc}"
                            tools_description.append(tool_desc)
                            print(f"Added description for tool: {tool_desc}")
                        except Exception as e:
                            print(f"Error processing tool {i}: {e}")
                            tools_description.append(f"{i+1}. Error processing tool")
                    
                    tools_description = "\n".join(tools_description)
                    print("Successfully created tools description")
                except Exception as e:
                    print(f"Error creating tools description: {e}")
                    tools_description = "Error loading tools"

                system_prompt = """You are a mathematical reasoning and Windows tools agent that solves problems step by step.
You follow structured reasoning and use tools as needed.

Available Tools:""" + f"\n{tools_description}\n" + """Task Flow:
First, break the problem into logical steps using show_reasoning.

For each step that involves a computation, use calculate.

After calculating, verify each result using verify.

After all steps are completed, use check_consistency to ensure the steps align logically.

Once verified and consistent, Perform the windows interaction actions and return the final answer using FINAL_ANSWER 

Fallback Behavior:
If calculate fails or gives an unexpected result, re-analyze the expression using show_reasoning and attempt a corrected calculate.

If verify fails, report the mismatch and suggest a fix using show_reasoning.

If check_consistency fails, re-evaluate the steps with show_reasoning and correct the errors.

If uncertain at any step, respond with exactly in this format without any markdown syntax:

FUNCTION_CALL: {"name": function_name, "args": {"param1": value1, "param2": value2, ...}}
FINAL_ANSWER: [answer]

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

                problem = """calculate area triangle with sides 10, 8, 6 cms
                Open a Microsoft paint window on the right side of screen, draw a 400x400 pixel size rectangle from 300,300 top left co-ordinate, then write the final result in a textbox"""
                console.print(Panel(f"Problem: {problem}", border_style="cyan"))

                # Initialize conversation
                prompt = f"{system_prompt}\n\nSolve this problem step by step: {problem}"
                conversation_history = []
                try:
                    while True:
                        response = await generate_with_timeout(client, prompt)
                        if not response or not response.text:
                            break

                        result = response.text.strip()
                        
                        console.print(f"\n[yellow]Assistant:[/yellow] {result}")
                        if "FUNCTION_CALL" in result:
                            match = re.search(r'(FUNCTION_CALL:\s*\{.*\})', result)
                            if match:
                                result = match.group(1)

                        if result.startswith("FUNCTION_CALL:"):
                            _, function_info = result.split(":", 1)
                            function_info = json.loads(function_info.strip())
                            func_name = function_info.get("name")
                            func_args = function_info.get("args")

                            if func_name == "show_reasoning":
                                steps = func_args.get("steps")
                                for i, step in enumerate(steps):
                                    console.print(f"[pink]Step {i + 1} : [/pink]{step}")
                                await session.call_tool("show_reasoning", arguments={"steps": steps})
                                prompt += f"\nUser: Next step?"
                                
                            elif func_name == "calculate":
                                expression = str(func_args.get("expression"))
                                calc_result = await session.call_tool("calculate", arguments={"expression": expression})
                                if calc_result.content:
                                    value = calc_result.content[0].text
                                    prompt += f"\nUser: Result is {value}. Let's verify this step."
                                    conversation_history.append((expression, float(value)))
                                    
                            elif func_name == "verify":
                                expression, expected = str(func_args.get("expression")), float(func_args.get("expected"))
                                await session.call_tool("verify", arguments={
                                    "expression": expression,
                                    "expected": expected
                                })
                                prompt += f"\nUser: Verified."
                            
                            elif func_name == "check_consistency":
                                steps = func_args.get("steps")
                                await session.call_tool("verify", arguments={"steps": steps})
                                prompt += f"\nUser: Consistency Checked."

                            elif func_name == "open_paint":
                                paint_result = await session.call_tool("open_paint", arguments={})
                                prompt += f"\nUser: Opened Paint."

                            elif func_name == "draw_rectangle":
                                await session.call_tool("draw_rectangle", arguments=func_args)
                                prompt += f"\nUser: Rectangle Drawn."

                            elif func_name == "add_text_to_paint":
                                await session.call_tool("add_text_to_paint", arguments={"text": func_args.get("text")})
                                prompt += f"\nUser: Added Text to Paint."
                                
                        elif result.startswith("FINAL_ANSWER:"):
                            # Verify the final answer against the original problem
                            if conversation_history:
                                final_answer = float(result.split("[")[1].split("]")[0])
                                await session.call_tool("verify", arguments={
                                    "expression": problem,
                                    "expected": final_answer
                                })
                            break
                        
                        prompt += f"\nAssistant: {result}"
                    console.print("\n[green]Calculation completed![/green]")
                except Exception as e:
                    console.print(f"Error: {str(e)}, expr : {len(expression.strip())}")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())
