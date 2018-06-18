import asyncio
loop = asyncio.get_event_loop()

async def sleep():
    while True:
        await asyncio.sleep(.2)
        print('yes')

asyncio.ensure_future(sleep())

# blocks
# loop.run_forever()

loop.run_in_executor(None, loop.run_forever)
print('more')
