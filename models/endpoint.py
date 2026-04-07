from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Endpoint:
    path: str
    method: str                        # GET, POST, PUT, DELETE
    operation_id: Optional[str]
    parameters: List[Dict]
    request_body: Optional[Dict]
    responses: Dict
    tags: List[str] = field(default_factory=list)
    produces: List[str] = field(default_factory=list)