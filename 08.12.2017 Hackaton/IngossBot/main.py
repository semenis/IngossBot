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
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

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


        # STRINGS
        self.text_menu = 'Я могу помочь тебе найти информацию 😊\nЗадай мне свой вопрос или выбери категорию 👇'
        self.text_car = 'Автострахование\n\n\/'
        self.text_travel = 'Путешествия\n\n\/'
        self.text_property = 'Имущество\n\n\/'
        self.text_life = 'Здоровье и жизнь\n\n\/'
        self.text_investments = 'Инвестиции и пенсия\n\n\/'


        # DICTS
        self.markup_themes = self.markups(
            ["Автострахование", "Путешествия"],
            ["Имущество", 'Здоровье и жизнь'],
            'Инвестиции и пенсия',
            '🔙'
        )

        self.markup_menu = self.markups(
            '🗄 Виды страхования',
            '🏪 Офисы',
            '⚙ Сервисы и платежи',
            ['FAQ', 'О компании']
        )

        self.themes = {
            '1':'Автострахование',
            '2':'Путешествия',
            '3':'Имущество',
            '4':'Здоровье',
            '5':'Инвестиции',
            '6':'Офисы',
            '7':'Сервисы',
            '8':'Оператор',
            '9':'Переспросить',
            '10':'Мусор'
        }

        self.themes_add = {
            'Автострахование': 'car',
            'Путешествия': 'travel',
            'Имущество': 'property',
            'Здоровье': 'life',
            'Инвестиции':'investments',
            'Офисы':'offices',
            'Сервисы':'services',
            'Оператор': 'operator',
            'Переспросить':'ask',
            'Мусор':'delete'
        }

        self.themes_rev = {
            'car':'Автострахование',
            'travel':'Путешествия',
            'property':'Имущество',
            'life':'Здоровье',
            'investments':'Инвестиции',
            'offices':'Офисы',
            'services':'Сервисы',
            'operator':'Оператор',
            'ask':'Переспросить',
            'delete':'Мусор'
        }

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
        self.bot.send_message(message.chat.id, "Неизвестная команда.")

    def on_callback(self, call):
        if call.message:
            d = call.data.split(':')
            if d[0] == 'long_polic':
                if d[1] == 'yes':
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    keyboard.add(telebot.types.InlineKeyboardButton('Продлить в режиме онлайн', url='https://ingos.ru/services/prolongation/'))
                    self.bot.answer_callback_query(call.id, 'ОК')
                    self.bot.edit_message_text('*Продлить – КАСКО/страхование квартир*\n\nДля этого нужно:\n\n· Номер страхового полиса\n· Фамилию того, кто заключал договор (страхователя)\n· Узнать стоимость продления можно за 20 дней до окончания срока действия полиса', call.from_user.id, call.message.message_id, reply_markup=keyboard, parse_mode='Markdown')

                else:
                    self.bot.answer_callback_query(call.id, '')
                    self.bot.edit_message_text('Спасибо, я учту это!', call.from_user.id, call.message.message_id)

            elif d[0] == 'theme':
                theme = d[1]

                if d[2] == 'yes':
                    self.bot.answer_callback_query(call.id, 'ОК')

                else:
                    self.bot.answer_callback_query(call.id, 'ТЫ ПЕТУХ')
                    self.bot.edit_message_text('Спасибо!\n\nЯ учту ваше мнение!', call.from_user.id, call.message.message_id)

        elif call.inline_message_id:
            pass

    def on_stop(self, message):
        self.bot.send_message(message.chat.id, "Вы нажали /stop")

    def on_start(self, message):
        self.ch_page(message.chat.id, 'start')
        self.bot.send_message(message.chat.id, "Что вы хотели узнать?", reply_markup=self.markups(None))

    def on_sticker(self, message):
        logging.info('Sticker file id - %s' % message.sticker.file_id)
        self.bot.send_message(message.chat.id, "Вы прислали стикер.")

    def on_photo(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали фото.")

    def on_document(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали документ.")

    def on_voice(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали голос.")

    def on_video(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали видео.")

    def on_audio(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали аудио.")

    def on_contact(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали контакт.")

    def on_location(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали локацию.")

    def on_ping(self, message):
        self.bot.send_message(message.chat.id, random.choice(self.f.strings['ping']))

    def on_like(self, message):
        self.bot.send_message(message.chat.id, 'Благодарю! 😊\nМне очень приятно!')
        self.bot.send_sticker(message.chat.id, random.choice(self.f.strings['stickers_like']))

    def ch_page(self, user_id, page):
        self.users[str(user_id)]['page'] = page

    def neyronka(self, _str):
        newsTrainer = Trainer(tokenizer)
        with open('o', 'rt', encoding='utf8') as csvfile:
            res = '['
            for i in csvfile.readlines():
                if i == '\n':
                    continue
                else:
                    theme, text = i.split('***')
                    res += '{\'text\':' + '\'' + text.strip() + '\'' + ', ' + '\'category\':' + '\'' + str(
                        theme) + '\'},\n'
            res += ']'
            newsSet = eval(res)
            for news in newsSet:
                newsTrainer.train(news['text'], news['category'])
            newsClassifier = Classifier(newsTrainer.data, tokenizer)
            unknownInstance = _str
            classification = newsClassifier.classify(unknownInstance)
            return (sorted(classification, key=(lambda x: -x[1])))

    def obuchenie(self, theme, _str):
        with open('o', 'a', encoding='utf8') as csvfile:
            csvfile.write('\n' + theme + '***' + _str)

    def get_theme(self, text):
        themes = self.themes
        res = self.neyronka(text)
        theme = themes[res[0][0]]

        print(self.themes[res[0][0]], res)

        if theme == 10 or (res[0][1] <= 7.1e-08 and res[0][0] == '7') or res[0][1] == 0 :
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
            status, th = self.get_theme(text)

            if status:
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('✅ Да', callback_data='theme:%s:yes' % self.themes_add[th]),
                    telebot.types.InlineKeyboardButton('❌ Нет', callback_data='theme:%s:no' % self.themes_add[th])
                )
                self.bot.send_message(message.chat.id, 'Перейти в раздел %s ?' % th, reply_markup=markup)

            else:
                self.ch_page(message.chat.id, 'menu')
                markup = self.markup_menu
                self.bot.send_message(
                    message.chat.id,
                    'Я не совсем точно вас понял 😄\n\nПредлагаю вам воспользоваться поиском:',
                    reply_markup=markup
                )

        elif page == 'menu':
            if text == '🗄 Виды страхования':
                self.ch_page(id, 'themes')
                markup = self.markup_themes
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

            elif text == '🏪 Офисы':
                self.ch_page(id, 'offices')
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

            elif text == '⚙ Сервисы и платежи':
                self.ch_page(id, 'services')
                markup = self.markups(['Продление полиса', 'Активация полиса'], ['Оплата', 'Проверка'], '🔙')
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

            elif text == 'О компании':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Учредительные документы и свидетельства', url='https://www.ingos.ru/company/disclosure_info/docs/'))
                self.bot.send_message(message.chat.id, '*СПАО* «[Ингосстрах](https://www.ingos.ru)» — _одна из крупнейших российских страховых компаний, стабильно входит в Топ 10 страховщиков РФ._\n\nОтносится к категории системообразующих российских страховых компаний.\n\nНаиболее медиа-активный страховщик, три года подряд занимает первое место в рейтинге наиболее упоминаемых в прессе страховых компаний.', reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

            elif text == 'FAQ':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Открыть на сайте', url='https://www.ingos.ru/faq/'))
                self.bot.send_message(message.chat.id, '*Часто задаваемые вопросы*\n\nВ этом разделе приведены ответы на самые распространенные вопросы, задаваемые пользователями.\n\nЕсли вы не нашли ответ на свой вопрос, то можете обратиться в наш контакт-центр по телефону +7 495 956-55-55 или 8 800 100 77 55.', reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)


            else:
                status, th = self.get_theme(text)

                if status:
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(
                        telebot.types.InlineKeyboardButton('✅ Да', callback_data='theme:%s:yes' % self.themes_add[th]),
                        telebot.types.InlineKeyboardButton('❌ Нет', callback_data='theme:%s:no' % self.themes_add[th])
                    )
                    self.bot.send_message(message.chat.id, 'Перейти в раздел %s ?' % th, reply_markup=markup)
                else:
                    markup = self.markup_menu
                    self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

        elif page == "themes":
            if text == "Автострахование":
                self.ch_page(id, 'car')
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, eval('self.text_%s' % self.themes_add[text]), reply_markup=markup)

            elif text == "Путешествия":
                self.ch_page(id, 'travel')
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, eval('self.text_%s' % self.themes_add[text]), reply_markup=markup)

            elif text == "Имущество":
                self.ch_page(id, 'property')
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, eval('self.text_%s' % self.themes_add[text]), reply_markup=markup)

            elif text == "Здоровье и жизнь":
                self.ch_page(id, 'life')
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, eval('self.text_%s' % self.themes_add['Здоровье']), reply_markup=markup)

            elif text == "Инвестиции и пенсия":
                self.ch_page(id, 'investments')
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, eval('self.text_%s' % self.themes_add['Инвестиции']), reply_markup=markup)

            elif text == "🔙":
                self.ch_page(id, 'menu')
                markup = self.markup_menu
                self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

            else:
                status, th = self.get_theme(text)

                if status:
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(
                        telebot.types.InlineKeyboardButton('✅ Да', callback_data='theme:%s:yes' % self.themes_add[th]),
                        telebot.types.InlineKeyboardButton('❌ Нет', callback_data='theme:%s:no' % self.themes_add[th])
                    )
                    self.bot.send_message(message.chat.id, 'Перейти в раздел %s ?' % th, reply_markup=markup)

                else:
                    markup = self.markup_themes
                    self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

        elif page == 'offices':
            if text == '🔙':
                self.ch_page(id, "menu")
                markup = self.markup_menu
                self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

            else:
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

        elif page == 'services':
            if text == '🔙':
                self.ch_page(id, "menu")
                markup = self.markup_menu
                self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

            elif text == 'Продление полиса':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton('✅ Да', callback_data='long_polic:yes'), telebot.types.InlineKeyboardButton('❌ Нет', callback_data='long_polic:no'))
                self.bot.send_message(message.chat.id, 'Хотите продлить полис на условиях предыдущего договора?', reply_markup=markup)

            else:
                markup = self.markups(['Продление полиса', 'Активация полиса'], ['Оплата', 'Проверка'], '🔙')
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

        elif page == 'services_2':
            if text == '🔙':
                self.ch_page(id, "menu")
                markup = self.markup_menu
                self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

            elif text == 'Продление полиса':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton('✅ Да', callback_data='long_polic:yes'), telebot.types.InlineKeyboardButton('❌ Нет', callback_data='long_polic:no'))
                self.bot.send_message(message.chat.id, 'Хотите продлить полис на условиях предыдущего договора?', reply_markup=markup)


            else:
                markup = self.markups('Продление полиса', '🔙')
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

        elif page == 'offices':
            if text == '🔙':
                self.ch_page(id, "menu")
                markup = self.markup_menu
                self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

            else:
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

        elif page == "car":
            if text == '🔙':
                self.ch_page(id, "themes")
                markup = self.markup_themes
                self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

            elif text == 'ОСАГО':
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, '800', reply_markup=markup)

            elif text == 'КАСКО':
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, '800', reply_markup=markup)

            else:
                markup = self.markups('ОСАГО', 'КАСКО', '🔙')
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

        elif page == "travel":
            if text == '🔙':
                self.ch_page(id, "themes")
                markup = self.markup_themes
                self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

            else:
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, page, reply_markup=markup)

        elif page == 'property':
            if text == '🔙':
                self.ch_page(id, "themes")
                markup = self.markup_themes
                self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

            else:
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, page, reply_markup=markup)

        elif page == 'life':
            if text == '🔙':
                self.ch_page(id, "themes")
                markup = self.markup_themes
                self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

            else:
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, page, reply_markup=markup)

        elif page == 'investments':
            if text == '🔙':
                self.ch_page(id, "themes")
                markup = self.markup_themes
                self.bot.send_message(message.chat.id, self.text_menu, reply_markup=markup)

            else:
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, page, reply_markup=markup)

        else:
            self.ch_page(id, "themes")
            markup = self.markup_themes
            self.bot.send_message(message.chat.id, "Ошибка.", reply_markup=markup)

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

        #except Exception as Error:
            #print('Error %s' % Error)


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
