import atexit

f = open(f"bench/bench.out", "w")

def log(line):
    #global f
    f.write(f"\n{line}")

def exit_handler():
    f.close()

atexit.register(exit_handler)