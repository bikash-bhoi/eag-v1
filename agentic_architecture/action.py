import asyncio

async def act(session, func_name, args):
    return_val = await session.call_tool(func_name, args)
    return return_val
