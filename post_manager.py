import datetime
import logging
import vk_api
import re
import os

run_dir = '{}/'.format(os.path.split(__file__)[0])
logging.basicConfig(
    format='%(asctime)s|| %(funcName)20s:%(lineno)-3d|| %(message)s',
    level=logging.INFO,
    filename=run_dir + 'bot.log',
    filemode='w')


class Note:
    def __init__(self):
        self.name = ''
        self.dz = ''
        self.date = datetime.datetime.today()

    def __str__(self):
        return '\n{} \n# {}\n@ {}'.format(self.name.upper(),
                                          '{}, {}'.format(self.weekday(self.get_calendar()[2]), self.date),
                                          self.dz)

    @staticmethod
    def weekday(wday):
        return {
            1: "Понедельник",
            2: "Вторник",
            3: "Среда",
            4: "Четверг",
            5: "Пятница",
            6: "Суббота",
        }.get(wday)

    def get_calendar(self):
        return self.date.isocalendar()


class PostManager:

    def __init__(self, login, password, group_id):
        self.login = ''
        self.password = ''
        self.vk = vk_api.VkApi(login, password)
        self.group_id = group_id
        self.recent_notes = []
        self.last_id = 0
        self.auth()

    def auth(self):
        try:
            self.vk.auth()
        except vk_api.ApiError as error:
            logging.info(error)

    def sort(self, result):
        return sorted(result, key=self.sortByDate)

    @staticmethod
    def sortByDate(note):
        return note.date.timetuple().tm_yday

    @staticmethod
    def parse_lessons(text):
        calendar = '📅'
        books = '📚'
        name_sep = '#'
        lessons = text.rsplit('_')
        notes = []

        for lesson in lessons:
            note = Note()
            try:
                note.name = re.search(name_sep + " ?[А-я ]*", lesson).group().strip("# \n")
                date = re.search(calendar + " ?[^`]*{}".format(books), lesson).group().strip(
                    "{}{} \n".format(calendar, books))
                date = datetime.datetime.strptime(date, '%d.%m.%y').date()
                note.date = date
                note.dz = re.search(books + " ?[^`]*\n?", lesson).group().strip("{} \n".format(books))
                notes.append(note)
            except:
                continue

        return notes

    def update_posts(self, group_id, count):
        posts = self.vk.method('wall.get', {'domain': group_id, 'count': count, 'fields': 'domain,lists'})
        posts = posts.get('items')
        recent_notes = []

        for post in posts:
            text = post.get('text')
            if re.sub('^#ДЗ *\n?$', '', text) or re.sub('^#дз *\n?$', '', text):
                lessons = self.parse_lessons(text.lstrip('#дзДЗ'))
                for note in lessons:
                    if note is not None:
                        recent_notes.append(note)

        return recent_notes

    def get_this_week(self, count):
        today = datetime.datetime.today()
        td = today.isocalendar()
        td_year, td_week, td_wday = td[0], td[1], td[2]
        result = []

        for note in self.update_posts(self.group_id, count):
            note_calendar = note.get_calendar()
            nt_year, nt_week, nt_wday = note_calendar[0], note_calendar[1], note_calendar[2]

            if nt_week == td_week and nt_wday >= td_wday:
                if td_wday not in [6, 7]:
                    td_tt = today.timetuple()
                    if td_wday == nt_wday and td_tt.tm_hour >= 13:
                        continue
                    result.append(note)
                elif nt_week == td_week + 1:
                    result.append(note)
        print(self.sort(result))

        return self.sort(result)

    def week(self):
        result = '{}'.format('-' * 0)
        for note in self.get_this_week(50):
            result += '{}\n{}'.format(str(note), '-' * 20)
        if result is '':
            result = 'Записей нет.'
        return result
