import networkx as nx

class DependencyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_dependency(self, from_ep, to_ep, dep_type):
        self.graph.add_edge(
            f"{from_ep.method} {from_ep.path}",
            f"{to_ep.method} {to_ep.path}",
            type=dep_type.value
        )

    def get_chains(self):
        return list(nx.topological_sort(self.graph))

    def detect_cycles(self):
        return list(nx.simple_cycles(self.graph))