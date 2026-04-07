from models.endpoint import Endpoint

class OASParser:
    def __init__(self, spec: dict):
        self.spec = spec
        self.version = self._detect_version()

    def _detect_version(self) -> str:
        if 'swagger' in self.spec:
            return '2.0'
        return '3.x'

    def parse_endpoints(self) -> list[Endpoint]:
        endpoints = []
        for path, methods in self.spec.get('paths', {}).items():
            for method, details in methods.items():
                if method in ['get','post','put','delete','patch']:
                    endpoints.append(Endpoint(
                        path=path,
                        method=method.upper(),
                        operation_id=details.get('operationId'),
                        parameters=details.get('parameters', []),
                        request_body=details.get('requestBody'),
                        responses=details.get('responses', {}),
                        tags=details.get('tags', [])
                    ))
        return endpoints