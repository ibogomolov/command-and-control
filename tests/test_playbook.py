from program.playbook import Playbook, Task, PlaybookException
from tests.fixtures import FileTestCase


class TestPlaybook(FileTestCase):
    def test_from_file_success(self):
        playbook_json = [{"hosts": "dbservers",
                          "tasks": [
                              {"name": "Server uptime",
                               "bash": "uptime"},
                              {"name": "Server disk usage",
                               "bash": "du -h"}]
                          }]
        self.create_playbook_file_from_json(playbook_json)

        pb = Playbook.from_file(self.playbook_file)
        self.assertEqual(pb.hosts_group, "dbservers")
        self.assertListEqual(pb.tasks,
                             [Task(name="Server uptime", command="uptime"),
                              Task(name="Server disk usage", command="du -h")])

    def test_from_file_2_playbooks_in_the_file(self):
        playbook_json = [{"hosts": "dbservers",
                          "tasks": [
                              {"name": "Server uptime",
                               "bash": "uptime"}]
                          },
                         {"hosts": "webservers",
                          "tasks": [
                              {"name": "Server disk usage",
                               "bash": "du -h"}]
                          }]
        self.create_playbook_file_from_json(playbook_json)

        with self.assertRaises(PlaybookException) as context:
            Playbook.from_file(self.playbook_file)

        self.assertEqual(str(context.exception), "Require exactly one playbook per file. Found 2")
