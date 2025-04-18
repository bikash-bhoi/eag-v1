import os
import re
import json
from click import prompt
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
import asyncio
from rich.console import Console
from rich.panel import Panel

from memory import update_memory
from perception import generate_with_timeout, build_prompt
from memory import update_memory
from decision import decide
from action import act

console = Console()

# Load environment variables and setup Gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

async def main():
    try:
        console.print(Panel("Chain of Thought Calculator + Paint", border_style="cyan"))

        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
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

                problem = """calculate area triangle with sides 10, 8, 6 cms
                Open a Microsoft paint window on the right side of screen, draw a 400x400 pixel size rectangle from 300,300 top left co-ordinate, then write the final result in a textbox"""
                console.print(Panel(f"Problem: {problem}", border_style="cyan"))
                prompt = await build_prompt(tools_description, problem)

                conversation_history = []
                try:
                    while True:
                        response = await generate_with_timeout(client, prompt, console)
                        if not response or not response.text:
                            break

                        result = response.text.strip()
                        
                        console.print(f"\n[yellow]Assistant:[/yellow] {result}")

                        func_name, args, mem_update = decide(problem, result, console, conversation_history)
                        return_val = await act(session, func_name, args)
                        prompt, conversation_history = update_memory(prompt, return_val, args, func_name, mem_update, conversation_history, result)
                        
                        if func_name == "check_consistency":
                            break
                        
                    console.print("\n[green]Calculation completed![/green]")
                except Exception as e:
                    console.print(f"Error: {str(e)}")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())
