from cachi2.core.models.input import Request
from cachi2.core.models.output import Component, EnvironmentVariable, RequestOutput
from cachi2.core.package_managers.yarn.utils import run_yarn_cmd
from cachi2.core.rooted_path import RootedPath


def fetch_yarn_source(request: Request) -> RequestOutput:
    """Process all the yarn source directories in a request."""
    components: list[Component] = []

    for package in request.yarn_classic_packages:
        path = request.source_dir.join_within_root(package.path)
        request.output_dir.join_within_root("deps/yarn-classic").path.mkdir(
            parents=True, exist_ok=True
        )
        _fetch_dependencies(path, _get_prefetch_environment_variables(request.output_dir))

    return RequestOutput.from_obj_list(
        components, _generate_build_environment_variables(), project_files=[]
    )


def _fetch_dependencies(source_dir: RootedPath, env: dict[str, str]) -> None:
    """Fetch dependencies using 'yarn install'.

    :param source_dir: the directory in which the yarn command will be called.
    :param env: environment variable mapping used for the prefetch.
    :raises PackageManagerError: if the 'yarn install' command fails.
    """
    run_yarn_cmd(
        [
            "install",
            "--disable-pnp",
            "--frozen-lockfile",
            "--ignore-engines",
            "--no-default-rc",
            "--non-interactive",
        ],
        source_dir,
        env,
    )


def _get_prefetch_environment_variables(output_dir: RootedPath) -> dict[str, str]:
    """Get environment variables that will be used for the prefetch."""
    return {
        "COREPACK_ENABLE_DOWNLOAD_PROMPT": "0",
        "COREPACK_ENABLE_PROJECT_SPEC": "0",
        "YARN_IGNORE_PATH": "true",
        "YARN_IGNORE_SCRIPTS": "true",
        "YARN_YARN_OFFLINE_MIRROR": str(output_dir.join_within_root("deps/yarn-classic")),
        "YARN_YARN_OFFLINE_MIRROR_PRUNING": "false",
    }


def _generate_build_environment_variables() -> list[EnvironmentVariable]:
    """Generate environment variables that will be used for building the project."""
    env_vars = {
        "YARN_YARN_OFFLINE_MIRROR": "${output_dir}/deps/yarn-classic",
        "YARN_YARN_OFFLINE_MIRROR_PRUNING": "false",
    }

    return [EnvironmentVariable(name=key, value=value) for key, value in env_vars.items()]
