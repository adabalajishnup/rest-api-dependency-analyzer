from models.dependency_types import DependencyType

class DependencyAnalyzer:
    def __init__(self, endpoints, trie):
        self.endpoints = endpoints
        self.trie = trie

    def find_hierarchical(self):
        # Use trie traversal
        return self.trie.find_hierarchical_deps()

    def find_operational(self):
        # POST /x must come before GET /x/{id}
        deps = []
        path_map = {}
        for ep in self.endpoints:
            base = ep.path.split('{')[0].rstrip('/')
            path_map.setdefault(base, []).append(ep)
        for base, eps in path_map.items():
            methods = {e.method: e for e in eps}
            if 'POST' in methods and 'GET' in methods:
                deps.append({'type': DependencyType.OPERATIONAL,
                             'from': methods['POST'], 'to': methods['GET']})
        return deps

    def find_workflow(self):
        # POST → PUT → DELETE on same resource = workflow
        deps = []
        path_map = {}
        for ep in self.endpoints:
            base = ep.path.split('{')[0].rstrip('/')
            path_map.setdefault(base, []).append(ep)
        for base, eps in path_map.items():
            methods = {e.method: e for e in eps}
            sequence = [methods.get(m) for m in ['POST','GET','PUT','DELETE'] if m in methods]
            if len(sequence) >= 2:
                deps.append({'type': DependencyType.WORKFLOW, 'sequence': sequence})
        return deps

    def find_inter_parameter(self):
        # If two params share a name across endpoints, they're likely linked
        deps = []
        param_index = {}
        for ep in self.endpoints:
            for param in ep.parameters:
                name = param.get('name')
                param_index.setdefault(name, []).append(ep)
        for name, eps in param_index.items():
            if len(eps) > 1:
                deps.append({'type': DependencyType.INTER_PARAM,
                             'param': name, 'endpoints': eps})
        return deps