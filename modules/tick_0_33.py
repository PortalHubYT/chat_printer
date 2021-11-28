import time
from .logger import log

TPS = 0.33

cycle_time = 1 / TPS
remainer = 0


def run(called_at_time: float) -> None:

    global remainer

    if remainer > cycle_time:
        
        log(int(cycle_time))
        print(int(cycle_time))
        remainer = 0
        # remainer = remainer - cycle_time
    else:
        remainer += time.time() - called_at_time
