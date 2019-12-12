import subprocess


def run(command: str) -> str:
    return subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')

