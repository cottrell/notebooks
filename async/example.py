import asyncio
import time

# probably not safe?
state = dict()
state['a'] = 1
state['b'] = 1

loop = asyncio.get_event_loop()

def get_state():
    return state

def update_a(d=state):
    while True:
        time.sleep(3)
        d['a'] += 1

def update_b(d=state):
    while True:
        time.sleep(1)
        d['b'] += 1

def start(executor=None):
    return loop.run_in_executor(executor, update_a)
