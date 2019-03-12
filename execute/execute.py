import collections
import os
import shlex
import subprocess
import sys
import threading

from pyreto import defaults, export
from pyreto.compat import string_type, to_binary


Result = collections.namedtuple('Result', 'exit_code stdout stderr')


@export
@defaults(stdin=None, timeout=None, sigterm_timeout=3)
def execute(command, stdin, timeout, sigterm_timeout):
    if isinstance(command, string_type) and os.name != 'nt':
        command = shlex.split(command)
    execution = Execution(command, stdin)
    thread = threading.Thread(target=execution.run)
    thread.start()
    thread.join(timeout)
    if execution.error is not None:
        raise execution.error
    if execution.process is not None and execution.exit_code is None:
        execution.process.terminate()
        # If the process doesn't respond to SIGTERM, use SIGKILL.
        thread.join(sigterm_timeout)
        if execution.exit_code is None:
            execution.process.kill()
        thread.join()
    return Result(execution.exit_code, execution.stdout, execution.stderr)


class Execution(object):
    
    def __init__(self, command, stdin):
        self.command = command
        self.stdin = to_binary(stdin)
        self.error = None
        self.process = None
        self.stdout = None
        self.stderr = None
        self.exit_code = None

    def run(self):
        try:
            self.process = subprocess.Popen(
                self.command,
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
            )
        except Exception as error:
            if sys.version_info.major >= 3:
                self.error = error
            else:
                self.error = sys.exc_info()
            return
        self.stdout, self.stderr = self.process.communicate(self.stdin)
        self.exit_code = self.process.returncode
