import subprocess

if __name__ == '__main__':

    HOST = "localhost"
    # Ports are handled in ~/.ssh/config since we use OpenSSH
    COMMAND = "uname -a"

    ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print("ERROR: %s" % error)
    else:
        print(result)
