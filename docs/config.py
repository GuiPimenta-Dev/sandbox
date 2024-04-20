from infra.services import Services


class DocsConfig:
    def __init__(self, services: Services) -> None:
        # Swagger at /swagger
        services.api_gateway.create_docs(endpoint="/swagger", mode="swagger", public=True)

        # Redoc at /redoc
        services.api_gateway.create_docs(endpoint="/redoc", mode="redoc", public=True)

        # Architecture Diagram at /diagram
        services.api_gateway.create_docs(endpoint="/diagram", mode="diagram", public=True)

        # Tests Report at /tests
        services.api_gateway.create_docs(endpoint="/tests", mode="tests", public=True)

        # Coverage Report at /coverage
        services.api_gateway.create_docs(endpoint="/coverage", mode="coverage", public=True)
