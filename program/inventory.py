import configparser
from typing import Dict, Iterable, List


class Inventory:
    """An internal representation of a hosts file"""

    def __init__(self) -> None:
        self._hosts: Dict[str, List[str]] = {}

    @staticmethod
    def from_file(filepath: str) -> Inventory:
        try:
            with open(filepath, "r") as file:
                config = configparser.ConfigParser(allow_no_value=True, empty_lines_in_values=False, interpolation=None)
                config.read_file(file)
        except configparser.DuplicateOptionError:
            raise InventoryException("Hosts file contains duplicate host in a group")
        except configparser.DuplicateSectionError:
            raise InventoryException("Hosts file contains duplicate groups")
        except configparser.MissingSectionHeaderError:
            raise InventoryException("Hosts file contains hosts declared outside of a group")
        except configparser.ParsingError as e:
            raise InventoryException(f"Error while parsing the hosts file: {e.message}")

        inventory = Inventory()
        for group in config.sections():
            inventory._hosts[group] = []
            for host in config[group]:
                inventory._hosts[group].append(host)

        return inventory

    def get_hosts_by_group(self, group: str) -> Iterable[str]:
        if group not in self._hosts:
            raise InventoryException(f"Group '{group}' is absent from the hosts file")
        elif len(self._hosts[group]) == 0:
            raise InventoryException(f"Group '{group}' has no hosts")

        return self._hosts[group]


class InventoryException(Exception):
    """An exception raised when an error occurs during an inventory operation"""
    pass
