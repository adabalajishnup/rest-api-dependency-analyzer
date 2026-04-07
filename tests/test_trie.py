import pytest
from analyzer.trie import DependencyTrie
from models.endpoint import Endpoint

def make_endpoint(path, method):
    return Endpoint(
        path=path, method=method,
        operation_id=None, parameters=[],
        request_body=None, responses={}
    )

def test_insert_and_find_hierarchical():
    trie = DependencyTrie()
    trie.insert(make_endpoint('/pets', 'GET'))
    trie.insert(make_endpoint('/pets', 'POST'))
    trie.insert(make_endpoint('/pets/{petId}', 'GET'))

    deps = trie.find_hierarchical_deps()
    assert len(deps) == 1
    assert deps[0]['parent'] == '/pets'

def test_no_hierarchical_for_flat_api():
    trie = DependencyTrie()
    trie.insert(make_endpoint('/pets', 'GET'))
    trie.insert(make_endpoint('/owners', 'GET'))

    deps = trie.find_hierarchical_deps()
    assert len(deps) == 0