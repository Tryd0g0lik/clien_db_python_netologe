import re
import psycopg2 as psy

class DropUser:
  def __init__(self):
    pass

  def drop_user(self, conn, curs):
    data_var =  DropUser._select_user(self, conn, curs)
    DropUser._drop_client(self, data_var, conn, curs)

  def _select_user(self, conn, curs):
    print("Введите email для поиска")
    email_var = input(": ")
    email_var = (email_var).strip()

    if email_var.find("@") != (-1):
      curs.execute("""SELECT * FROM users u
      JOIN phone_user pu on pu.email_user = u.email_user
      WHERE u.email_user = %s""", (email_var, ))
      data_var = curs.fetchall()

      for c in data_var:
        print(c)
    return (data_var, email_var)

  def _drop_client(self, data_var, conn, curs):
    print("""Удалить всего клиента или телефон?
    Всего   - '0'
    Телефон - '1'""")
    client_var = input(": ")
    client_var = client_var.strip()

    if client_var == '0':
      curs.execute("""DELETE FROM phone_user WHERE email_user = %s;""", \
                   (data_var[1],))
      curs.execute("""DELETE FROM users WHERE email_user = %s;""", \
                   (data_var[1],))
      conn.commit()
      print("Сделано")

    elif client_var == '1':
      print("""Номер телефона?""")
      phone_var = input(": ")
      phone_var = phone_var.strip().replace("-", "").replace(" ", "").lstrip("+7").lstrip("8")
      curs.execute("""DELETE FROM phone_user WHERE phone_user = %s;""", (phone_var,))

      conn.commit()
      print("Сделано")

    else:
      exit()





