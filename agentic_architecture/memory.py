import json

def update_memory(prompt, return_val, args, func_name, mem_update, conversation_history, result):

    if func_name == "calculate":
        val = json.loads(return_val.content[0].text)["content"]["text"]
        mem_update = mem_update.replace("##value##", str(val))
        conversation_history.append((args["input_data"]["expression"], float(val)))
    
    prompt += mem_update
    prompt += f"\nAssistant: {result}"
    return prompt, conversation_history
