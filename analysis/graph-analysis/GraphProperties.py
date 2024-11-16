import os
import re
import pandas as pd
from unified_planning.engines import CompilationKind
from pypmt.apis import create_encoder
from unified_planning.io import PDDLReader
from pypmt.encoders.basic import EncoderForallLazy
import networkx as nx


def analyze_graph(G, domain_name, instance_name):
    instance = int(re.sub(r'\D', '', instance_name))
    properties = {
        "Domain": domain_name,
        "Instance": instance,
        "Number of nodes": G.number_of_nodes(),
        "Number of edges": G.number_of_edges(),
        "Graph density": nx.density(G),
        "Max no. Edges Possible": G.number_of_nodes() * (G.number_of_nodes() - 1) / 2,
    }
    degrees = dict(G.degree())
    if properties["Number of nodes"] > 0:
        avg_degree = sum(degrees.values()) / properties["Number of nodes"]
        max_degree_node, max_degree = max(G.degree(), key=lambda x: x[1])
        properties["Node with highest degree"] = max_degree_node
        properties["Highest degree"] = max_degree
        properties["Average degree"] = avg_degree
    else:
        properties["Average degree"] = 0
    return properties



domains = {"rovers-classical"}

results = []

def get_properties(directory_path, max_instance):
    for item in os.listdir(directory_path):
        if item in domains:
            item_path = os.path.join(directory_path, item)
            domain_file = os.path.join(item_path, "domain.pddl")
            for file in os.listdir(item_path):
                if file != "domain.pddl" and file.endswith(".pddl"):
                    instance = re.sub(r'\D', '', file)
                    if int(instance) < max_instance:
                        compilation_list = [
                            ('up_quantifiers_remover', CompilationKind.QUANTIFIERS_REMOVING),
                            ('up_disjunctive_conditions_remover', CompilationKind.DISJUNCTIVE_CONDITIONS_REMOVING),
                            ('up_grounder', CompilationKind.GROUNDING)
                        ]
                        # Mimic the solver calling the modifier
                        problem_file = os.path.join(item_path, file)
                        task = PDDLReader().parse_problem(domain_file, problem_file)
                        encoder, _ = create_encoder(EncoderForallLazy, task, compilation_list)
                        encoder.create_variables(0)
                        encoder.encode_execution_semantics()
                        graph = encoder.modifier.graph
                        properties = analyze_graph(graph, item, file)
                        results.append(properties)


get_properties("domains/classical", 20 )
# get_properties("../../domains/numeric", 10 )
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by=['Instance'])
results_df.to_csv("graph_properties.csv", index=False)
