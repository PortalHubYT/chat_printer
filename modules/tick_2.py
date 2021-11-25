import time

TPS = 0.33

cycle_time = 1 / TPS
remainer = 0


def run(called_at_time: float) -> None:

    global remainer

    if remainer > cycle_time:
        print("3 second has passed in tick 2\n")
        remainer = 0
    else:
        remainer += time.time() - called_at_time
