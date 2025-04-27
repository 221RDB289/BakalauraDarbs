import traci


def run_simulation():
    cmd = ["sumo", "-c", "riga.sumo.cfg"]
    traci.start(cmd)

    step = 0
    while step < 28800:
        traci.simulationStep()
        step += 1

    traci.close()


if __name__ == "__main__":
    run_simulation()
