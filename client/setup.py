from pathlib import Path

from setuptools import find_namespace_packages, setup

BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt")) as file:
    required_packages = [ln.strip() for ln in file.readlines()]

style_packages = ["black==22.12.0", "flake8==6.0.0", "isort==5.11.4", "pydocstyle==6.2.3"]

security_packages = ["bandit==1.7.0"]

git_checks_packages = ["pre-commit==2.21.0"]

setup(
    name="grpc-server-python",
    version=1.0,
    description="A project using grpc",
    author="Fernando de Lima",
    python_requires=">=3.10",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={
        "dev": style_packages
        + security_packages
        + git_checks_packages
    }
)