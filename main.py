from module.alter_user import AlterUser
import psycopg2 as psy

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
        user = AlterUser()
        user.alter_user(conn, curs)

      elif r == 'ex':
        exit()

