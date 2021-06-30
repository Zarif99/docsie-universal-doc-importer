import json
import os.path
from collections import Mapping
from pathlib import Path
from typing import List


class RepositoryMap(Mapping):
    """Represents a JSON view of a git repository file structure.

    >>> repo_map = RepositoryMap('repo')
    >>> repo_map.add_path('path/to/file.txt')
    >>> repo_map.add_path('path/to/another_file.txt')
    >>> repo_map
    <RepositoryMap at 0x1063dc700> JSON: {
      "test": [
        {
          "path": [
            {
              "to": [
                "file.txt",
                "another_file.txt"
              ]
            }
          ]
        }
      ]
    }
    """

    def __init__(self, repo_name: str, filter_extensions: List[str] = None):
        self.repo_name = repo_name
        self.filter_extensions = filter_extensions or []

        self._repo_map = {self.repo_name: []}

    def add_path(self, path: str) -> None:
        """Add a path to the repository map."""
        *path_bits, file = Path(path).parts

        # Do not add the path if its extension is not listed in allowed extensions
        extension = os.path.splitext(file)[1][1:]
        if extension not in self.filter_extensions:
            return

        current_path = self[self.repo_name]
        for bit in path_bits:
            # Get the first dict which contains a `bit` key.
            folder = next(
                (folder for index, folder in enumerate(current_path)
                 if isinstance(folder, dict) and bit in folder),
                None
            )
            if folder is None:
                folder = {bit: []}
                current_path.append(folder)

            current_path = folder[bit]

        # Do not add a file if it already exists
        if file not in current_path:
            current_path.append(file)

    def __getitem__(self, key):
        return self._repo_map[key]

    def __iter__(self):
        return iter(self._repo_map)

    def __len__(self):
        return len(self._repo_map)

    def __str__(self):
        return json.dumps(
            self.as_dict(),
            sort_keys=True,
            indent=2,
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} at {hex(id(self))}> JSON: {self}"

    def as_dict(self) -> dict:
        """Return the repo map as a dictionary.

        It can be useful in some cases,
        where the :class:`Mapping` is not supported or does not act like a default dict,
        but calling a `dict()` function is unwanted due to performance issues.
        """
        return self._repo_map.copy()
