import asyncio
import contextlib
import os
import locale


class SubprocessProtocol(asyncio.SubprocessProtocol):
    def pipe_data_received(self, fd, data):
        if fd == 1:
            name = 'stdout'
        elif fd == 2:
            name = 'stderr'
        text = data.decode(locale.getpreferredencoding(False))
        print('Received from {}: {}'.format(name, text.strip()))

    def process_exited(self):
        loop.stop()


if os.name == 'nt':
    # On Windows, the ProactorEventLoop is necessary to listen on pipes
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()
with contextlib.closing(loop):
    # This will only connect to the process
    import shlex
    cmd = 'for x in $(seq 100); do echo $1 && sleep 1; done'
    # cmd = shlex.split(cmd)
    transport = loop.run_until_complete(loop.subprocess_shell(SubprocessProtocol, cmd, stdout=asyncio.subprocess.PIPE))[0]
    # Wait until process has finished
    loop.run_forever()
    print('Program exited with: {}'.format(transport.get_returncode()))
