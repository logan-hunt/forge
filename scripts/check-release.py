"""Run Forge's local package and isolated behavior checks without activating it."""
import os
from pathlib import Path
import shlex
import subprocess
import sys

package = Path(__file__).resolve().parents[1]
commands = (
    [sys.executable, '-B', str(package / 'scripts/verify-forge.py')],
    [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(package / 'tests'), '-p', 'test_*.py'],
)
for command in commands:
    print(shlex.join(command), flush=True)
    result = subprocess.run(command, cwd=package, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    if result.returncode:
        sys.exit(result.returncode)

print('Local checks passed. Host discovery and agent behavior require the checks in docs/sharing.md.')
