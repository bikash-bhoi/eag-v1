from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import re
from pywinauto.application import Application
import win32gui
import win32con
import time
from win32api import GetSystemMetrics
from pydentic_models import *

console = Console()
mcp = FastMCP("CoTCalculator")

@mcp.tool()
def show_reasoning(input_data: ShowReasoningInput) -> TextResponse:
    """Describe your plan in steps. Each step must include a 
    "description" and a "type" field (e.g., "arithmetic", "logic", "geometry")"""
    console.print("[blue]FUNCTION CALL:[/blue] show_reasoning()")
    for i, step in enumerate(input_data.steps, 1):
        console.print(Panel(
            f"{step.description}",
            title=f"Step {i} - {step.type}",
            border_style="cyan"
        ))
    return TextResponse(
        content=TextContent(
            type="text",
            text="Reasoning shown"
        )
    )

@mcp.tool()
def calculate(input_data: CalculateInput) -> TextResponse:
    """Calculate the result of an expression, expression has to be python based"""
    console.print("[blue]FUNCTION CALL:[/blue] calculate()")
    console.print(f"[blue]Expression:[/blue] {input_data.expression}")
    try:
        result = eval(input_data.expression.strip())
        console.print(f"[green]Result:[/green] {result}")
        return TextResponse(
            content=TextContent(
                type="text",
                text=str(result)
            )
        )
    except Exception as e:
        return TextResponse(
            content=TextContent(
                type="text",
                text=f"Error: {str(e)} for Expression: {input_data.expression}"
            )
        )

@mcp.tool()
def verify(input_data: VerifyInput) -> TextResponse:
    """Verify if a calculation is correct"""
    console.print("[blue]FUNCTION CALL:[/blue] verify()")
    console.print(f"[blue]Verifying:[/blue] {input_data.expression} = {input_data.expected}")
    try:
        actual = float(eval(input_data.expression))
        is_correct = abs(actual - float(input_data.expected)) < 1e-10
        
        if is_correct:
            console.print(f"[green] Correct! {input_data.expression} = {input_data.expected}[/green]")
        else:
            console.print(f"[red] Incorrect! {input_data.expression} should be {actual}, got {input_data.expected}[/red]")
            
        return TextResponse(
            content=TextContent(
                type="text",
                text=str(is_correct)
            )
        )
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        return TextResponse(
            content=TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )
        )

@mcp.tool()
def check_consistency(input_data: CheckConsistencyInput) -> TextResponse:
    """Check if calculation steps are consistent with each other"""
    console.print("[blue]FUNCTION CALL:[/blue] check_consistency()")
    
    try:
        # Create a table for step analysis
        table = Table(
            title="Step-by-Step Consistency Analysis",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        table.add_column("Step", style="cyan")
        table.add_column("Expression", style="blue")
        table.add_column("Result", style="green")
        table.add_column("Checks", style="yellow")

        issues = []
        warnings = []
        insights = []
        previous = None
        
        for i, (expression, result) in enumerate(input_data.steps, 1):
            checks = []
            
            # 1. Basic Calculation Verification
            try:
                expected = eval(expression)
                if abs(float(expected) - float(result)) < 1e-10:
                    checks.append("[green] Calculation verified[/green]")
                else:
                    issues.append(f"Step {i}: Calculation mismatch")
                    checks.append("[red] Calculation error[/red]")
            except:
                warnings.append(f"Step {i}: Couldn't verify calculation")
                checks.append("[yellow]! Verification failed[/yellow]")

            # 2. Dependency Analysis
            if previous:
                prev_expr, prev_result = previous
                if str(prev_result) in expression:
                    checks.append("[green] Uses previous result[/green]")
                    insights.append(f"Step {i} builds on step {i-1}")
                else:
                    checks.append("[blue]○ Independent step[/blue]")

            # 3. Magnitude Check
            if previous and result != 0 and previous[1] != 0:
                ratio = abs(result / previous[1])
                if ratio > 1000:
                    warnings.append(f"Step {i}: Large increase ({ratio:.2f}x)")
                    checks.append("[yellow]! Large magnitude increase[/yellow]")
                elif ratio < 0.001:
                    warnings.append(f"Step {i}: Large decrease ({1/ratio:.2f}x)")
                    checks.append("[yellow]! Large magnitude decrease[/yellow]")

            # 4. Pattern Analysis
            operators = re.findall(r'[\+\-\*\/\(\)]', expression)
            if '(' in operators and ')' not in operators:
                warnings.append(f"Step {i}: Mismatched parentheses")
                checks.append("[red] Invalid parentheses[/red]")

            # 5. Result Range Check
            if abs(result) > 1e6:
                warnings.append(f"Step {i}: Very large result")
                checks.append("[yellow]! Large result[/yellow]")
            elif abs(result) < 1e-6 and result != 0:
                warnings.append(f"Step {i}: Very small result")
                checks.append("[yellow]! Small result[/yellow]")

            # Add row to table
            table.add_row(
                f"Step {i}",
                expression,
                f"{result}",
                "\n".join(checks)
            )
            
            previous = (expression, result)

        # Display Analysis
        console.print("\n[bold cyan]Consistency Analysis Report[/bold cyan]")
        console.print(table)

        if issues:
            console.print(Panel(
                "\n".join(f"[red]• {issue}[/red]" for issue in issues),
                title="Critical Issues",
                border_style="red"
            ))

        if warnings:
            console.print(Panel(
                "\n".join(f"[yellow]• {warning}[/yellow]" for warning in warnings),
                title="Warnings",
                border_style="yellow"
            ))

        if insights:
            console.print(Panel(
                "\n".join(f"[blue]• {insight}[/blue]" for insight in insights),
                title="Analysis Insights",
                border_style="blue"
            ))

        # Final Consistency Score
        total_checks = len(input_data.steps) * 5  # 5 types of checks per step
        passed_checks = total_checks - (len(issues) * 2 + len(warnings))
        consistency_score = (passed_checks / total_checks) * 100

        console.print(Panel(
            f"[bold]Consistency Score: {consistency_score:.1f}%[/bold]\n" +
            f"Passed Checks: {passed_checks}/{total_checks}\n" +
            f"Critical Issues: {len(issues)}\n" +
            f"Warnings: {len(warnings)}\n" +
            f"Insights: {len(insights)}",
            title="Summary",
            border_style="green" if consistency_score > 80 else "yellow" if consistency_score > 60 else "red"
        ))

        return TextResponse(
            content=TextContent(
                type="text",
                text=str(ConsistencyResult(
                    consistency_score=consistency_score,
                    issues=issues,
                    warnings=warnings,
                    insights=insights
                ).dict())
            )
        )
    except Exception as e:
        console.print(f"[red]Error in consistency check: {str(e)}[/red]")
        return TextContent(
            content=TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )
        )

