from modules.commands.interface.ICommand import ICommand


class AboutCommand(ICommand):

    def __init__(self):
        super().__init__()
        self._triggers = ['about', 'About']

    def proceed(self, *args, **kwargs):
        if len(args) > 0 and args[1] in self._triggers:
            about = """
(C) Morris Bot, 2018

Моррис изначально представлялся в воображении обычным скриптом на ~100-200 строк, который только и может, что пересылать сообщения от администраторов. 
Нутро, однако, посчитало, что этого мало, и вот Вы видите то, что видите...

Посмотреть и оценить (это обязательно :D) Вы можете на моём аккаунте Github:
- https://github.com/nogip/morris

А связаться со мной через:
- Vk: vk.com/nogip
- Instagram: instagram.com/balzph 

Developed by Mamatkazin Karim, г.Сочи
        """
            return about
        return False
