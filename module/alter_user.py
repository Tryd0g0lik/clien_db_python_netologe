import psycopg2 as psy
import re

class AlterUser:
  def __init__(self):
    pass

  def alter_user(self, conn, curs):
    print("""Введите пользовательские данные: телефон или email""")

    phone, email = input('phone: '), input('email: ')

    if phone != '':
      phone = int(phone.strip())
      data_var = AlterUser._select_data_user(self, phone, curs)
      AlterUser._alter_data_user(self, data_var, conn, curs)

    elif phone == '' and email == '':
      exit()

    else:
      email = email.strip()
      data_var = AlterUser._select_data_user(self, email, curs)
      AlterUser._alter_data_user(self, data_var, conn, curs)
    print("Сделано.")
    return

  def _select_data_user(self, d_var, curs):
    if type(d_var) == int:
      # d_var = np.int32(d_var)email@var.ew
      curs.execute("""select u.id_users, u.name, u.subname, pu.id_phone,  pu.phone_user from phone_user pu 
  join users u on u.email_user = pu.email_user 
  where pu.phone_user = %s;""", (d_var,))
      data_var = curs.fetchall()
      print(data_var)

    if type(d_var) == str:
      curs.execute("""select u.id_users, u.name, u.subname, pu.id_phone,  pu.phone_user from phone_user pu 
  join users u on u.email_user = pu.email_user 
  where pu.email_user = %s;""", (d_var,))
      data_var= (curs.fetchall())

      for c in data_var:
       print(c)
    return data_var

  def _alter_data_user(self, data_var, conn, curs):
    print("""Меняем: Имя Фамилию или телефон""")
    old_var, new_var = input("old: "), input("new: ")
    old_var = (old_var).strip().replace("-", "").replace(" ", "").lstrip("+7").lstrip("8")
    new_var = (new_var).strip().replace("-", "").replace(" ", "").lstrip("+7").lstrip("8")

    text_var = re.compile(r"[^0-9*\s\W][a-zа-яё]*", re.I)
    integer_var = re.compile(r"[0-9*]{3,}[^a-zа-яё]*", re.I)




    for i in range(len(data_var)):
      for ind in range(len(data_var[i])):

        if re.match(text_var, old_var) and data_var[i][ind] == old_var:
          id_user_ver = data_var[i][0]

          if ind == 1:
            curs.execute("""update users set name = %s
            where id_users = %s;""", (new_var, id_user_ver))
          elif ind == 2:
            curs.execute("""update users set subname = %s
            where id_users = %s;""", (new_var, id_user_ver))

          conn.commit()


        elif re.match(integer_var, old_var) and data_var[i][ind] == int(old_var):
          id_phone_var = data_var[i][3]

          curs.execute("""update phone_user set phone_user = %s
          where id_phone = %s;""", (int(new_var), id_phone_var))
          conn.commit()

