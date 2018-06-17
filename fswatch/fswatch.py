# https://docs.python.org/3/library/asyncio-subprocess.html#subprocess-using-streams
# https://stackoverflow.com/questions/41536151/terminate-external-program-run-through-asyncio-with-specific-signal
# https://stackoverflow.com/questions/45711041/how-to-use-a-read-write-stream-between-two-python-asyncio-coroutines
# https://www.programcreek.com/python/example/82526/asyncio.create_subprocess_exec
# https://stackoverflow.com/questions/43826254/exit-program-while-tasks-in-default-executor-are-still-running
# https://stackoverflow.com/questions/40016501/how-to-schedule-and-cancel-tasks-with-asyncio
import shlex
import asyncio
import asyncio.subprocess
import sys
import os
import time
import threading
import concurrent
import functools

# https://stackoverflow.com/questions/43826254/exit-program-while-tasks-in-default-executor-are-still-running

def run(task, background=True, executor=None):
    """
    runs in foreground if there are awaits.
    child proc is killed when python exits.
    """
    loop = get_event_loop()
    # is there a better pattern?
    # task = asyncio.ensure_future(task) # when is this needed?
    _callable = lambda : loop.run_until_complete(task)
    if background:
        loop.run_in_executor(executor, _callable)
    else:
        _callable()

def shutdown(loop=None):
    if loop is None:
        loop = get_event_loop()
    print('received stop signal, cancelling tasks...')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    print('bye, exiting in a minute...')

def stop_all():
    loop = get_event_loop()
    loop.stop()
    # nope does not work

def get_event_loop():
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        print('opening new loop')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop

_global_state = dict(a=0)

async def sleep():
    while True:
        await asyncio.sleep(1)
        print('sleep')

async def touch():
    cmd = 'while true; do touch tmp/$(date -u +"%Y-%m-%dT%H:%M:%SZ"); sleep 1; done'
    cmd = shlex.split(cmd)
    create = asyncio.create_subprocess_exec(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, preexec_fn=os.setpgrp)
    proc = await create
    while True:
        x = await proc.stdout.readline()
        # y = await proc.stderr.readline() # can not do this as whole thing will wait for y
        if x:
            print('here', x)
        else:
            print('process done. breaking loop')
            break
    return proc

async def watch():
    watcher = 'fswatch -Ltux tmp'
    watcher = asyncio.create_subprocess_shell(watcher, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    proc = await watcher
    while True:
        line = await proc.stdout.readline()
        print('STDOUT', line)
        yield line

async def get_date():
    code = 'import datetime; print(datetime.datetime.now())'
    # Create the subprocess, redirect the standard output into a pipe
    create = asyncio.create_subprocess_exec(sys.executable, '-c', code, stdout=asyncio.subprocess.PIPE)
    proc = await create
    # Read one line of output
    data = await proc.stdout.readline()
    line = data.decode('ascii').rstrip()
    # Wait for the subprocess exit
    await proc.wait()
    return line

def run_get_date():
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = get_event_loop()
    date = loop.run_until_complete(get_date())
    print("Current date: %s" % date)
    loop.close()

if __name__ == '__main__':
    run()