@mcp.tool()
async def draw_rectangle(input_data: RectangleInput) -> TextResponse:
    """Draw a rectangle in Paint from (x1,y1) to (x2,y2)"""
    global paint_app
    try:
        if not paint_app:
            return TextResponse(
                content=TextContent(
                    type="text",
                    text=f"Rectangle drawn from ({input_data.x1},{input_data.y1}) to ({input_data.x2},{input_data.y2})"
                )
            )

        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width to adjust coordinates
        primary_width = GetSystemMetrics(0)
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.2)
        
        # Click on the Rectangle tool using the correct coordinates right half of the screen
        paint_window.click_input(coords=(439, 69 ))  # Using coordinates

        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Draw rectangle - coordinates should already be relative to the Paint window
        # No need to add primary_width since we're clicking within the Paint window
        canvas.press_mouse_input(coords=(input_data.x1+1280, input_data.y1))
        canvas.move_mouse_input(coords=(input_data.x2+1280, input_data.y2))
        canvas.release_mouse_input(coords=(input_data.x2+1280, input_data.y2))
        
        return TextResponse(
            content=TextContent(
                type="text",
                text=f"Rectangle drawn from ({input_data.x1},{input_data.y1}) to ({input_data.x2},{input_data.y2})"
            )
        )
    except Exception as e:
        return TextResponse(
            content=TextContent(
                type="text",
                text=f"Error drawing rectangle: {str(e)}"
            )
        )

@mcp.tool()
async def add_text_to_paint(input_data: PaintTextInput) -> TextResponse:
    """Add text in Paint"""
    global paint_app
    try:
        if not paint_app:
            return TextResponse(
                content=TextContent(
                            type="text",
                            text="Paint is not open. Please call open_paint first."
                        )
            )
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.2)
        
        # Click on the Rectangle tool
        # paint_window.click_input(coords=(797, -27))
        # time.sleep(0.5)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # # Select text tool using keyboard shortcuts
        # paint_window.type_keys('t')
        # time.sleep(0.5)
        # paint_window.type_keys('x')
        # time.sleep(0.5)
        paint_window.type_keys("%")  # ALT key
        time.sleep(1)
        paint_window.type_keys("H")  # H key
        time.sleep(1)
        paint_window.type_keys("T")  # T key
        time.sleep(1)
        
        # Click where to start typing
        canvas.click_input(coords=(350, 340))
        time.sleep(0.7)

        canvas.type_keys('^b')
        time.sleep(0.7)
        text = f"Final Answer : {input_data.text}"
        # Type the text passed from client
        paint_window.type_keys(text, with_spaces=True)
        time.sleep(0.5)
        
        # Click to exit text mode
        canvas.click_input(coords=(800, 530))
        
        return TextResponse(
            content=TextContent(
                type="text",
                text=f"Rectangle drawn and text '{text}' added successfully"
            )
        )

    except Exception as e:
        return TextResponse(
            content=TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )
        )

@mcp.tool()
async def open_paint() -> TextResponse:
    """Open Microsoft Paint on the right side on current monitor"""
    global paint_app
    try:
        paint_app = Application().start('mspaint.exe')
        time.sleep(0.2)
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width
        primary_width = GetSystemMetrics(0)
        primary_height = GetSystemMetrics(1)
        
        # First move to secondary monitor without specifying size
        win32gui.SetWindowPos(
            paint_window.handle,
            win32con.HWND_TOP,
            primary_width // 2, 0,  # Position it on right half of primary monitor
            primary_width // 2, primary_height,  # Size it to the right half of the primary monitor
            0 #win32con.SWP_NOSIZE #| win32con.SWP_SHOWWINDOW # Don't change the size
        )
        win32gui.ShowWindow(paint_window.handle, win32con.SW_NORMAL)
        time.sleep(0.2)
        
        return TextResponse(
            content=TextContent(
                type="text",
                text="Paint opened successfully on Right side of monitor"
            )
        )

    except Exception as e:
        return TextResponse(
            content=TextContent(
                type="text",
                text=f"Error opening Paint: {str(e)}"
            )
        )


if __name__ == "__main__":
    import sys
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "dev":
            mcp.run()
        else:
            mcp.run(transport="stdio")
    except Exception as e:
        # Ensure error is properly JSON serialized
        error_response = {
            "content": [
                TextContent(
                    type="text",
                    text=f"Server Error: {str(e)}"
                )
            ]
        }
        print(error_response)
        sys.exit(1)
