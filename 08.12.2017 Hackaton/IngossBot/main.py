# -*- coding: utf-8 -*-

# Imports

import json
import logging
import os
import random
import sys
import threading
import time

import telebot

print(sys.executable, os.path.realpath(__file__))
# print(dir(telebot))
# print(dir(os))


logging.basicConfig(format="[%(asctime)-15s] %(levelname)s %(funcName)s: %(message)s", level=logging.INFO)


class TelegramBot:
    """ This is Bot Class

    Methods:
        send_message_thread

    """

    def __init__(self):
        self.f = FilesExchange(True)
        self.users = self.f.users
        print(self.f.config['name'], self.f.config['version'])
        self.bot = telebot.TeleBot(self.f.config['token'])

        self.markup_themes = self.markups(
            ["Автострахование", "Путешествия"],
            ["Имущество", 'Здоровье и жизнь'],
            'Инвестиции и пенсия',
            '🔙'
        )

        self.markup_menu = self.markups(
            '🗄 Виды страхования',
            '🏪 Офисы',
            'Сервисы и платежи',
            ['FAQ', 'О компании']
        )

        self.themes = {
            'car': 'Автострахование',
            #'Автострахование': 'car',
            'travel': 'Путешествия',
            #'Путешествия': 'travel',
            'property': 'Имущество',
            #'Имущество': 'property',
            'life': 'Здоровье и жизнь',
            #'Здоровье и жизнь': 'life',
            'investments': 'Инвестиции и пенсия',
            #'Инвестиции и пенсия': 'investments'
        }

        self.additional_themes = [
            (['автострахование', 'осаго', 'страхование', 'автомобиля', 'еосаго', 'причинение', 'вреда', 'имуществу',
              'третьих', 'лиц', 'причинение', 'вреда', 'жизни', 'и', 'здоровью', 'третьих', 'лиц', 'каско',
              'страхование', 'автомобиля', 'каско', 'ущерб', 'угон', 'и', 'полная', 'гибель', 'зеленая', 'карта'],
             'car', 0),

            (['путешествия', 'за', 'границу', 'по', 'россии', 'медицинские', 'расходы', 'несчастный', 'случай', 'утеря',
              'багажа', 'занятия', 'спортом', 'отмена', 'поездки', 'невыезд', 'первичный', 'отказ', 'в', 'визе',
              'повторный', 'отказ', 'в', 'визе', 'болезнь', 'или', 'травма'], 'travel', 0),

            (['имущество', 'квартира', 'страхование', 'квартиры', 'экспресс', 'страхование', 'имущества', 'страхование',
              'гражданской', 'ответственности', 'на', 'случай', 'причинения', 'вреда', 'соседямтретьим', 'лицам',
              'страхование', 'имущества', 'на', 'время', 'отпуска', 'страхование', 'квартиры', 'дом', 'конструктивные',
              'элементы', 'отделка', 'и', 'инженерное', 'оборудование', 'движимое', 'имущество', 'страхование',
              'квартиры', 'платинум', 'конструктивные', 'элементы', 'отделка', 'и', 'инженерное', 'оборудование',
              'движимое', 'имущество', 'загородная', 'недвижимость', 'ответственность', 'ипотека'], 'property', 0),

            (['здоровье', 'и', 'жизнь', 'добровольное', 'медицинское', 'страхование', 'дмс', 'обязательное',
              'медицинское', 'страхование', 'омс', 'международные', 'программы', 'страхование', 'мигрантов', 'жизнь',
              'и', 'несчастный', 'случай', 'травмы', 'ушибы', 'ожоги', 'потеря', 'трудоспособности', 'на', 'случай',
              'критических', 'заболеваний', 'дмс', 'при', 'дтп', 'автомед', 'добровольное', 'медицинское',
              'страхование',
              'при', 'дтп', 'автомед', 'страхование', 'от', 'укуса', 'клеща', 'антиклещ', 'укус', 'иксодового',
              'клеща'],
             'life', 0),

            (['инвестиции', 'и', 'пенсия', 'инвестиционное', 'страхование', 'жизни', 'накопительные', 'программы',
              'пенсионные', 'накопления', 'паевые', 'фонды', 'пифы', 'доверительное', 'управление', 'индивидуальный',
              'инвестиционный'], 'investments')

        ]

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            logging.info('Callback')
            self.on_callback(call)

        @self.bot.message_handler(commands=["stop"])
        def stop(message):
            if self.check_user(message):
                return
            logging.info('Command /stop')
            self.on_stop(message)

        @self.bot.message_handler(commands=["start"])
        def start(message):
            if self.check_user(message):
                return
            logging.info('Command /start')
            self.on_start(message)

        @self.bot.message_handler(content_types=["sticker"])
        def stickers(message):
            if self.check_user(message): return
            logging.info('Sticker')
            self.on_sticker(message)

        @self.bot.message_handler(content_types=["photo"])
        def photos(message):
            if self.check_user(message): return
            self.on_photo(message)

        @self.bot.message_handler(content_types=["audio"])
        def audios(message):
            if self.check_user(message): return
            logging.info('Audio')
            self.on_audio(message)

        @self.bot.message_handler(content_types=["video"])
        def videos(message):
            if self.check_user(message): return
            logging.info('Video')
            self.on_video(message)

        @self.bot.message_handler(content_types=["voice"])
        def voices(message):
            if self.check_user(message): return
            logging.info('Voice')
            self.on_voice(message)

        @self.bot.message_handler(content_types=["document"])
        def documents(message):
            if self.check_user(message): return
            logging.info('Document')
            self.on_document(message)

        @self.bot.message_handler(content_types=["contact"])
        def contacts(message):
            if self.check_user(message): return
            logging.info('Contact')
            self.on_contact(message)

        @self.bot.message_handler(content_types=["location"])
        def locations(message):
            if self.check_user(message): return
            logging.info('Location')
            self.on_location(message)

        @self.bot.message_handler(commands=["ping"])
        def on_ping(message):
            if self.check_user(message): return
            logging.info('Command')
            self.on_ping(message)

        @self.bot.message_handler(content_types=['text'])
        def echo_message(message):
            if self.check_user(message): return
            logging.info('Message')

            if message.text[0] == '/':
                self.on_unknown_command(message)

            else:
                self.NewMessage(message)

    def on_unknown_command(self, message):
        self.send_message_thread(message.chat.id, "Неизвестная команда.")

    def on_callback(self, call):
        if call.message:
            pass
        elif call.inline_message_id:
            pass

    def on_stop(self, message):
        self.send_message_thread(message.chat.id, "Вы нажали /stop")

    def on_start(self, message):
        self.ch_page(message.chat.id, 'start')
        self.send_message_thread(message.chat.id, "Что вы хотели узнать?", reply_markup=self.markups(None))

    def on_sticker(self, message):
        logging.info('Sticker file id - %s' % message.sticker.file_id)
        self.send_message_thread(message.chat.id, "Вы прислали стикер.")

    def on_photo(self, message):
        self.send_message_thread(message.chat.id, "Вы прислали фото.")

    def on_document(self, message):
        self.send_message_thread(message.chat.id, "Вы прислали документ.")

    def on_voice(self, message):
        self.send_message_thread(message.chat.id, "Вы прислали голос.")

    def on_video(self, message):
        self.send_message_thread(message.chat.id, "Вы прислали видео.")

    def on_audio(self, message):
        self.send_message_thread(message.chat.id, "Вы прислали аудио.")

    def on_contact(self, message):
        self.send_message_thread(message.chat.id, "Вы прислали контакт.")

    def on_location(self, message):
        self.send_message_thread(message.chat.id, "Вы прислали локацию.")

    def on_ping(self, message):
        self.send_message_thread(message.chat.id, random.choice(self.f.strings['ping']))

    def on_like(self, message):
        self.bot.send_message(message.chat.id, 'Благодарю! 😊\nМне очень приятно!')
        self.bot.send_sticker(message.chat.id, random.choice(self.f.strings['stickers_like']))

    def ch_page(self, user_id, page):
        self.users[str(user_id)]['page'] = page

    def get_theme(self, text):
        th = self.additional_themes[:]

        rss = [chr(i) for i in range(1039, 1104)] + [' ']
        r = ''.join([i for i in text.lower() if i in rss])
        r = r.split()

        yet = [0 for _ in range(th.__len__())]

        for i in range(th.__len__()):
            x = ' '.join(th[i][0])
            for word in r:
                u = word
                if len(u) > 5:
                    u = u[:-1]
                if u in x:
                    yet[i] += len(u)/1

        inx = yet.index(max(yet))
        theme = th[inx][1]

        if max(yet) < 2:
            return (False, theme)

        else:
            return (True, theme)

    def add_word(self, word, theme):
        return

    def NewMessage(self, message):
        if ord(message.text[0]) == 128077:
            self.on_like(message)
            return

        id = message.chat.id
        text = message.text
        page = self.get_user(id)["page"]

        if page == 'start':
            status, theme = self.get_theme(text)

            if status:
                theme = self.themes[theme]

                if theme == "Автострахование":
                    self.ch_page(id, 'car')
                    markup = self.markups("Вернуться")
                    self.send_message_thread(message.chat.id, theme, reply_markup=markup)

                elif theme == "Путешествия":
                    self.ch_page(id, 'travel')
                    markup = self.markups("Вернуться")
                    self.send_message_thread(message.chat.id, theme, reply_markup=markup)

                elif theme == "Имущество":
                    self.ch_page(id, 'property')
                    markup = self.markups("Вернуться")
                    self.send_message_thread(message.chat.id, theme, reply_markup=markup)

                elif theme == "Здоровье и жизнь":
                    self.ch_page(id, 'life')
                    markup = self.markups("Вернуться")
                    self.send_message_thread(message.chat.id, theme, reply_markup=markup)

                elif theme == "Инвестиции и пенсия":
                    self.ch_page(id, 'investments')
                    markup = self.markups("Вернуться")
                    self.send_message_thread(message.chat.id, theme, reply_markup=markup)

                elif theme == "🔙":
                    self.ch_page(id, 'menu')
                    markup = self.markups("Вернуться")
                    self.send_message_thread(message.chat.id, theme, reply_markup=markup)

            else:
                self.ch_page(message.chat.id, 'menu')
                markup = self.markup_menu
                self.send_message_thread(message.chat.id,
                                         'Я не совсем точно вас понял 😄\n\nПредлагаю вам воспользоваться поиском:',
                                         reply_markup=markup)

        elif page == 'menu':
            if text == '🗄 Виды страхования':
                self.ch_page(id, 'themes')
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, text, reply_markup=markup)

            elif text == '🏪 Офисы':
                self.ch_page(id, 'offices')
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, text, reply_markup=markup)

            elif text == 'Сервисы и платежи':
                self.ch_page(id, 'services')
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, text, reply_markup=markup)

            elif text == 'О компании':
                markup = self.markup_menu
                self.send_message_thread(message.chat.id, '*СПАО* «[Ингосстрах](https://www.ingos.ru)» — _одна из крупнейших российских страховых компаний, стабильно входит в Топ 10 страховщиков РФ._\n\nОтносится к категории системообразующих российских страховых компаний.\n\nНаиболее медиа-активный страховщик, три года подряд занимает первое место в рейтинге наиболее упоминаемых в прессе страховых компаний.', reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

            else:
                markup = self.markup_menu
                self.bot.send_message(message.chat.id, 'Я могу помочь тебе найти информацию 😊\nЗадай мне свой вопрос или выбери категорию 👇', reply_markup=markup)

        elif page == "themes":
            if text == "Автострахование":
                self.ch_page(id, 'car')
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, text, reply_markup=markup)

            elif text == "Путешествия":
                self.ch_page(id, 'travel')
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, text, reply_markup=markup)

            elif text == "Имущество":
                self.ch_page(id, 'property')
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, text, reply_markup=markup)

            elif text == "Здоровье и жизнь":
                self.ch_page(id, 'life')
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, text, reply_markup=markup)

            elif text == "Инвестиции и пенсия":
                self.ch_page(id, 'investments')
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, text, reply_markup=markup)

            else:
                status, theme = self.get_theme(text)
                if status:
                    theme = self.themes[theme]

                    if theme == "Автострахование":
                        self.ch_page(id, 'car')
                        markup = self.markups("Вернуться")
                        self.send_message_thread(message.chat.id, theme, reply_markup=markup)

                    elif theme == "Путешествия":
                        self.ch_page(id, 'travel')
                        markup = self.markups("Вернуться")
                        self.send_message_thread(message.chat.id, theme, reply_markup=markup)

                    elif theme == "Имущество":
                        self.ch_page(id, 'property')
                        markup = self.markups("Вернуться")
                        self.send_message_thread(message.chat.id, theme, reply_markup=markup)

                    elif theme == "Здоровье и жизнь":
                        self.ch_page(id, 'life')
                        markup = self.markups("Вернуться")
                        self.send_message_thread(message.chat.id, theme, reply_markup=markup)

                    elif theme == "Инвестиции и пенсия":
                        self.ch_page(id, 'investments')
                        markup = self.markups("Вернуться")
                        self.send_message_thread(message.chat.id, theme, reply_markup=markup)
                else:
                    markup = self.markup_themes
                    self.send_message_thread(message.chat.id, 'Я могу помочь тебе найти информацию 😊\nЗадай мне свой вопрос или выбери категорию 👇', reply_markup=markup)

        elif page == "car":
            if text == "Вернуться":
                self.ch_page(id, "themes")
                markup = self.markup_themes
                self.send_message_thread(message.chat.id, 'Я могу помочь тебе найти информацию 😊\nЗадай мне свой вопрос или выбери категорию 👇', reply_markup=markup)

            else:
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, "Вы в комнате 1", reply_markup=markup)

        elif page == "travel":
            if text == "Вернуться":
                self.ch_page(id, "themes")
                markup = self.markup_themes
                self.send_message_thread(message.chat.id, 'Я могу помочь тебе найти информацию 😊\nЗадай мне свой вопрос или выбери категорию 👇', reply_markup=markup)

            else:
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, page, reply_markup=markup)

        elif page == 'property':
            if text == "Вернуться":
                self.ch_page(id, "themes")
                markup = self.markup_themes
                self.send_message_thread(message.chat.id, 'Я могу помочь тебе найти информацию 😊\nЗадай мне свой вопрос или выбери категорию 👇', reply_markup=markup)

            else:
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, page, reply_markup=markup)

        elif page == 'life':
            if text == "Вернуться":
                self.ch_page(id, "themes")
                markup = self.markup_themes
                self.send_message_thread(message.chat.id, 'Я могу помочь тебе найти информацию 😊\nЗадай мне свой вопрос или выбери категорию 👇', reply_markup=markup)

            else:
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, page, reply_markup=markup)

        elif page == 'investments':
            if text == "Вернуться":
                self.ch_page(id, "themes")
                markup = self.markup_themes
                self.send_message_thread(message.chat.id, 'Я могу помочь тебе найти информацию 😊\nЗадай мне свой вопрос или выбери категорию 👇', reply_markup=markup)

            else:
                markup = self.markups("Вернуться")
                self.send_message_thread(message.chat.id, page, reply_markup=markup)

        else:
            self.ch_page(id, "themes")
            markup = self.markup_themes
            self.send_message_thread(message.chat.id, "Ошибка.", reply_markup=markup)

    def get_user(self, user_id):
        return self.users[str(user_id)]

    def check_user(self, message):
        # Check User in Dictionary Users
        if message.chat.id < 0:
            return True

        if str(message.chat.id) in self.users:
            self.get_user(message.chat.id)['time'] = int(time.time())
            if self.get_user(message.chat.id)["chat"]:
                threading.Thread(target=self.f.update_users, args=[self.users]).start()
                return False
            else:
                threading.Thread(target=self.f.update_users, args=[self.users]).start()
                return True

        else:
            self.clear()
            logging.warning('New User')

            self.users[str(message.chat.id)] = {
                "name": message.from_user.first_name,
                "sname": message.from_user.last_name,
                "username": message.from_user.username,
                "page": "start",
                "chat": True,
                "start": int(time.time()),
                "time": int(time.time())

            }

            threading.Thread(target=self.f.update_users, args=[self.users]).start()
            return False

    def send_message_thread(
            self,
            chat_id,
            text,
            disable_web_page_preview=None,
            reply_to_message_id=None,
            reply_markup=None,
            parse_mode=None,
            disable_notification=None
    ):
        threading.Thread(target=self.bot.send_message, args=[
            chat_id,
            text,
            disable_web_page_preview,
            reply_to_message_id,
            reply_markup,
            parse_mode,
            disable_notification
        ]).start()

    def markups(self, *args):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        if len(args):
            for i in args:
                if i is None:
                    return telebot.types.ReplyKeyboardRemove()

                if type(i) in (str, int):
                    markup.row(str(i))
                else:
                    markup.row(*i)

        else:
            return telebot.types.ReplyKeyboardRemove()
        return markup

    def listener(self, message):
        pass

    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        print(self.f.config['name'], self.f.config['version'])

    def run(self):
        logging.info('New Proccess Bot')

        try:
            # self.bot.set_update_listener(self.listener)
            self.bot.polling(True)

        except telebot.apihelper.ApiException:
            threading.Thread(target=self.run).start()


