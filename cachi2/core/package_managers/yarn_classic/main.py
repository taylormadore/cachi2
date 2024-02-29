from cachi2.core.models.input import Request
from cachi2.core.models.output import Component, EnvironmentVariable, RequestOutput


def fetch_yarn_source(request: Request) -> RequestOutput:
    """Process all the yarn source directories in a request."""
    components: list[Component] = []
    env_vars: list[EnvironmentVariable] = []

    for package in request.yarn_classic_packages:
        pass

    return RequestOutput.from_obj_list(components, env_vars, project_files=[])
