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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
        self.texts = {
            'menu': 'Я могу помочь тебе найти информацию 😄\nЗадай мне свой вопрос или выбери категорию 👇',
            'car': 'Автострахование\n\n\/',
            'travel': 'Путешествия\n\n\/',
            'property': 'Имущество\n\n\/',
            'life': 'Здоровье и жизнь\n\n\/',
            'investments': 'Инвестиции и пенсия\n\n\/'
        }

        # DICTS
        self.themes = {
            '1': 'Автострахование',
            '2': 'Путешествия',
            '3': 'Имущество',
            '4': 'Здоровье',
            '5': 'Инвестиции',
            '6': 'Офисы',
            '7': 'Сервисы',
            '8': 'Оператор',
            '9': 'Переспросить',
            '10': 'Мусор'
        }

        self.themes_add = {
            'Автострахование': 'car',
            'Путешествия': 'travel',
            'Имущество': 'property',
            'Здоровье': 'life',
            'Инвестиции': 'investments',
            'Офисы': 'offices',
            'Сервисы': 'services',
            'Оператор': 'operator',
            'Переспросить': 'ask',
            'Мусор': 'delete'
        }

        self.themes_rev = {
            'car': 'Автострахование',
            'travel': 'Путешествия',
            'property': 'Имущество',
            'life': 'Здоровье',
            'investments': 'Инвестиции',
            'offices': 'Офисы',
            'services': 'Сервисы',
            'operator': 'Оператор',
            'ask': 'Переспросить',
            'delete': 'Мусор'
        }

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(telebot.types.KeyboardButton('Найти ближайший офис 😊', request_location=True))
        markup.row(telebot.types.KeyboardButton('🔙'))

        self.markups_themes = {
            'themes': self.markups(["Автострахование", "Путешествия"], ["Имущество", 'Здоровье и жизнь'],
                                   'Инвестиции и пенсия', '🔙'),
            'menu': self.markups('🗄 Виды страхования', '🏪 Офисы', '⚙ Сервисы и платежи', ['FAQ', ' О компании']),
            'car': self.markups(['ОСАГО', 'КАСКО'], 'Зеленая карта', '🔙'),
            'travel': self.markups(['За границу', 'По России'], 'Отмена поездки (Невыезд)', '🔙'),
            'property': self.markups(['Квартира', 'Ипотека'], 'Загородная недвижимость', 'Ответственность', '🔙'),
            'life': self.markups('Медицинское страхование', 'Международные программы', 'Жизнь и несчастный случай',
                                 'Страхование мигрантов', '🔙'),
            'investments': self.markups('Инвестиционное страхование жизни', 'Накопительные программы',
                                        'Пенсионные накопления', 'Паевые инвестиционные фонды (ПИФы)', '🔙'),
            'offices': markup,
            'services': self.markups(['Продление полиса', 'Активация полиса'], ['Оплата', 'Проверка'], '🔙'),
            'operator': self.markups('🔙'),
            'ask': self.markups('🔙'),
            'delete': self.markups('🔙'),
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
            self.bot.answer_callback_query(call.id, '')
            if d[0] == 'long_polic':
                if d[1] == 'yes':
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    keyboard.add(telebot.types.InlineKeyboardButton('Продлить в режиме онлайн',
                                                                    url='https://ingos.ru/services/prolongation/'))
                    self.bot.edit_message_text(
                        '*Продлить – КАСКО/страхование квартир*\n\nДля этого нужно:\n\n· Номер страхового полиса\n· Фамилию того, кто заключал договор (страхователя)\n· Узнать стоимость продления можно за 20 дней до окончания срока действия полиса',
                        call.from_user.id, call.message.message_id, reply_markup=keyboard, parse_mode='Markdown')

                else:
                    self.bot.edit_message_text('Спасибо, я учту это!', call.from_user.id, call.message.message_id)

            elif d[0] == 'pay':
                if d[1] == 'yes':
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    keyboard.add(telebot.types.InlineKeyboardButton('Оплатить счета или платежи',
                                                                    url='https://ingos.ru/services/pay/'))
                    self.bot.edit_message_text(
                        '*Онлайн оплата очередных взносов и счетов удобным для Вас способом.*\n\nДля этого нужно:\n\n· Номер счета или договора\n· Фамилию страхователя или плательщика по счету\n· Оплатить взнос или счет возможно до даты, указанной в счете или в плановой рассрочке платежа\n· Если срок платежа просрочен - обратитесь в Ингосстрах для получения дополнительной консультации',
                        call.from_user.id, call.message.message_id, reply_markup=keyboard, parse_mode='Markdown')

                else:
                    self.bot.edit_message_text('Спасибо, я учту это!', call.from_user.id, call.message.message_id)

            elif d[0] == 'activate_polic':
                if d[1] == 'yes':
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    keyboard.add(telebot.types.InlineKeyboardButton('Активировать в режиме онлайн',
                                                                    url='https://ingos.ru/services/activate/'))
                    self.bot.edit_message_text(
                        '*Активировать полиса*\n\nДля этого нужно:\n\n· Название страхового продукта\n· Номер полиса\n· Код активации\n· Сроки активации полиса указанные на коробке, в которой он находится',
                        call.from_user.id, call.message.message_id, reply_markup=keyboard, parse_mode='Markdown')

                else:
                    self.bot.edit_message_text('Спасибо, я учту это!', call.from_user.id, call.message.message_id)

            elif d[0] == 'check':
                if d[1] == 'yes':
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    keyboard.add(telebot.types.InlineKeyboardButton(
                        'Оплатить счета или платежи',
                        url='https://ingos.ru/services/check_policy/')
                    )
                    self.bot.edit_message_text(
                        '*Проверьте подлинность и статус страхового полиса по базе СПАО «Ингосстрах».*\n\nДля этого нужно:\n\n· Номер счета или договора\n\n· Фамилию страхователя или плательщика по счету\n\n· Оплатить взнос или счет возможно до даты, указанной в счете или в плановой рассрочке платежа\n\n· Если срок платежа просрочен - обратитесь в Ингосстрах для получения дополнительной консультации',
                        call.from_user.id, call.message.message_id, reply_markup=keyboard, parse_mode='Markdown')

                else:
                    self.bot.edit_message_text('Спасибо, я учту это!', call.from_user.id, call.message.message_id)

            elif d[0] == 'theme':
                theme = d[1]

                if d[2] == 'yes':
                    self.obuchenie({
                                       'car': '1',
                                       'travel': '2',
                                       'property': '3',
                                       'life': '4',
                                       'investments': '5',
                                       'offices': '6',
                                       'services': '7',
                                       'operator': '8',
                                       'ask': '9',
                                       'delete': '10'
                                   }[theme], self.users[str(call.from_user.id)]['text_to_save'])
                    self.ch_page(call.from_user.id, theme)
                    self.bot.delete_message(call.from_user.id, call.message.message_id)
                    self.bot.send_message(call.from_user.id, self.themes_rev[theme],
                                          reply_markup=self.markups_themes[theme])

                else:
                    self.bot.edit_message_text('Спасибо!\n\nЯ учту ваше мнение!', call.from_user.id,
                                               call.message.message_id)

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
        self.ch_page(message.chat.id, 'menu')
        l = message.location
        l = self.get_coords(l.longitude, l.latitude)
        self.bot.send_message(message.chat.id, ''.join(l[:-1]), reply_markup=self.markups_themes['menu'])
        self.bot.send_location(message.chat.id, l[-1][0], l[-1][-1])

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
            csvfile.write('\n\n' + theme + '***' + _str)

    def get_theme(self, text):
        themes = self.themes
        res = self.neyronka(text)
        theme = themes[res[0][0]]

        print(self.themes[res[0][0]], res)

        if theme == 10 or (res[0][1] <= 1.0000000000000001e-07 and res[0][0] == '7') or res[0][1] == 0 or res[0][
            1] == 6.380000000000001e-07:
            return (False, theme)
        else:
            return (True, theme)

    def get_coords(self, a, b):
        try:
            yet = [
                ('Ингосстрах', '4,3 (61)', 'Страховая компания · ул. Пятницкая, 12, стр. 2', (55.743465, 37.627067)),
                ('Ингосстрах', '', 'Страховое агентство · Голиковский пер., 7, стр.1', (55.739767, 37.627137)),
                ('Ингосстрах', '4,0 (15)', 'Страховое агентство · Лесная ул., 41', (55.780200, 37.590409)),
                ('Ингосстрах', '', 'Страховое агентство · Валовая ул., 18', (55.730446,37.630421)),
                ('Ингосстрах', '', 'Страховое агентство · Павелецкая пл., 2', (55.729640, 37.636207)),
                ('Ингосстрах', '4,3 (17)', 'Страховое агентство · Орлово-Давыдовский пер., 2/5с1', 'Открыто до 17:00', (55.783434, 37.639085)),
                ('Ингосстрах', '4,2 (19)', 'Страховое агентство · ул. Климашкина, 21', 'Открыто до 17:00', (55.776748, 37.688150)),
                ('Ингосстрах', '3,9 (16)', 'Страхование · Бакунинская ул., 50', 'Открыто до 17:00', (55.746291, 37.673781)),
                ('Ингосстрах', '4,3 (10)', 'Страховая компания · ул. Сергия Радонежского, 6', (55.754915, 37.556928)),
                ('ИНГОССТРАХ, '', агентский офис', '3,7 (3)', 'Агентство автострахования · Краснопресненская наб., 12, подъезд 1, 2 этаж', (55.734901, 37.664961)),
                ('Ингосстрах', '3,4 (7)', 'Страховая компания · Марксистская ул., 34 корпус 8', (55.771658, 37.680359)),
                ('Ингосстрах', '', 'Страховое агентство · ул. Фридриха Энгельса, 3/5с2, Москва, 105005', (55.741419, 37.540520)),
                ('Ингосстрах', '3,3 (7)', 'Страховое агентство · Кутузовский просп., 33', (55.704118, 37.656710)),
                ('Ингосстрах-М', '', 'Агентство медицинского страхования · 1-й Автозаводский пр-д, 4 строение 1', (55.718620, 37.571810)),
                ('Ингосстрах', '4,8 (12)', 'Страховая компания · Хамовнический Вал ул., 18', 'Открыто до 17:00', (55.709596, 37.622652)),
                ('Ингосстрах', '4,2 (309)', 'Страховое агентство · ул. Большая Тульская, 10. стр. 9', (55.814127, 37.576321)),
                ('Ингосстрах', '3,2 (10)', 'Страховая компания · Дмитровское ш., 7', (55.797547, 37.558442)),
                ('Ингосстрах', '5,0 (3)', 'Страховая компания · ул. Верхняя Масловка, 25', (55.816341, 37.640736)),
                ('Ингосстрах', '4,6 (31)', 'Страховое агентство · пр-т Мира, 124, корпус 1', 'Открыто до 17:00', (55.733583, 37.712789)),
                ('Ингосстрах', '', 'Страховое агентство · Нижегородская ул., 31', 'Открыто до 17:00', (55.744605, 37.663063))
            ]

            ns = []
            for i in range(len(yet)):
                ns.append(abs(a+b-yet[i][-1][0]-yet[i][-1][1]))
            inx = ns.index(min(ns))
            return yet[inx]
        except:
            pass

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
                self.users[str(message.chat.id)]['text_to_save'] = text
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('✅ Да', callback_data='theme:%s:yes' % self.themes_add[th]),
                    telebot.types.InlineKeyboardButton('❌ Нет', callback_data='theme:%s:no' % self.themes_add[th])
                )
                self.bot.send_message(message.chat.id, 'Перейти в раздел %s ?' % th, reply_markup=markup)

            else:
                self.ch_page(message.chat.id, 'menu')
                markup = self.markups_themes['menu']
                self.bot.send_message(
                    message.chat.id,
                    'Я не совсем точно вас понял 😄\n\nПредлагаю вам воспользоваться поиском:',
                    reply_markup=markup
                )

        elif page == 'menu':
            if text == '🗄 Виды страхования':
                self.ch_page(id, 'themes')
                markup = self.markups_themes['themes']
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

            elif text == '🏪 Офисы':
                self.ch_page(id, 'offices')
                markup = self.markups_themes['offices']
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

            elif text == '⚙ Сервисы и платежи':
                self.ch_page(id, 'services')
                markup = self.markups(['Продление полиса', 'Активация полиса'], ['Оплата', 'Проверка'], '🔙')
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

            elif text == 'О компании':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Учредительные документы и свидетельства',
                                                              url='https://www.ingos.ru/company/disclosure_info/docs/'))
                self.bot.send_message(message.chat.id,
                                      '*СПАО* «[Ингосстрах](https://www.ingos.ru)» — _одна из крупнейших российских страховых компаний, стабильно входит в Топ 10 страховщиков РФ._\n\nОтносится к категории системообразующих российских страховых компаний.\n\nНаиболее медиа-активный страховщик, три года подряд занимает первое место в рейтинге наиболее упоминаемых в прессе страховых компаний.',
                                      reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

            elif text == 'FAQ':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Открыть на сайте', url='https://www.ingos.ru/faq/'))
                self.bot.send_message(message.chat.id,
                                      '*Часто задаваемые вопросы*\n\nВ этом разделе приведены ответы на самые распространенные вопросы, задаваемые пользователями.\n\nЕсли вы не нашли ответ на свой вопрос, то можете обратиться в наш контакт-центр по телефону +7(495)956-55-55 или 8(800)100-77-55.',
                                      reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)


            else:
                status, th = self.get_theme(text)

                if status:
                    self.users[str(message.chat.id)]['text_to_save'] = text
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(
                        telebot.types.InlineKeyboardButton('✅ Да', callback_data='theme:%s:yes' % self.themes_add[th]),
                        telebot.types.InlineKeyboardButton('❌ Нет', callback_data='theme:%s:no' % self.themes_add[th])
                    )
                    self.bot.send_message(message.chat.id, 'Перейти в раздел %s ?' % th, reply_markup=markup)
                else:
                    markup = self.markups_themes['menu']
                    self.bot.send_message(message.chat.id, self.texts[page], reply_markup=markup)

        elif page == "themes":
            if text == "Автострахование":
                self.ch_page(id, 'car')
                markup = self.markups_themes[self.themes_add[text]]
                self.bot.send_message(message.chat.id, self.themes_add[text], reply_markup=markup)

            elif text == "Путешествия":
                self.ch_page(id, 'travel')
                markup = self.markups_themes[self.themes_add[text]]
                self.bot.send_message(message.chat.id, self.themes_add[text], reply_markup=markup)

            elif text == "Имущество":
                self.ch_page(id, 'property')
                markup = self.markups_themes[self.themes_add[text]]
                self.bot.send_message(message.chat.id, self.themes_add[text], reply_markup=markup)

            elif text == "Здоровье и жизнь":
                self.ch_page(id, 'life')
                markup = self.markups_themes[self.themes_add['Здоровье']]
                self.bot.send_message(message.chat.id, self.themes_add['Здоровье'], reply_markup=markup)

            elif text == "Инвестиции и пенсия":
                self.ch_page(id, 'investments')
                markup = self.markups_themes[self.themes_add['Инвестиции']]
                self.bot.send_message(message.chat.id, self.themes_add['Инвестиции'], reply_markup=markup)

            elif text == "🔙":
                self.ch_page(id, 'menu')
                markup = self.markups_themes['menu']
                self.bot.send_message(message.chat.id, self.texts['menu'], reply_markup=markup)

            else:
                status, th = self.get_theme(text)

                if status:
                    self.users[str(message.chat.id)]['text_to_save'] = text
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(
                        telebot.types.InlineKeyboardButton('✅ Да', callback_data='theme:%s:yes' % self.themes_add[th]),
                        telebot.types.InlineKeyboardButton('❌ Нет', callback_data='theme:%s:no' % self.themes_add[th])
                    )
                    self.bot.send_message(message.chat.id, 'Перейти в раздел %s ?' % th, reply_markup=markup)

                else:
                    markup = self.markups_themes['themes']
                    self.bot.send_message(message.chat.id, self.texts['menu'], reply_markup=markup)

        elif page == 'services':
            if text == '🔙':
                self.ch_page(id, "menu")
                markup = self.markups_themes['menu']
                self.bot.send_message(message.chat.id, self.texts['menu'], reply_markup=markup)

            elif text == 'Продление полиса':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton('✅ Да', callback_data='long_polic:yes'),
                           telebot.types.InlineKeyboardButton('❌ Нет', callback_data='long_polic:no'))
                self.bot.send_message(message.chat.id, 'Хотите продлить полис на условиях предыдущего договора?',
                                      reply_markup=markup)


            elif text == 'Активация полиса':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton('✅ Да', callback_data='activate_polic:yes'),
                           telebot.types.InlineKeyboardButton('❌ Нет', callback_data='activate_polic:no'))
                self.bot.send_message(message.chat.id, 'Хотите активировать полис?', reply_markup=markup)


            elif text == 'Оплата':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton('✅ Да', callback_data='pay:yes'),
                           telebot.types.InlineKeyboardButton('❌ Нет', callback_data='pay:no'))
                self.bot.send_message(message.chat.id, 'Хотите оплатить взнос или счет?', reply_markup=markup)


            elif text == 'Проверка':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton('✅ Да', callback_data='check:yes'),
                           telebot.types.InlineKeyboardButton('❌ Нет', callback_data='check:no'))
                self.bot.send_message(message.chat.id,
                                      'Хотите подлинность и статус страхового полиса по базе СПАО «Ингосстрах»?',
                                      reply_markup=markup)

            else:
                markup = self.markups(['Продление полиса', 'Активация полиса'], ['Оплата', 'Проверка'], '🔙')
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

        elif page == 'offices':
            if text == '🔙':
                self.ch_page(id, "menu")
                markup = self.markups_themes['menu']
                self.bot.send_message(message.chat.id, self.texts['menu'], reply_markup=markup)

            else:
                markup = self.markups_themes['offices']
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

        elif page == "car":
            if text == '🔙':
                self.ch_page(id, "themes")
                markup = self.markups_themes['themes']
                self.bot.send_message(message.chat.id, self.texts['menu'], reply_markup=markup)

            elif text == 'ОСАГО':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton('Калькулятор ОСАГО',
                                                              url='https://www.ingos.ru/auto/osago/calc/'))
                self.bot.send_message(message.chat.id,
                                      'Рассчитать стоимость *полиса ОСАГО* онлайн по базовым тарифам без учета страховой истории',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'КАСКО':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Расчет КАСКО', url='https://www.ingos.ru/auto/kasko/calc/'))
                self.bot.send_message(message.chat.id, 'Оформите *Полис КАСКО* на сайте', reply_markup=markup,
                                      parse_mode='Markdown')

            elif text == 'Зеленая карта':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Оформление онлайн', url='https://www.ingos.ru/auto/greencard/'))
                self.bot.send_message(message.chat.id, 'Оформите *Зеленую карту* в офисах Ингосстрах',
                                      reply_markup=markup, parse_mode='Markdown')

            else:
                markup = self.markups('ОСАГО', 'КАСКО', '🔙')
                self.bot.send_message(message.chat.id, text, reply_markup=markup)

        elif page == "travel":
            if text == '🔙':
                self.ch_page(id, "themes")
                markup = self.markups_themes['themes']
                self.bot.send_message(message.chat.id, self.texts['menu'], reply_markup=markup)

            elif text == 'За границу':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Оформление онлайн', url='https://www.ingos.ru/travel/abroad/'))
                self.bot.send_message(message.chat.id,
                                      '*Страхование путешествующих* – это в первую очередь медицинская помощь застрахованным, находящимся за границей в путешествии или деловой поездке\n\nСтраховой полис покрывает риски, связанные с ухудшением здоровья застрахованного, при обычном заболевании и другие',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'По России':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Оформление онлайн', url='https://www.ingos.ru/travel/russia/'))
                self.bot.send_message(message.chat.id,
                                      'Медицинское *страхование туристов* при поездках по России обеспечивает вас гарантией организации медицинской помощи при выезде с постоянного места жительства.',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'Отмена поездки (Невыезд)':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Оформление онлайн', url='https://www.ingos.ru/travel/neviezd/'))
                self.bot.send_message(message.chat.id,
                                      '*Страховка от невыезда* - полис страхования от отмены поездки.\n\nДанный полис защищает застрахованного от расходов, которые он может понести, если его поездка отменится по независящим от него обстоятельствам.',
                                      reply_markup=markup, parse_mode='Markdown')

            else:
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, page, reply_markup=markup)

        elif page == 'property':
            if text == '🔙':
                self.ch_page(id, "themes")
                markup = self.markups_themes['themes']
                self.bot.send_message(message.chat.id, self.texts['menu'], reply_markup=markup)

            elif text == 'Квартира':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Подробнее', url='https://www.ingos.ru/property/flat/'))
                self.bot.send_message(message.chat.id,
                                      '*Добровольное страхование квартиры* – это возможность застраховать ваше недвижимое и движимое (в т.ч. ценное) имущество и ответственность перед соседями на случай повреждений, возникших в результате пожара, взрыва, залива, стихийных бедствий, противоправных действий и других актуальных рисков.',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'Загородная недвижимость':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Рассчитать', url='https://www.ingos.ru/property/house/calc/'))
                self.bot.send_message(message.chat.id,
                                      '*Страхование строений* – возможность застраховать дачу, дом за городом, баню, хозяйственные постройки, ограждения и иные сооружения на приусадебном участке, элементы ландшафтного дизайна, а также самоходные машины и движимое имущество. ',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'Ответственность':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Рассчитать',
                                                       url='https://www.ingos.ru/property/calc/?calculator=express_go'))
                self.bot.send_message(message.chat.id,
                                      '*Страхование гражданской ответственности* – это возможность застраховать вашу гражданскую ответственность перед лицами, которым может быть причинен вред по вашей вине при эксплуатации вашего имущества.',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'Ипотека':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Посмотреть', url='https://www.ingos.ru/mortgage/'))
                self.bot.send_message(message.chat.id,
                                      '*Ипотечное страхование* — это способ защиты финансовых интересов заемщика по выплате кредита в случае наступления непредвиденных обстоятельств и одно из обязательных требований банков и иных кредитных организаций, которые выдают ипотечные кредиты и займы.',
                                      reply_markup=markup, parse_mode='Markdown')

            else:
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, page, reply_markup=markup)

        elif page == 'life':
            if text == '🔙':
                self.ch_page(id, "themes")
                markup = self.markups_themes['themes']
                self.bot.send_message(message.chat.id, self.texts['menu'], reply_markup=markup)

            elif text == 'Медицинское страхование':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Добровольное', url='https://www.ingos.ru/health_life/dms/'))
                markup.add(
                    telebot.types.InlineKeyboardButton('Обязательное', url='https://www.ingos.ru/health_life/oms/'))
                self.bot.send_message(message.chat.id,
                                      '*Страхование гражданской ответственности* – это возможность застраховать вашу гражданскую ответственность перед лицами, которым может быть причинен вред по вашей вине при эксплуатации вашего имущества.',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'Международные программы':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Подробнее', url='https://www.ingos.ru/health_life/intl_dms/'))
                self.bot.send_message(message.chat.id,
                                      '*Программы международного медицинского страхования* предполагают организацию и оплату медицинской помощи по различным заболеваниям и состояниям, в том числе продолжительным или требующим дорогостоящего лечения в лучших клиниках мира и России.',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'Жизнь и несчастный случай':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Подробнее', url='https://www.ingos.ru/health_life/ns/'))
                self.bot.send_message(message.chat.id,
                                      '*Cтрахование жизни и здоровья от несчастных случаев* – это надежный способ позаботиться о себе и своих близких. Особенность данной страховки заключается в том, что она предоставляет страхователю широкие возможности для выбора.',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'Страхование мигрантов':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Подробнее', url='https://www.ingos.ru/health_life/migrant/'))
                self.bot.send_message(message.chat.id,
                                      '*О полисе страхования трудовых мигрантов*\n\nС 1.01.2015 года в соответствии с Федеральным законом от 1 декабря 2014 г. № 407 и 409 «О внесении в Трудовой кодекс Российской Федерации и статью 13 Федерального закона «О правовом положении иностранных граждан в Российской Федерации» изменений, связанных с особенностями регулирования труда работников, являющихся иностранными гражданами или лицами без гражданства»"',
                                      reply_markup=markup, parse_mode='Markdown')


            else:
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, page, reply_markup=markup)

        elif page == 'investments':
            if text == '🔙':
                self.ch_page(id, "themes")
                markup = self.markups_themes['themes']
                self.bot.send_message(message.chat.id, self.texts['menu'], reply_markup=markup)

            elif text == 'Инвестиционное страхование жизни':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Подробнее', url='https://www.ingos.ru/pension_investment/ili/'))
                self.bot.send_message(message.chat.id,
                                      '*Программа инвестиционного страхования жизни «Вектор»*\n\nИнвестиционное страхование жизни (ИСЖ) сочетает в себе преимущества ряда финансовых инструментов, делая его по-своему уникальным.',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'Накопительные программы':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Подробнее',
                                                       url='https://www.ingos.ru/pension_investment/nprog/'))
                self.bot.send_message(message.chat.id,
                                      '*Накопительное страхование жизни*\nПрограммы накопительного страхования жизни (НСЖ) позволяют создать финансовый резерв к определенной дате и обеспечивают страховой защитой на случай непредвиденных происшествий, связанных с жизнью и здоровьем.',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'Пенсионные накопления':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Подробнее',
                                                       url='https://www.ingos.ru/pension_investment/savings/'))
                self.bot.send_message(message.chat.id,
                                      '31 декабря 2015 года завершился период, отведенный гражданам для выбора варианта пенсионного обеспечения: сохранить накопительную пенсию или отказаться от ее дальнейшего формирования.',
                                      reply_markup=markup, parse_mode='Markdown')

            elif text == 'Паевые инвестиционные фонды (ПИФы)':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton('Подробнее',
                                                       url='https://www.ingos.ru/pension_investment/fund/'))
                self.bot.send_message(message.chat.id,
                                      '*Паевой инвестиционный фонд (ПИФ)*\n\nФорма коллективного инвестирования, при которой средства множества пайщиков (инвесторов) передаются профессиональным управляющим. Те, в свою очередь, делают инвестиции в ценные бумаги или иное имущество с целью получения максимального дохода.',
                                      reply_markup=markup, parse_mode='Markdown')

            else:
                markup = self.markups('🔙')
                self.bot.send_message(message.chat.id, page, reply_markup=markup)

        else:
            self.ch_page(id, "themes")
            markup = self.markups_themes['themes']
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

            # except Exception as Error:
            # print('Error %s' % Error)


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
