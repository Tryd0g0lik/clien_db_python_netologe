import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import TOKEN_BOT, GROUP_ID, ID_APP
from vk_api.bot_longpoll import VkBotLongPoll
from module.API_VK.api import api


class vkBot:
    list_message = []

    def __init__(self, db):
        self.apiVK = api(db)
        self.vk_session = vk_api.VkApi(token=TOKEN_BOT)
        self.longpoll = VkBotLongPoll(self.vk_session, GROUP_ID)
        self.vk = self.vk_session.get_api()

        self.offset = self.apiVK.offset
        self.count_users = 0
        self.id_user = 0
        # self.filter = (1, 99, 2, 6, 20, 20)
        self.filter = self.apiVK.search_filter(self.id_user)
        self.message_id = 0

        # Метод создания основного меню
        def menu_keyboard(self):
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_callback_button(
                label='🔍 ПОИСК', color=VkKeyboardColor.SECONDARY,
                payload={"type": "search"}
                )
            keyboard.add_line()
            keyboard.add_callback_button(
                label='⭐ Избранные', color=VkKeyboardColor.POSITIVE,
                payload={"type": "favorites"}
                )
            keyboard.add_callback_button(
                label='✘ Чёрный список', color=VkKeyboardColor.NEGATIVE,
                payload={"type": "blacklist"}
                )
            keyboard.add_line()
            keyboard.add_callback_button(
                label='⚙ Фильтр', color=VkKeyboardColor.SECONDARY,
                payload={"type": "filter"}
                )
            keyboard.add_callback_button(label='🚑 HELP', color=VkKeyboardColor.PRIMARY, payload={"type": "help"})
            return keyboard

        # Метод создания кнопок управления для листания людей
        def menu_search(self):
            keyboard_sender = VkKeyboard(inline=True)
            keyboard_sender.add_callback_button(
                label='⬅', color=VkKeyboardColor.SECONDARY,
                payload={"type": "search_back"}
                )
            keyboard_sender.add_callback_button(
                label='❌ Черный список', color=VkKeyboardColor.PRIMARY,
                payload={"type": "add_blacklist"}
                )
            keyboard_sender.add_callback_button(
                label='❤ Избранный', color=VkKeyboardColor.POSITIVE,
                payload={"type": "add_favorites"}
                )
            keyboard_sender.add_callback_button(
                label='➡', color=VkKeyboardColor.SECONDARY,
                payload={"type": "search_next"}
                )
            return keyboard_sender

        # Метод сбора сообщения для отправки от бота
        def message(self, peer_id, random_id, message, keyboard=None, attachment=None):
            if keyboard is not None:
                keyboard = keyboard.get_keyboard()
            else:
                keyboard = ''
            if attachment is not None:
                attachment = attachment
            else:
                attachment = ''
            return self.vk.messages.send(
                peer_id=peer_id,
                random_id=random_id,
                keyboard=keyboard,
                message=message,
                attachment=attachment
            )

        # Метод создания сообщения ПОМОЩИ
        def bot_help_message(self):
            message = f"Справка по командам:\n" \
                      f"help - справка\n" \
                      f"start - начать работу с ботом\n" \
                      f"search - поиск пользователей по заданному фильтру\n" \
                      f"search_next - поиск, листать Далее\n" \
                      f"search_back - поиск, листать Назад\n" \
                      f"filter - настройка фильтра поиска\n" \
                      f"filter_setting 1,99,2,6,20,23 - изменить настройки фильтра\n" \
                      f"add_favorites - добавить пользователя в избранные\n" \
                      f"add_blacklist - добавить потльзователя в чёрный список\n" \
                      f"favorites - список избранных пользователей\n" \
                      f"blacklist - список пользователей попавших в черный список"
            return message

        # Метод удаления предыдущего сообщения от бота, чтоб не засирать чат
        def worker_message(self, user_id, action):
            message_id = self.message_id
            offset = self.offset
            id_mess = self.apiVK.worker_message(user_id, message_id, offset, action)
            if id_mess:
                print(f"MESSAGE ====> {id_mess}========> action====>{action}========> message====>>{message_id}")
                self.vk.messages.delete(
                    message_ids=id_mess,
                    group_id=GROUP_ID,
                    delete_for_all=True,
                )

        # Метод основной логики управления что с команд, что с кнопок
        def bot_command(self, event_command, event, peer_id, random_id):
            offset = self.offset
            count_users = self.count_users
            filter = self.filter
            id_user = self.id_user

            if event_command == 'start':
                # self.delete_message()
                self.worker_message(peer_id, 'drop')
                user = self.apiVK.user(event.object.message['from_id'])
                keyboard = self.menu_keyboard()
                message = f'Привет, {user["first_name"]}!\n ' \
                          f'Так как в нашем боте не используются проставление лайков для пользователей, ' \
                          f'мы не используем алгортмы получения токенов!\n' \
                          f'Для продолжения работы используй кнопки действия!\n'
                self.message_id = self.message(peer_id, random_id, message, keyboard)
                print(f"Start====>  {self.message_id}")
                # self.list_message.append(self.message_id)
                self.worker_message(peer_id, 'insert')
                self.filter = user["filter"]

            elif event_command == 'help':
                # self.delete_message()
                self.worker_message(peer_id, 'drop')
                message = self.bot_help_message()
                self.message_id = self.message(peer_id, random_id, message)
                print(f"HELP====>   {self.message_id}")
                # self.list_message.append(self.message_id)
                self.worker_message(peer_id, 'insert')

            elif 'search' in event_command:
                # self.delete_message()
                self.worker_message(peer_id, 'drop')
                if event_command == 'search':
                    offset = 0
                    command = 'search'
                elif event_command == 'search_next':
                    if offset > count_users:
                        offset = count_users
                    else:
                        offset += 1
                    command = 'search_next'
                elif event_command == 'search_back':
                    if offset > 0:
                        offset -= 1
                        command = 'search_back'
                    else:
                        offset = 0
                        command = 'search'
                users = self.apiVK.search_users(peer_id, offset, filter, command)
                self.offset = users['offset']
                self.count_users = users["count"]
                keyboard = self.menu_search()
                if users['star'] is True:
                    star = '⭐ '
                else:
                    star = ''
                message = f'{star}{users["users"][0]["first_name"]} {users["users"][0]["last_name"]}\n' \
                          f'https://vk.com/id{users["users"][0]["id_user"]}'
                attachment = users['users'][0]['photo']
                self.message_id = self.message(peer_id, random_id, message, keyboard, attachment)
                self.id_user = users["users"][0]["id_user"]
                print(f"SEARCH={command}===> {self.message_id}")
                # self.list_message.append(self.message_id)
                self.worker_message(peer_id, 'insert')

            elif event_command == 'add_favorites':
                # self.list_message.append(self.message_id)
                print(f"add fav===>{self.message_id}")
                self.worker_message(peer_id, 'insert')
                if id_user != 0:
                    list_favorites = self.apiVK.insert_favorites(id_user, peer_id)
                    if list_favorites is not False:
                        message = f"Пользователь добавлен в избранные!!!!! В вашем листе {list_favorites}"
                    else:
                        message = f"Пользователь был добавлен в какой-то из листов!!!"
                    self.message_id = self.message(peer_id, random_id, message)
                    print(f"ADD_FAVORITES====>{self.message_id}")
                    # self.delete_message()
                print(f"drop fav===>{self.message_id}")
                self.worker_message(peer_id, 'drop')

            elif event_command == 'add_blacklist':
                # self.list_message.append(self.message_id)
                self.worker_message(peer_id, "insert")
                if id_user != 0:
                    list_black = self.apiVK.insert_blacklist(id_user, peer_id)
                    if list_black is not False:
                        message = f"Пользователь добавлен в чёрный список!!!!! В вашем листе {list_black}"
                    else:
                        message = f"Пользователь был добавлен в какой-то из листов!!!"
                    self.message_id = self.message(peer_id, random_id, message)
                    print(f"ADD_BLACKLIST====>{self.message_id}")
                # self.delete_message()
                self.worker_message(peer_id, 'drop')

            elif event_command == 'filter':
                # self.delete_message()
                self.worker_message(peer_id, 'drop')
                message = f"Тип фильтра (Страна, Город, Пол, Семейное положение, Возраст с, Возраст по). В данный момент фильтр {filter}"
                self.message_id = self.message(peer_id, random_id, message)
                print(f"FILTER====>{self.message_id}")
                # self.list_message.append(self.message_id)
                self.worker_message(peer_id, 'insert')

            elif 'filter_setting' in event_command:
                # self.delete_message()
                self.worker_message(peer_id, 'drop')
                string = event.object.message['text'].lower().replace("filter_setting", "")
                new_filter = self.apiVK.update_filter(peer_id, string)
                self.filter = new_filter
                message = f"Фильтры изменён на {new_filter}!!!!!"
                self.message_id = self.message(peer_id, random_id, message)
                print(f"FILTER_SETTING====>{self.message_id}")
                # self.list_message.append(self.message_id)
                self.worker_message(peer_id, 'insert')

            elif event_command == 'favorites':
                # self.delete_message()
                self.worker_message(peer_id, 'drop')
                message = ''
                list_favorite = self.apiVK.view_favorites(peer_id)
                for item in list_favorite:
                    message += f"https://vk.com/id{item}\n"
                message = f"Ваши избранные пользователи {len(list_favorite)}:\n{message}"
                self.message_id = self.message(peer_id, random_id, message)
                print(f"FAVORITES====>{self.message_id}")
                # self.list_message.append(self.message_id)
                self.worker_message(peer_id, 'insert')

            elif event_command == 'blacklist':
                # self.delete_message()
                self.worker_message(peer_id, 'drop')
                message = ''
                list_blacklist = self.apiVK.view_blacklist(peer_id)
                for item in list_blacklist:
                    message += f"https://vk.com/id{item}\n"
                message = f"Ваши пользователи из чёрного списка {len(list_blacklist)}:\n{message}"
                self.message_id = self.message(peer_id, random_id, message)
                print(f"BLACKLIST====>{self.message_id}")
                # self.list_message.append(self.message_id)
                self.worker_message(peer_id, 'insert')
            if event_command == 'start':# correct
                return (user, event_command, id_user)# correct
            return (event_commandq, id_user) # correct