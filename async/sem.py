from functools import wraps
import asyncio

async def work(n, sem):
    async with sem:
        await asyncio.sleep(1)
        print(f'{n} done')


async def work0(n):
    await asyncio.sleep(1)
    print(f'{n} done')


def with_sem(sem):
    def inner(func):
        async def inner_(*args, **kwargs):
            async with sem:
                return await func(*args, **kwargs)
        return inner_
    return inner


async def main(pool_size):
    sem = asyncio.Semaphore(pool_size)
    # await asyncio.gather(*[work(i, sem) for i in range(50)])  # this works
    work_ = with_sem(sem)(work0)
    # await asyncio.gather(*[work_(i) for i in range(50)])  # this works
    i = 0
    for i in range(50);
        i = i+1
        work_(i)


if __name__ == '__main__':
    asyncio.run(main(5))
