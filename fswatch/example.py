# python example.py produce | python ./example.py consume
# wrapper.py

python example.py produce | python ./example.py consume

import asyncio
import random
import sys


async def produce():
    for i in range(10000):
        await asyncio.sleep(random.randint(0, 3))
        yield str(i)


async def consume(generator):
    async for value in generator:
        print(int(value.strip().decode()) ** 2)


async def system_out_generator(loop, stdout, generator):
    async for line in generator:
        print(line, file=stdout, flush=True)


async def system_in_generator(loop, stdin):
    reader = asyncio.StreamReader(loop=loop)
    reader_protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: reader_protocol, stdin)
    while True:
        line = await reader.readline()
        if not line:
            break
        yield line


async def main(loop):
    try:
        if sys.argv[1] == "produce":
            await system_out_generator(loop, sys.stdout, produce())
        elif sys.argv[1] == "consume":
            await consume(system_in_generator(loop, sys.stdin))
    except IndexError:
        await consume(produce())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
