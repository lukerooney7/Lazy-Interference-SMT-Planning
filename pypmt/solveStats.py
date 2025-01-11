import csv
import os


def get_problem(name):
    # instance = int(name.split('_')[-1])
    # domain = name.split('_')[-2]
    return name


def save_stats(planner):
    relevant_attrs = {"propagations", "user-propagations", "decisions", "final-checks", "conflicts"}
    output_file = "./stats.csv"
    file_exists = os.path.isfile(output_file)
    lines = planner.solver.statistics().__str__().strip("()").strip().split("\n")
    stats_dict = {}
    for field in relevant_attrs:
        stats_dict.setdefault(field, 0)
    for line in lines:
        key, value = line.strip().split(maxsplit=1)
        key = key.strip(":")
        if key in relevant_attrs:
            stats_dict[key] = value
    
    name = get_problem(planner.encoder.task.name)
    stats_dict['problem'] = name
    stats_dict['length'] = len(planner.solution)
    stats_dict['steps'] = planner.horizon + 1
    # stats_dict['mutexes'] = len(planner.encoder.modifier.mutexes) + planner.propagator.mutexes
    # stats_dict['instance'] = instance
    stats_dict['propagator'] = planner.propagator.name
    # fieldnames = ['domain', 'length', 'steps', 'mutexes', 'instance', 'propagator']  # Predefined field names
    # for field in fieldnames:
    
    with open(output_file, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=stats_dict.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(stats_dict)