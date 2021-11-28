import time
from .logger import log

TPS = 20
cycle_time = 1 / TPS

remainer = 0


def run(called_at_time: float) -> None:

    global remainer

    if remainer > cycle_time:
        log(TPS)
        print(TPS)
        
        remainer = 0
        # remainer = remainer - cycle_time
    else:
        remainer += time.time() - called_at_time
