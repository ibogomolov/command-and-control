# command-and-control

A command and control program that allows us to run tasks on multiple servers.

## SSH config

The program uses OpenSSH. This means that ssh connections are configured in ~/.ssh/config and are independent of the
program.

## Playbook execution

The program goes through all the tasks in the playbook one by one. It executes the current task on all the hosts before
moving to the next one. If there is an error during the task execution on any host, the playbook execution is aborted.
Although different behaviours might be desirable in different situations, this execution strategy was chosen as the
default one.

## Running the program

### Prerequisites

- This program was developed using **Python 3.14.0** and it is required to run the program.
- **Poetry** is used to manage dependencies
  and [Python environments](https://python-poetry.org/docs/managing-environments/).


1. Install the required version of python.

```shell
pyenv install 3.14.0
pyenv local 3.14.0
```

2. Create virtualenv and install dependencies.

```shell
poetry install
```

3. Activate project's virtualenv.

```shell
eval $(poetry env activate)
```

4. Update the hosts file and create a playbook. There is a symlink for convenience.

```shell
vim hosts
vim new_playbook.yaml
```

5. Run the playbook. You can use relative or absolute path for the playbook file.

```shell
python run_playbook.py new_playbook.yaml
```
