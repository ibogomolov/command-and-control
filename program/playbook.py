from dataclasses import dataclass
from typing import List

import yaml


@dataclass
class Task:
    name: str
    command: str


class Playbook:
    def __init__(self) -> None:
        self.hosts_group = ""
        self.tasks: List[Task] = []

    @staticmethod
    def from_file(filepath: str) -> Playbook:
        try:
            with open(filepath, "r") as file:
                content = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise PlaybookException(f"Error while parsing the playbook file: {str(e)}")

        if len(content) != 1:
            raise PlaybookException(f"Require exactly one playbook per file. Found {len(content)}")
        # From this point it is expected that playbook format is correct

        playbook = Playbook()
        playbook.hosts_group = content[0]["hosts"]
        for task in content[0]["tasks"]:
            playbook.tasks.append(Task(task["name"], task["bash"]))

        return playbook


class PlaybookException(Exception):
    """An exception raised when an error occurs during parsing of a playbook file"""
    pass
