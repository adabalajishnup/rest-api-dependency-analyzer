class TrieNode:
    def __init__(self):
        self.children = {}        # segment → TrieNode
        self.endpoints = []       # list of Endpoint objects at this node
        self.is_param = False     # True if segment is {param}

class DependencyTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, endpoint):
        node = self.root
        segments = [s for s in endpoint.path.split('/') if s]
        for seg in segments:
            is_param = seg.startswith('{')
            key = '__PARAM__' if is_param else seg
            if key not in node.children:
                node.children[key] = TrieNode()
                node.children[key].is_param = is_param
            node = node.children[key]
        node.endpoints.append(endpoint)

    def find_hierarchical_deps(self) -> list:
        """Traverse trie; parent node with children = hierarchical dependency."""
        deps = []
        self._traverse(self.root, [], deps)
        return deps

    def _traverse(self, node, path_so_far, deps):
        if node.endpoints and node.children:
            deps.append({
                'parent': '/' + '/'.join(path_so_far),
                'children': list(node.children.keys())
            })
        for seg, child in node.children.items():
            self._traverse(child, path_so_far + [seg], deps)