import os

from enum import Enum
from typing import Optional


class EnvironmentVariables(str, Enum):
    PORT = "PORT"
    HOST = "HOST"
    N_WORKERS = "N_WORKERS"

    def get_env(self, default: Optional[str] = None) -> Optional[str]:
        """Get environ value.

        Args:
            default (Optional[str]): Default value if not present.
            Defaults to None.

        Returns:
            Optional[str]: Value as string. Returns default if not present.
        """

        return os.environ.get(self, default)
