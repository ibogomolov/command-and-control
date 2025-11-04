import subprocess
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Tuple

from program.inventory import Inventory
from program.playbook import Playbook, Task

HOSTS_FILE_LOCATION = "/etc/playbook/hosts"
TASK_TIMEOUT_IN_SECONDS = 30


class PlaybookExecutor:
    def __init__(self, playbook: Playbook):
        self.playbook = playbook
        self.inventory = Inventory.from_file(HOSTS_FILE_LOCATION)

    @staticmethod
    def execute_task(task: Task, host: str) -> Tuple[int, str, str]:
        ssh = subprocess.Popen(["ssh", host, task.command],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=False,
                               text=True)
        outs, _ = ssh.communicate()
        return ssh.returncode, host, outs

    def execute(self) -> None:
        print("Executing playbook...")
        hosts = self.inventory.get_hosts_by_group(self.playbook.hosts_group)
        is_error = False

        with ThreadPoolExecutor(max_workers=5) as executor:
            for task in self.playbook.tasks:
                print(f"\n- Task '{task.name}'\n")
                results = executor.map(partial(self.execute_task, task), hosts, timeout=TASK_TIMEOUT_IN_SECONDS)
                for result in results:
                    rc, host, out = result
                    print(f"* {host}\n{'ERROR ' if rc else ''}{out.strip()}")
                    if rc:
                        is_error = True

                if is_error:
                    print("\nExecution aborted due to an error.")
                    exit(1)

        print("\nExecution completed successfully!")