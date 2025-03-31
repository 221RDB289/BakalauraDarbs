import traci


def run_simulation():
    cmd = ["sumo", "-c", "riga.sumo.cfg"]
    traci.start(cmd)

    step = 0
    while step < 10000:  # 10x vairāk soļi, jo cfg failā 1 solis = 0.1
        traci.simulationStep()
        step += 1

    traci.close()


if __name__ == "__main__":
    run_simulation()
