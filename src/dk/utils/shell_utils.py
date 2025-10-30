import subprocess

from .rich_utils import out


def run_cmd(cmd, print_output=False, return_output=False, **kwargs):
    """Run shell commands."""
    process = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    output = process.stderr.strip() or process.stdout.strip()

    if print_output:
        out(output)

    if return_output:
        return output

    return process
