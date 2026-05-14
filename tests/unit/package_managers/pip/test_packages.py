# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path

import pypi_simple
import pytest

from hermeto.core.package_managers.pip.packages import (
    PyPIPackage,
    URLPackage,
    VCSPackage,
)

CUSTOM_PYPI_ENDPOINT = "https://my-pypi.org/simple/"
GIT_REF = "a" * 40

_PATH = Path("/deps/pip/pkg.tar.gz")
_REQ_FILE = "requirements.txt"


@pytest.mark.parametrize(
    "dep, expected_purl",
    [
        (
            PyPIPackage(
                package="pypi_package",
                path=_PATH,
                requirement_file=_REQ_FILE,
                missing_req_file_checksum=False,
                package_type="sdist",
                version="1.0.0",
                index_url=pypi_simple.PYPI_SIMPLE_ENDPOINT,
            ),
            "pkg:pypi/pypi-package@1.0.0",
        ),
        (
            PyPIPackage(
                package="mypypi_package",
                path=_PATH,
                requirement_file=_REQ_FILE,
                missing_req_file_checksum=False,
                package_type="sdist",
                version="2.0.0",
                index_url=CUSTOM_PYPI_ENDPOINT,
            ),
            f"pkg:pypi/mypypi-package@2.0.0?repository_url={CUSTOM_PYPI_ENDPOINT}",
        ),
        (
            VCSPackage(
                package="git_dependency",
                path=_PATH,
                requirement_file=_REQ_FILE,
                missing_req_file_checksum=False,
                package_type="sdist",
                url="https://github.com/my-org/git_dependency",
                ref=GIT_REF,
                host="github.com",
                namespace="my-org",
                repo="git_dependency",
            ),
            f"pkg:pypi/git-dependency?vcs_url=git%2Bhttps://github.com/my-org/git_dependency%40{GIT_REF}",
        ),
        (
            VCSPackage(
                package="Git_dependency",
                path=_PATH,
                requirement_file=_REQ_FILE,
                missing_req_file_checksum=False,
                package_type="sdist",
                url="file:///github.com/my-org/git_dependency",
                ref=GIT_REF,
                host="",
                namespace="github.com/my-org",
                repo="git_dependency",
            ),
            f"pkg:pypi/git-dependency?vcs_url=git%2Bfile:///github.com/my-org/git_dependency%40{GIT_REF}",
        ),
        (
            VCSPackage(
                package="git_dependency",
                path=_PATH,
                requirement_file=_REQ_FILE,
                missing_req_file_checksum=False,
                package_type="sdist",
                url="ssh://git@github.com/my-org/git_dependency",
                ref=GIT_REF,
                host="github.com",
                namespace="my-org",
                repo="git_dependency",
            ),
            f"pkg:pypi/git-dependency?vcs_url=git%2Bssh://git%40github.com/my-org/git_dependency%40{GIT_REF}",
        ),
        (
            VCSPackage(
                package="git_dependency",
                path=_PATH,
                requirement_file=_REQ_FILE,
                missing_req_file_checksum=False,
                package_type="sdist",
                url="https://github.com/my-org/git_dependency",
                ref=GIT_REF,
                host="github.com",
                namespace="my-org",
                repo="git_dependency",
            ),
            f"pkg:pypi/git-dependency?vcs_url=git%2Bhttps://github.com/my-org/git_dependency%40{GIT_REF}",
        ),
        (
            URLPackage(
                package="https_dependency",
                path=_PATH,
                requirement_file=_REQ_FILE,
                missing_req_file_checksum=False,
                package_type="sdist",
                original_url=f"https://github.com/my-org/https_dependency/{GIT_REF}/file.tar.gz",
                checksum="sha256:de526c1",
            ),
            f"pkg:pypi/https-dependency?checksum=sha256:de526c1&download_url=https://github.com/my-org/https_dependency/{GIT_REF}/file.tar.gz",
        ),
    ],
)
def test_make_purl(dep: PyPIPackage | VCSPackage | URLPackage, expected_purl: str) -> None:
    assert dep._make_purl() == expected_purl
