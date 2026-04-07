from enum import Enum

class DependencyType(Enum):
    HIERARCHICAL = "hierarchical"     # /users → /users/{id}
    OPERATIONAL  = "operational"      # POST /users before GET /users/{id}
    WORKFLOW     = "workflow"         # sequence: create → update → delete
    INTER_PARAM  = "inter_parameter"  # param A's value constrains param B