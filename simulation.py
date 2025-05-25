import traci
from time import perf_counter


def run_simulation(sumo_cfg_file):
    start = perf_counter()
    cmd = ["sumo", "-c", sumo_cfg_file, "--no-step-log=true"]
    traci.start(cmd)

    step = 0
    while step < 28800:
        traci.simulationStep()
        step += 1

        # pārbauda vai kurjeri vēl ir sistēmā:
        stop = True
        for vehicle in traci.vehicle.getIDList():
            if vehicle.startswith("c"):
                stop = False
                break
        if stop:
            print(f"All couriers have left the simulation (step={step})")
            break

    traci.close()
    end = perf_counter()
    print(f"run_simulation({sumo_cfg_file}) spent {end - start} seconds")


if __name__ == "__main__":
    print("manual simulation")
    # run_simulation("riga.sumo.cfg")
    # run_simulation("experiments/experiment_10_1/experiment.sumo.cfg")
    # run_simulation("experiments/experiment_2_4/experiment.sumo.cfg")
    # run_simulation("experiments/experiment_2_5/experiment.sumo.cfg")
