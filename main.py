import psycopg2 as psy
import re

def mine_menu():
  print("""
    создающая структуру БД -  с
    добавить нового клиента - a
    добавить телефон        - ph
    изменить данные         - al
    удалить телефон         - dp
    удалить клиента         - dc
    найти клиента           - s
    выйти                   - ex
  """)

  return

def create_db(conn, curs):
  curs.execute("""CREATE TABLE IF NOT EXISTS users (id_users SERIAL PRIMARY KEY, name VARCHAR(25) NOT NULL, 
      subname VARCHAR(25) NOT NULL, email_user VARCHAR(40) NOT NULL UNIQUE);""")
  curs.execute("""CREATE TABLE IF NOT EXISTS phone_user (id_phone SERIAL PRIMARY KEY, email_user TEXT NOT NULL 
      REFERENCES users (email_user), phone_user INTEGER NOT NULL UNIQUE);""")
  conn.commit()
  return

def insert_user(email_var, name_var, subn_var, conn, curs):
  curs.execute("""INSERT INTO users (email_user, name, subname) VALUES (%s, %s, %s) RETURNING email_user;""",\
 (email_var, name_var, subn_var))
  conn.commit()
  return

def insert_phone(email_var, phone_var,conn, curs):
  curs.execute("""insert into phone_user (email_user, phone_user) values (%s, %s) returning phone_user;""", (email_var, phone_var))
  conn.commit()
  return

def _select_data_user(d_var, curs):
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

def _alter_data_user(data_var, conn, curs):
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

def alter_user (conn, curs):
  print("""Введите пользовательские данные: телефон или email""")

  phone, email = input('phone: '), input('email: ')

  if phone != '':
    phone = int(phone.strip())
    data_var = _select_data_user(phone, curs)
    _alter_data_user(data_var, conn, curs)

  elif phone == '' and email == '' :
    exit()

  else:
    email = email.strip()
    data_var = _select_data_user(email, curs)
    _alter_data_user(data_var, conn, curs)
  print("Сжедано.")
  return


if __name__ == ('__main__'):

  # print(type(np.int32(33333333)))
  # print(np.int32(33333333))
  conn = psy.connect(
    database = "client_db",
    password = "nlo7",
    user = "postgres"
  )



with conn:
  with conn.cursor() as curs:
    mine_menu()

    while True:
      r = input(": ")
      r = r.lower().strip()

      if r == 'c':
        create_db(conn, curs)
      elif r == 'a':
        print("Добавить пользователя")
        name, sub, phone, emile  = input('name: '), input('subname: '), input('phone: '), input('email: ')
        phone = int((phone).strip().replace("-", "").replace(" ", "").lstrip("+7").lstrip("8"))

        insert_user(emile, name, sub, conn, curs)
        insert_phone(emile, phone, conn, curs)

      elif r == 'ph':
        print("Добавить телефон пользователя")
        phone, emile = input('phone: '), input('email: ')
        insert_phone(emile, phone, conn, curs)

      elif r == 'al':
        alter_user(conn, curs)

      elif r == 'ex':
        exit()

