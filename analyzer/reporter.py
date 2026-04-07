import json
from rich.console import Console
from rich.table import Table

class Reporter:
    def __init__(self, dependencies):
        self.deps = dependencies
        self.console = Console()

    def print_table(self):
        table = Table(title="API Dependencies")
        table.add_column("Type")
        table.add_column("From")
        table.add_column("To / Info")
        for dep in self.deps:
            table.add_row(str(dep.get('type','')), str(dep.get('from','')), str(dep.get('to','')))
        self.console.print(table)

    def to_json(self, outfile='report.json'):
        with open(outfile, 'w') as f:
            json.dump(self.deps, f, indent=2, default=str)