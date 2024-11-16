import networkx as nx
from matplotlib import pyplot as plt
from unified_planning.io import PDDLReader

from pypmt.encoders.basic import EncoderGrounded

from pypmt.modifiers.modifierParallel import ParallelModifier

domain = "/Users/lukeroooney/Desktop/Dissertation/parallelSAT/numeric-domains/counters/domain.pddl"
problem = "/Users/lukeroooney/Desktop/Dissertation/parallelSAT/numeric-domains/counters/instances/fz_instance_2.pddl"

modifier = ParallelModifier(True, True)
task = PDDLReader().parse_problem(domain, problem)
encoder = EncoderGrounded("", task, modifier)
action_vars = list(map(lambda x: x[0], encoder.up_actions_to_z3.values()))

modifier.encode(encoder, action_vars)

G = modifier.graph

plt.figure(figsize=(8, 8))
pos = nx.kamada_kawai_layout(G)
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightgrey",
    edge_color="black",
    node_size=7000,
    font_size=10,
    edgecolors = "black",
    linewidths = 1.5
)
plt.title("Graph Representation of the Modifier")
plt.show()

