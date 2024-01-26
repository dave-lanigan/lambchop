import functools
import importlib
import inspect
import sys
from pathlib import Path

import anyio
import dill
from anyio.abc import SocketAttribute

from http.server import BaseHTTPRequestHandler, HTTPServer

from lambchop.datastructures import Task


class Server:
    def __init__(self, port: int = 1956) -> None:
        self.port = port
        self.jobs = 0
    
    def deserialize(self, task: Task) -> None:
        return dill.loads(task)

    def get_fun(self, task: Task) -> None:
        f = Path(task.file)
        sys.path.append(str(f.parent))
        module = importlib.import_module(f.stem)
        return getattr(module, task.func)

    async def execute(self, msg) -> None:
        task: Task = self.deserialize(msg)

        func = self.get_fun(task)
        args = task.args
        kwargs = task.kwargs

        if inspect.iscoroutinefunction(func):
            await func(*args, **kwargs)
        else:
            if kwargs:  # pragma: no cover
                # run_sync doesn't accept 'kwargs', so bind them in here
                func = functools.partial(func, **kwargs)
            await anyio.to_thread.run_sync(func, *args)
        return b"COMPLETED"

    async def handle(self, client):
        async with client:
            addr = client.extra(SocketAttribute.remote_address)
            print(f"receiving message from: {addr}")
            msg = await client.receive()
            
            if msg == b"PING":
                await client.send(b"PONG")
                return

            if
            
            try:
                self.jobs += 1
                print("Number of jobs: ", self.jobs)
                msg = await self.execute(msg)
                self.jobs -= 1
                
                await client.send(msg)
            except Exception as e:
                print(e)
                await client.send(b"ERROR")

    async def serve(self):
        print("Starting server.")
        listener = await anyio.create_tcp_listener(local_port=self.port)
        print(f"Listening on port: {self.port}")
        await listener.serve(self.handle)


if __name__ == "__main__":
    s = Server()
    anyio.run(s.serve)
