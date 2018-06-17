import asyncio
import os
import random
import sys

async def echo():
    cmd = 'while True; do touch tmp/$(date -u +"%Y-%m-%dT%H:%M:%SZ"); echo HERE $x; sleep 1; done'
    create = asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, preexec_fn=os.setpgrp)
    proc = await create
    while True:
        x = await proc.stdout.readline()
        if x:
            print('here', x)
        else:
            print('process done. breaking loop')
            break
    return proc

async def sleep():
    while True:
        await asyncio.sleep(1)
        print('here')

def get_event_loop():
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        print('opening new loop')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop

global_kill_switch = False

async def killable_wrapper(task_func):
    # https://stackoverflow.com/questions/40016501/how-to-schedule-and-cancel-tasks-with-asyncio
    task = None
    while True:
        print('asdf')
        await asyncio.sleep(0) # why?
        print('b')
        if global_kill_switch and task:
            print('b')
            if not task.cancelled():
                task.cancel()
            else:
                task = None
        else:
            print('adbb')
            task = asyncio.ensure_future(task_func())

def run():
    loop = get_event_loop()
    app = killable_wrapper(sleep)
    fut = asyncio.ensure_future(app)
    loop.run_forever()
