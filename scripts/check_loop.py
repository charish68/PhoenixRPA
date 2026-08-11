import asyncio

print(asyncio.get_event_loop_policy())
print(type(asyncio.get_running_loop()) if asyncio.get_event_loop().is_running() else "No running loop")