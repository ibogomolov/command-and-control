import sys

from program.executor import PlaybookExecutor
from program.playbook import Playbook

if __name__ == '__main__':
    playbook = Playbook.from_file(sys.argv[1])
    executor = PlaybookExecutor(playbook)
    executor.execute()
