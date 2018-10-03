from commands import Command
from commands.shell.EgeShell import EgeShell
from threading import Thread


class EgeShellCommand(Command):

    def __init__(self, group):
        super().__init__()
        self._triggers = ['ege', 'Ege']
        self._group = group

    def proceed(self, member, message, attachments, group, *args, **kwargs):
        command = command.split()
        if user and (command[0] in self._triggers):
            shell = EgeShell(self._group, user)
            if not args:
                t = Thread(target=shell.shell_execute, args=(*args,))
                t.start()
                while True:
                    if not t.is_alive():
                        unlock = kwargs.get('unlock')
                        print(user.id)
                        unlock(user.id)
                        return 'IGNORE'
        return False

if __name__ == '__main__':
    pass