import argparse
from utils.file_loader import load_spec
from analyzer.parser import OASParser
from analyzer.trie import DependencyTrie
from analyzer.dependency import DependencyAnalyzer
from analyzer.reporter import Reporter

def main():
    parser = argparse.ArgumentParser(description='REST API Dependency Analyzer')
    parser.add_argument('spec', help='Path to OAS YAML/JSON file')
    parser.add_argument('--output', choices=['table','json'], default='table')
    args = parser.parse_args()

    spec = load_spec(args.spec)
    oas_parser = OASParser(spec)
    endpoints = oas_parser.parse_endpoints()

    trie = DependencyTrie()
    for ep in endpoints:
        trie.insert(ep)

    analyzer = DependencyAnalyzer(endpoints, trie)
    deps = (
        analyzer.find_hierarchical() +
        analyzer.find_operational() +
        analyzer.find_workflow() +
        analyzer.find_inter_parameter()
    )

    reporter = Reporter(deps)
    if args.output == 'json':
        reporter.to_json()
    else:
        reporter.print_table()

if __name__ == '__main__':
    main()