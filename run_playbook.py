import sys

from program.executor import PlaybookExecutor
from program.playbook import Playbook

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <playbook>')
        sys.exit(1)

    playbook = Playbook.from_file(sys.argv[1])
    executor = PlaybookExecutor(playbook)
    executor.execute()
