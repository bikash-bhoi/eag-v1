import re
import json
from pydentic_models import *


def decide(problem, result, console, conversation_history):
    if "FUNCTION_CALL" in result:
        match = re.search(r'(FUNCTION_CALL:\s*\{.*\})', result)
        if match:
            result = match.group(1)
    func_name, args, mem_update = "", {}, ""
    
    if result.startswith("FUNCTION_CALL:"):
        _, function_info = result.split(":", 1)
        function_info = json.loads(function_info.strip())
        func_name = function_info.get("name")
        func_args = function_info.get("args")

        if func_name == "show_reasoning":
            steps = func_args.get("steps")
            for i, step in enumerate(steps):
                console.print(f"[pink]Step {i + 1} : [/pink]{step}")
            mem_update = f"\nUser: Next step?"
            args = {"input_data": ShowReasoningInput(steps=steps).model_dump()}
            
        elif func_name == "calculate":
            expression = str(func_args.get("expression"))
            args = {"input_data": CalculateInput(expression=expression).model_dump()}
            mem_update = f"\nUser: Result is ##value##. Let's verify this step."
                
        elif func_name == "verify":
            expression, expected = str(func_args.get("expression")), float(func_args.get("expected"))
            args = {"input_data": VerifyInput(expression=expression, expected=expected).model_dump()}
            mem_update = f"\nUser: Verified."
        
        elif func_name == "check_consistency":
            steps = func_args.get("steps")
            args = {"input_data": CheckConsistencyInput(steps=steps).model_dump()}
            mem_update = f"\nUser: Consistency Checked."

        elif func_name == "open_paint":
            args = {"input_data": {}}
            mem_update = f"\nUser: Opened Paint."

        elif func_name == "draw_rectangle":
            args = {"input_data": RectangleInput(**func_args).model_dump()}
            mem_update = f"\nUser: Rectangle Drawn."

        elif func_name == "add_text_to_paint":
            args = {"input_data": PaintTextInput(text=func_args.get("text")).model_dump()}
            mem_update = f"\nUser: Added Text to Paint."
            
    elif result.startswith("FINAL_ANSWER:"):
        # Verify the final answer against the original problem
        if conversation_history:
            final_answer = float(result.split("[")[1].split("]")[0])
            func_name = "verify"
            args = {"input_data": VerifyInput(expression=problem, expected=final_answer).model_dump()}
            mem_update = ""
   
    return func_name, args, mem_update
    
