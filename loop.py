import json
import importlib
import time


def game_loop():

    while True:

        time_delta = time.time()

        module_list = []
        with open("schedule.json", "r") as schedule_file:
            schedule = json.load(schedule_file)

            for module in schedule:
                try:
                    module_list.append(
                        importlib.import_module(f"modules.{module}", package="modules")
                    )
                except Exception as e:
                    print(f"{module} failed to load: {e}")
                    exit()

        for module in module_list:
            module.run(time_delta)


game_loop()
