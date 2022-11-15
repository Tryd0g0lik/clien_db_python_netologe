from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotEventType
from module.Bot.vkBot import vkBot
from module.dbBot.sql_requests import sqlTasks, Botdb
from module.user_token.token_api_vk import token, checkInput
import os


class Topmenu:

    def topMenu(self):
        """
        :return: Basis menu
        """
        return """
       Select the symbol for launch application:
        - 't' get a user-token;
        - 's' start a Bot;
        - 'e' exi;
        - 'd' create db
        """

    def insert(self):
        """
        :return: Return one symbol for a launch command of an application
        """

        print("Choose a command.")
        response = ((checkInput())[0]).lower()

        if response in "t":
            # if os.path.isfile(".env"):
            #     os.remove(".env")
            if os.path.isfile("vk_config.json"):
                os.remove("vk_config.json")
            token()
        elif response in "s":
            bot = vkBot()
            db = Botdb()
            for event in bot.longpoll.listen():
                random_id = get_random_id()
                if event.type == VkBotEventType.MESSAGE_NEW:
                    peer_id = event.object.message['peer_id']
                    event_command = event.object.message['text'].lower()
                    params = bot.bot_command(event_command, event, peer_id, random_id)  # correct
                    print("params MESSAGE_NEW: ", params)  # correct

                    if params[1] == 'start':  # correct
                        user_id = list((params[0]).values())[0]  # correct
                        print("user_id: ", user_id)

                elif event.type == VkBotEventType.MESSAGE_EVENT:
                    peer_id = event.object.peer_id
                    event_command = event.object.payload['type']

                    params = bot.bot_command(event_command, event, peer_id, random_id)  # correct
                    print(user_id, "params MESSAGE_EVENT: ", params)  # correct
                    if params[0] == "add_favorites" or params[0] == "add_blacklist":  # correct
                        db.insertElected(user_id=user_id, event_command=params[0], id_elected_user=params[1])  # correct
                    if type(params) == str and params == "blacklist" or params == "favorites":  # correct
                        if params == "blacklist":  # correct
                            variable_value = 1  # correct
                        elif params == "favorites":  # correct
                            variable_value = 0  # correct
                        print(db.public_list(variable_value))  # correct

        elif response in "d":
            new_db = sqlTasks()
            new_db.templateTable()

        elif response in "e":
            exit()

        else:
            return


if __name__ == "__main__":
    while True:
        menu = Topmenu()
        print(menu.topMenu())
        menu.insert()
