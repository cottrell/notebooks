# https://stackoverflow.com/questions/41536151/terminate-external-program-run-through-asyncio-with-specific-signal
import asyncio
import concurrent
import logging
import signal
import shlex
import asyncio.subprocess
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

class App():
    def __init__(self):
        self.loop = None
        self.started = False
        self.output = dict()
        self.processes = list()
    def _wrapped_runner(self):
    	try:
    	    self.loop.run_forever()
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
    def start(self, loop, background=True):
        self.loop = loop
        self.loop.add_signal_handler(signal.SIGINT, lambda: asyncio.async(self.stop('SIGINT')))
        self.loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.async(self.stop('SIGTERM')))
        asyncio.ensure_future(self.cancel_monitor(), loop=self.loop)
        if background:
            executor = None
            self.loop.run_in_executor(executor, self._wrapped_runner)
        else:
            self._wrapped_runner()
    async def stop(self, sig):
        print("Got {} signal".format(sig))
        for process in self.processes:
            print("sending SIGTERM signal to the process with pid {}".format(process.pid))
            process.send_signal(signal.SIGTERM)
        print("Canceling all tasks")
        for task in asyncio.Task.all_tasks():
            if task != asyncio.Task.current_task():
                task.cancel()
    async def cancel_monitor(self):
        while True:
            try:
                await asyncio.sleep(0.05)
                # print('cancel monitor running') # debug only, prints a lot
            except asyncio.CancelledError:
                break
        print("Stopping loop")
        self.loop.stop()
    async def _handle_stdout(self, process, cmd):
        line = await process.stdout.readline()
        line = line.strip().decode()
        self.output[cmd]['stdout'].append(line)
        print(line)
    async def add_cmd(self, cmd):
        assert self.loop is not None, 'loop is None'
        self.output[cmd] = dict(stdout=list(), stderr=list())
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
                )
        while True:
            # self._handle_stdout(process, cmd)
            await asyncio.ensure_future(self._handle_stdout(process, cmd), loop=self.loop)
            # line = await process.stdout.readline()
            # line = line.strip().decode()
            # self.output[cmd]['stderr'].append(line)
            # print(line)

cmd = """
python -c "
import time
while True:
    print('more')
    time.sleep(1)
"
"""
loop = get_event_loop()
app = App()
def run():
    # asyncio.ensure_future(app.add_cmd('fswatch -Ltux tmp'), loop=loop)
    asyncio.ensure_future(app.add_cmd(cmd), loop=loop)
    app.start(loop, background=False)
    # loop.call_soon(app.add_cmd('fswatch -Ltux tmp'))

if __name__ == '__main__':
    run()

