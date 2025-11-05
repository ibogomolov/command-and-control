import tempfile
from typing import List
from unittest import TestCase

import yaml


class FileTestCase(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_playbook_file_from_json(self, content: List):
        self.playbook_file = f"{self.temp_dir.name}/playbook.yaml"
        with open(self.playbook_file, "w") as yaml_file:
            yaml.dump(content, yaml_file)

    def create_hosts_file_from_text(self, content: str):
        self.hosts_file = f"{self.temp_dir.name}/hosts"
        with open(self.hosts_file, "w") as text_file:
            text_file.write(content)
