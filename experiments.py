from data.optimization import get_solution
from ortools.constraint_solver import routing_enums_pb2
import os
from data.addresses import get_random_addresses
from get_routes import create_courier_routes

# pirmā atrisinājuma (heiristikas) metode/algoritmi:
first_solution_strategies = [
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC,
    routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC,
    routing_enums_pb2.FirstSolutionStrategy.EVALUATOR_STRATEGY,
    routing_enums_pb2.FirstSolutionStrategy.SAVINGS,
    routing_enums_pb2.FirstSolutionStrategy.SWEEP,
    routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES,
    routing_enums_pb2.FirstSolutionStrategy.ALL_UNPERFORMED,
    routing_enums_pb2.FirstSolutionStrategy.BEST_INSERTION,
    routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION,
    routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_INSERTION,
    routing_enums_pb2.FirstSolutionStrategy.GLOBAL_CHEAPEST_ARC,
    routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_ARC,
    routing_enums_pb2.FirstSolutionStrategy.FIRST_UNBOUND_MIN_VALUE,
]


# lokālā atrisinājuma (metaheiristikas) metodes/algoritmi:
local_search_metaheuristics = [
    routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT,
    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH,
    routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING,
    routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH,
    routing_enums_pb2.LocalSearchMetaheuristic.GENERIC_TABU_SEARCH,
]


def create_experiemnt_trips():
    if not os.path.exists("experiments"):
        os.mkdir("experiments")
    # visiem eksperiemntiem vienādās vērtības:
    addresses = get_random_addresses(x=100, new=False)
    depot_address = "Plieņciema iela 35"
    courier_count = 4
    max_distance_m = 100000  # maksimālais nobraukšanas daudzums (m) katram kurjeram
    solution_minutes = 60  # 1 minūte, lai atrastu optimālo risinājumu
    # eksperimentu veidošana:
    i = 1
    for first_solution_strategy in first_solution_strategies:
        for local_search_metaheuristic in local_search_metaheuristics:
            print(
                f"EXPERIEMNT {i} ({first_solution_strategy}_{local_search_metaheuristic})"
            )
            folder = f"experiments/experiment_{first_solution_strategy}_{local_search_metaheuristic}"
            get_solution(
                depot_address=depot_address,
                addresses=addresses,
                folder=folder,
                courier_count=courier_count,
                max_distance_m=max_distance_m,
                first_solution_strategy=first_solution_strategy,
                local_search_metaheuristic=local_search_metaheuristic,
                solution_minutes=solution_minutes,
            )
            i += 1


import sys


def create_experiment_routes():
    for first_solution_strategy in first_solution_strategies:
        for local_search_metaheuristic in local_search_metaheuristics:
            folder = f"experiments/experiment_{first_solution_strategy}_{local_search_metaheuristic}"
            if os.path.exists(folder):
                create_courier_routes(folder)
                print(
                    f"ROUTES ({first_solution_strategy}_{local_search_metaheuristic})"
                )


def create_sumo_cfgs():
    sumo_cfg_template = "riga.sumo.cfg"
    with open(sumo_cfg_template, "r") as f:
        sumo_cfg = f.read()
    for first_solution_strategy in first_solution_strategies:
        for local_search_metaheuristic in local_search_metaheuristics:
            folder = f"experiments/experiment_{first_solution_strategy}_{local_search_metaheuristic}"
            if os.path.exists(folder):
                experiment_sumo_cfg = sumo_cfg.replace(
                    "simulation_files/courier.rou.xml", f"{folder}/courier.rou.xml"
                )
                experiment_sumo_cfg = sumo_cfg.replace("output/", f"{folder}/output/")
                if not os.path.exists(f"{folder}/output/"):
                    os.mkdir(f"{folder}/output/")
                with open(f"{folder}/riga.sumo.cfg", "w") as f:
                    f.write(experiment_sumo_cfg)
                print(
                    f"SUMO CFG ({first_solution_strategy}_{local_search_metaheuristic})"
                )


import time

if __name__ == "__main__":
    # create_experiemnt_trips()
    # create_experiment_routes()
    create_sumo_cfgs()

    # create_experiment_routes()
    # first_solution_strategy = 3
    # local_search_metaheuristic = 2
    # folder = (
    #     f"experiments/experiment_{first_solution_strategy}_{local_search_metaheuristic}"
    # )
    # if os.path.exists(folder):
    #     if os.path.exists(folder + "/courier.rou.xml"):
    #         os.remove(folder + "/courier.rou.xml")
    #     create_courier_routes(folder)
    #     print(f"ROUTES ({first_solution_strategy}_{local_search_metaheuristic})")