class FilesExchange:
    def __init__(self, debug=False):
        self.busy = False
        self.boot(debug)

    def boot(self, debug=False):
        if self.busy:
            return

        self.busy = True

        files = {'config', 'users', 'strings'}

        opens = {}

        for file in files:
            filename = '%s.json' % file
            if not os.access(filename, mode=os.F_OK):
                if debug: logging.info('Not Found File as "%s"' % filename)
                with open(file=filename, mode='w') as body:
                    if file == 'strings':
                        text = '{"ping": ["Of course I work!", "I\'m already work!"], "stickers_like":["CAADAgADHA4AAkKvaQABYnIuek_e3-wC", "CAADAgADpwEAAzigCiq77pQrZXN5Ag", "CAADAgAD3AADWQMDAAH0zFgaGiqNBgI", "CAADBAADTQIAAuJy2QABuawJiJx0CBoC", "CAADAgADPQMAAu7UDQABcLqwo2_UmeAC"]}'
                    elif file == 'config':
                        text = '{"token": "", "version": "0.0.1", "name": "TestDmRobot"}'
                    else:
                        text = '{}'
                    body.write(text)
            opens[file] = open(file=filename, mode='r')

        self.users = json.loads(opens['users'].read())
        self.config = json.loads(opens['config'].read())
        self.strings = json.loads(opens['strings'].read())

        opens['users'].close()
        opens['config'].close()
        opens['strings'].close()

        self.busy = False

    def update_users(self, users):
        with open(file='users.json', mode='w') as file:
            file.write(json.dumps(users))


if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
