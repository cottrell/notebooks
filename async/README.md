See this part of the doc that is easy to miss for recommended pattern

https://docs.python.org/3/library/asyncio-dev.html#concurrency-and-multithreading

> The loop.run_in_executor() method can be used with a concurrent.futures.ThreadPoolExecutor to execute blocking code in a different OS thread without blocking the OS thread that the event loop runs in.

> There is currently no way to schedule coroutines or callbacks directly from a different process (such as one started with multiprocessing). The Event Loop Methods section lists APIs that can read from pipes and watch file descriptors without blocking the event loop. In addition, asyncio’s Subprocess APIs provide a way to start a process and communicate with it from the event loop. Lastly, the aforementioned loop.run_in_executor() method can also be used with a concurrent.futures.ProcessPoolExecutor to execute code in a different process.
