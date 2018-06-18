import asyncio
import asyncio.subprocess
import concurrent
import logging
import os
import os.path
import shlex
import signal
import sys
import time
import traceback
from functools import partial
logging.getLogger('asyncio').setLevel(logging.DEBUG)

def get_event_loop():
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        print('opening new loop')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    def debug_exception_handler(loop, context):
        print(context)

    loop.set_debug(True)
    loop.set_exception_handler(debug_exception_handler)
    return loop

_cmd = """
python -c "
import time
while True:
    print('more')
    time.sleep(1)
"
"""

class ExtProgramRunner:
    run = True
    processes = []

    def __init__(self):
        pass

    def start(self, loop):
        self.current_loop = loop
        self.current_loop.add_signal_handler(signal.SIGINT, lambda: asyncio.async(self.stop('SIGINT')))
        self.current_loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.async(self.stop('SIGTERM')))
        asyncio.async(self.cancel_monitor())
        asyncio.Task(self.run_external_programs())

    async def stop(self, sig):
        print("Got {} signal".format(sig))
        self.run = False
        for process in self.processes:
            print("sending SIGTERM signal to the process with pid {}".format(process.pid))
            process.send_signal(signal.SIGTERM)
        print("Canceling all tasks")
        for task in asyncio.Task.all_tasks():
            task.cancel()

    async def cancel_monitor(self):
        while True:
            try:
                await asyncio.sleep(0.05)
            except asyncio.CancelledError:
                break
        print("Stopping loop")
        self.current_loop.stop()

    async def run_external_programs(self):
        asyncio.Task(self.run_cmd_forever(_cmd))

    async def run_cmd_forever(self, cmd):
        args = shlex.split(cmd)
        while self.run:
            process = await asyncio.create_subprocess_exec(*args, preexec_fn=os.setpgrp)
            self.processes.append(process)
            exit_code = await process.wait()
            for idx, p in enumerate(self.processes):
                if process.pid == p.pid:
                    self.processes.pop(idx)
            print("External program '{}' exited with exit code {}, relauching".format(cmd, exit_code))

loop = get_event_loop()

def run(background=False):
    asyncio.get_child_watcher().attach_loop(loop)
    daemon = ExtProgramRunner()
    loop.call_soon(daemon.start, loop)
    # start main event loop
    if background:
        executor = None
        loop.run_in_executor(executor, loop.run_forever)
    else:
        loop.run_forever()

def main():
    try:
        run(background=False)
    except KeyboardInterrupt:
        pass
    except asyncio.CancelledError as exc:
        print("asyncio.CancelledError")
    except Exception as exc:
        print(exc, file=sys.stderr)
        print("====", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
    finally:
        print("Stopping daemon...")
        loop.close()

if __name__ == '__main__':
    import argh
    argh.dispatch_command(main)
