from dataclasses import dataclass
from pathlib import Path

import tomli


class PathNotAFileException(Exception):
    pass


@dataclass(frozen=True)
class Config:
    core_host: str
    core_port: int

    @staticmethod
    def from_toml(path: str | Path):
        if isinstance(path, str):
            path = Path(path)

        if not path.is_file():
            raise PathNotAFileException()

        with path.open("rb") as f:
            config = tomli.load(f)

        return Config(
            core_host=config["core"]["host"],
            core_port=config["core"]["port"],
        )
