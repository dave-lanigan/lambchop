import time
from lambchop import SideKick

def long_running_process(x, y):
    print("Starting process 1.")
    time.sleep(x + y)
    print("Completed.")


def long_running_process2(x, y):
    print("Starting process 2.")
    time.sleep(x + y)
    print("Completed.")


def main():
    sk = SideKick()
    sk.add_task(long_running_process, x=5, y=3)
    sk.add_task(long_running_process2, x=5, y=3)
    sk.process()

if __name__ == "__main__":
    main()