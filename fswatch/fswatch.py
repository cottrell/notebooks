import asyncio
import traceback
import os
import os.path
import sys
import time
import signal
import shlex
from functools import partial
import concurrent
import logging
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

    async def start(self, loop):
        self.current_loop = loop
        self.current_loop.add_signal_handler(signal.SIGINT, lambda: asyncio.ensure_future(self.stop('SIGINT')))
        self.current_loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.ensure_future(self.stop('SIGTERM')))
        loop.call_soon(asyncio.ensure_future, self.cancel_monitor())
        loop.call_soon(asyncio.ensure_future, self.run_external_programs())

    async def stop(self, sig):
        print("Got {} signal".format(sig))
        self.run = False
        for process in self.processes:
            print("sending SIGTERM signal to the process with pid {}".format(process.pid))
            try:
                # process.send_signal(signal.SIGTERM)
                process.kill()
            except ProcessLookupError as e:
                # process already dead? how to check?
                pass
        print("Canceling all tasks")
        for task in asyncio.Task.all_tasks():
            task.cancel()

    async def cancel_monitor(self):
        print('cancel monitor start')
        while True:
            try:
                await asyncio.sleep(0.05)
            except asyncio.CancelledError:
                break
        print("Stopping loop")
        self.current_loop.stop()

    async def run_external_programs(self):
        print('run external program start')
        # schedule tasks for execution
        asyncio.Task(self.run_cmd_forever(_cmd))

    async def run_cmd_forever(self, cmd):
        print('run cmd forever start')
        args = shlex.split(cmd)
        while self.run: # for now do not run like this, just let it die
            process = await asyncio.create_subprocess_exec(*args)
            self.processes.append(process)
            exit_code = await process.wait()
            for idx, p in enumerate(self.processes):
                if process.pid == p.pid:
                    self.processes.pop(idx)
            print("External program '{}' exited with exit code {}, relaunching".format(cmd, exit_code))

loop = get_event_loop()

def run(background=False):
    # for REPL
    asyncio.get_child_watcher().attach_loop(loop)
    daemon = ExtProgramRunner()
    loop.call_soon(asyncio.ensure_future, daemon.start(loop))
    # start main event loop
    if not background:
        loop.run_forever()
    else:
        loop.run_in_executor(None, loop.run_forever)

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
