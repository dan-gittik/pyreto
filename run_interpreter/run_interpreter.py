from __future__ import print_function

import code
import sys

from pyreto import defaults, export


@export
@defaults(banner=None, exit_message=None, ps1='>>> ', ps2='... ', filename='<interpreter>')
def run_interpreter(banner, exit_message, ps1, ps2, filename, **namespace):
    if banner is not None:
        print(banner)
    interpreter = Interpreter(namespace, ps1, ps2, filename)
    interpreter.interact()
    if exit_message is not None:
        print(exit_message)
    return namespace


class Interpreter(code.InteractiveConsole):

    def __init__(self, namespace, ps1, ps2, filename):
        # code.InteractiveConsole is an old-style class, so it doesn't support super.
        code.InteractiveConsole.__init__(self, namespace, filename)
        self.ps1 = ps1
        self.ps2 = ps2
        self.skip_banner = True

    def interact(self):
        # We print the exit message ourselves, so suppress it if supported.
        if sys.version_info >= (3, 6):
            return code.InteractiveConsole.interact(self, exitmsg='')
        return code.InteractiveConsole.interact(self)

    def write(self, data):
        # We print the banner ourselves, so suppress it (i.e. first write).
        if self.skip_banner:
            self.skip_banner = False
            return
        return code.InteractiveConsole.write(self, data)

    def raw_input(self, prompt):
        # Prompts are hardcoded to sys.ps1/'>>> ' and sys.ps2/'... ', so swap them here.
        if prompt in (sys.ps1, '>>> '):
            prompt = self.ps1
        else:
            prompt = self.ps2
        return code.InteractiveConsole.raw_input(self, prompt)
