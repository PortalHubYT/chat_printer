import time

TPS = 1
cycle_time = 1 / TPS

remainer = 0


def run(called_at_time: float) -> None:

    global remainer

    if remainer > cycle_time:
        print("1 second has passed in tick 1")
        print(remainer)
        remainer = 0
    else:
        remainer += time.time() - called_at_time
