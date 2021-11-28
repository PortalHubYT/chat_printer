import os

TPS_RANGE = 1000

f = open(f"{os.getcwd()}/{TPS_RANGE}tps.reference", "w")


out = ""


class Tick():
    def __init__(self, tps,):
        self.tps = tps
    def tack(self, t):
        global out

        if t % self.tps == 0:
            s = f"{int(TPS_RANGE / self.tps)}"
            out = f"{out}\n{s}"
            #print(s)


#fake_ticks = [ Tick(x) for x in range(1, TPS_RANGE + 1) ]
fake_ticks = [Tick(1), Tick(20), Tick(1000)]


for x in range(1,5000):

    for tick in fake_ticks:
        tick.tack(x)






f.write(out)
f.close()