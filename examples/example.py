import anyio
import time
from lambchop import SideKick

def long_running_process(x, y):
    print("Starting process.")
    time.sleep(x + y)
    print("Completed.")


async def main():
    sk = SideKick()
    await sk.process(long_running_process, x=5, y=3)
    print("Done sending.")

if __name__ == "__main__":
    anyio.run(main)