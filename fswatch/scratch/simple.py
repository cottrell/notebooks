import shlex
import concurrent
import os
import asyncio
import asyncio.subprocess
import logging
logging.getLogger('asyncio').setLevel(logging.DEBUG)

def get_event_loop():
    loop = asyncio.get_event_loop()
    def debug_exception_handler(loop, context):
        print(context)
    loop.set_debug(True)
    loop.set_exception_handler(debug_exception_handler)
    return loop

loop = asyncio.get_event_loop()

async def sleep1():
    while True:
        await asyncio.sleep(.2)
        print('yes')

_cmd = """
python -c "
import time
while True:
    print('more')
    time.sleep(1)
"
"""
args = shlex.split(_cmd)
async def sleep2():
    process = await asyncio.create_subprocess_exec(*args, preexec_fn=os.setpgrp)

asyncio.get_child_watcher().attach_loop(loop)
# asyncio.ensure_future(sleep2())
loop.call_soon(asyncio.ensure_future, sleep2())

# blocks
# loop.run_forever()

executor = concurrent.futures.ThreadPoolExecutor()
loop.run_in_executor(None, loop.run_forever)
print('more')
