import os
import json
import vk_api


def checkInput():
  while True:

    resposne = ((input(': ')).strip())
    if resposne in " " or resposne == "":
      print(
        """
Error: returning and repeat.
"""
      )
      continue

    else:
      return resposne


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def mainAutor(login, password):
    """ Пример обработки двухфакторной аутентификации """
    vk_session = vk_api.VkApi(
        login, password,
        scope="FRIEND.STORIES.MESSAGES",
        auth_handler=auth_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    return vk_session


def renameFile():
    os.rename("vk_config.v2.json", "vk_config.json")
    return


def jsonGeToken():
  with open("vk_config.json", "r") as vkv2:
    dict_var = json.load(vkv2)
    login = list(dict_var.keys())[0]
    token = dict_var[login]["token"]["app6222115"]["scope_FRIEND.STORIES.MESSAGES"]["access_token"]
    id_user = dict_var[login]["token"]["app6222115"]["scope_FRIEND.STORIES.MESSAGES"]["user_id"]

  if not os.path.exists(".key"):
    from module.keyBot import BasisKey
    file = BasisKey()
    file.keys()

  if os.path.exists(".key"):
    with open(".key", "r") as file_key:
      fKeys = file_key.read()

    with open(".env", "w") as file_env:
      file_env.write( fKeys +
        """
# User_token for VK
TOKEN_API_VK = %s

# ID of autorized User     
user_id_user = %s
""" % (token, id_user)
    )
    return


def token():
# --------Get token and ID of usser --------
  if not os.path.exists("vk_config.json"):
    if not os.path.exists("vk_config.v2.json"):
      print("Your login and Password!")

      login, passw = "your@mail.ru", "your_password"
      vk_session = mainAutor(login, passw)
      vk_login = vk_api.VkApi(login, passw)
      vk_login.token['access_token']

    if os.path.exists("vk_config.v2.json"):
      renameFile()

    jsonGeToken()


class apiFunction:
    def __init__(self, token, id):
        """
        :param token: Key for work in vk througth user-profile
        :param id: User id

        """
        self.token = token
        self.id = id

    def getUser(self):
        """
        :return: data-user
        """
        return
