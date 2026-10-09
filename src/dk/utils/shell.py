import subprocess


def run_cmd(cmd, **kwargs):
    """Run shell commands."""
    process = subprocess.run(cmd, capture_output=True, text=True, **kwargs)

    process.stdout = process.stdout.strip("\n")
    process.stderr = process.stderr.strip("\n")

    return process
