from config import LOGIN_DB, PASSWORD_DB  # CLIENT_SECRET
import psycopg2
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine, MetaData, Table, String
from sqlalchemy import Integer, Column, CheckConstraint  # Text,


class Iterator:
  def __init__(self, atr:  list):
    """
    :param atr:  Received list at  the Bot will be divide on an id
    """
    self.atr = atr

  def __iter__(self):

    return self

  def __next__(self):

    if self.atr == []:
      raise StopIteration
    for link in self.atr:
      respons = str(link).split("id").pop()
      self.atr.pop(0)
      return respons


class Botdb():
  def __init__(self, id_user=None, id_elected_user=None,
               id_status=None):
    self.id_elected_user = id_elected_user
    self.id_user = id_user
    self.id_status = id_status

  def __start(self):
    """
    Open the new session.
    """
    self.conn = psycopg2.connect(
      database="vkinder",
      user=LOGIN_DB,
      password=PASSWORD_DB
    )
    self.cur = self.conn.cursor()

  def __close(self):
    """
    : return:  Transaction is closing
    """
    self.conn.close()
    self.cur.close()

  def __exists(self, table_name: str, column_name: str, value_column_name,
               column_name_2=None, value_column_name_2=None):
    """
    This's method for checks 'value_column_name' on the presence
    'value_column_name' in db and  the condition
    :param table_name:  Table name when will search
    :param column_name:  Column of the table when will a search
    :param value_column_name:  The row for search in the table
    :param column_name_2:  This attribute for searching the elected id user which has
      been assigned status
    :param value_column_name_2:   For an authorized user  is elected id user is only unique
    : return:  rows as a result simply searching. Session not closed
    """
    if column_name_2 is None:
      """
      Will it have in db or not
      """

      self.cur.execute("""
  SELECT * FROM %s WHERE %s=%s;
  """ % (table_name, column_name, value_column_name))
      response = self.cur.fetchall()

    else:
      """
      It will look nique or not unique
      """

      self.cur.execute(
        """
        SELECT * FROM %s WHERE %s=%s and %s=%s;
        """ % (table_name, column_name, value_column_name,
               column_name_2, value_column_name_2
               )
        )
      response = self.cur.fetchall()
    return response

  def __listIdUser(self, table_name,
                   column_name,
                   user_id,
                   event_command,
                   id_elected_user,
                   value_column_name_2):
    """
    The Filter  - spend data with the black or white the status
    :param table_name:  The name table in the db.
    :param column_name:  The chosen column of the db
    :param user_id:  ID user passed path authorization.
    :param event_command:
    :param id_elected_user:  id electes user.
    :param value_column_name_2:
    :return:
    """

    response_exists = Botdb.__exists(
      self,
      table_name=table_name,
      column_name=column_name,
      value_column_name=user_id,
      column_name_2=id_elected_user,
      value_column_name_2=value_column_name_2
      )

    if event_command == 'add_favorites' and user_id != 0:
      if response_exists != []:

        print("the list 'favorites' has this Id_use")
        return "None"

      elif response_exists == []:
        return (user_id, 'favorites', id_elected_user)

    elif event_command == 'add_blacklist' and user_id != 0:
      if response_exists != []:
        print(f"the list 'blacklist' has this Id_use")
        return "None"

      elif response_exists == []:
        return (user_id, 'favorites', id_elected_user)

    else:
      print("Don't see the command - it need in a black or white list be adds!")
      exit()

  def selectData(self):
    """"
    Get a data of the table
    """
    Botdb.__start(self)
    self.cur.execute("""SELECT * FROM elected_users;""")
    response_select = self.cur.fetchall()

    self.conn.rollback()
    Botdb.__close(self)

    return response_select

  def insertElected(self, user_id, event_command, id_elected_user):
    """
    TODO: We take authorized user id and for this account written does been record
     to a black and favorite lists Authorized id not unique.
    :return:  None
    """
    Botdb.__start(self)
    response = Botdb.__listIdUser(
      self, table_name="elected_users",
      column_name="id_user",
      user_id=user_id,
      event_command=event_command,
      id_elected_user="id_elected_user",
      value_column_name_2=id_elected_user
      )

    self.id_user = user_id
    self.id_elected_user = id_elected_user

    if event_command == "add_favorites":
      self.id_status = 0

    elif event_command == "add_blacklist":
      self.id_status = 1

    if response != "None":
      self.cur.execute("""\
  INSERT INTO elected_users VALUES (%s, %s,%s);""" % (
        self.id_user,
        self.id_elected_user,
        self.id_status)
                       )
      self.conn.commit()
      Botdb.__close(self)
    return

  def insertUser(self, params: list):
    """
    TODO:  Data about the authorized user
     If id_user not exists in the table 'Users' then going recording a new data in the db and will see row  'id_vk'
     is in db'    If td has 'id_vk' when see row A new id_vk №-id_vk (id user which aitorisation in bot)  has been
     inserted in 'user' table.'
    :param params:  Params which gets from the bot when went executing 'start' command
    : return:  The user id is active
    """
    Botdb.__start(self)
    response = Botdb.__exists(self, "users", 'id_vk', params["id_vk"])

    if response == None:
      self.cur.execute(
        """INSERT INTO users VALUES (%s,'%s','%s',%s,%s,'%s');""" % (
          params["id_vk"], params["first_name"],
          params["last_name"], params["age"],
          params["id_sity"], params["tokens"])
      )
      print("A new id_vk %s has been inserted in 'user' table." % (params["id_vk"],))
      self.conn.commit()
    else:
      print("'id_vk' is in db")
    Botdb.__close(self)
    return params["id_vk"]

  def public_list(self, value_column_name):
    """
    :param value_column_name:  Integer - which tell about the user status, it is user of the favorite's list or of blacklist
    : return:  The single list of the temples, this contains only unique id user from the lists and a status number.
     The integer 1 this is a blacklist status and integer 0 - favorite list
    """
    Botdb.__start(self)
    respons = Botdb.__exists(self, "%s" % ("elected_users",),
                           "%s" % ("id_status",),
                           "%s" % (value_column_name,))
    Botdb.__close(self)
    return respons


class sqlTasks():
  def __init__(self, dbname,  password="%s" % ("nlo7", )):
    """
    :param dbname:  Receiving database-name and creating base.
    :param password:  'password' variable has from password default the 'nlo7'
    : return:  True or False
    TODO:def __exists() - checking:
      - True if dataBase-name be exists
      - False if not exists
      def __connectedPosgres() - connecting with a 'db-postgres'
      def __createdb() - Build new data-base if it not exists
      def connectionNewDB() - The buil connection for a new database.
      def templateTable() - The created templates for a new-db and returned tables from
      this's new db
    """

    self.dbname = dbname
    self.password = password

  def __connectedPosgres(self):
    """
    Basic requests the db-postgres default
    """
    return create_engine("postgresql://postgres: %s@localhost: 5432/postgres" % (self.password, ))

  def __createdb(self):
    """
    : return:  Build new data-base if it not exists
    """
    session = sqlTasks.__connectedPosgres(self)

    with session.connect() as conn:
      conn.execute("commit")

    url = 'postgresql://postgres:%s@localhost:5432/%s' % (self.password, self.dbname)
    if not sqlTasks.__exists(self):
      create_database(url)
      print("Created database!")
    else:
      print("""DataBase exists. Session is closing""")
      conn.close()
      return
      exit()

    conn.close()
    print("Session closed!")
    return

  def __exists(self):
    """
    :param dbname: dataBase-name checking:
      - True if dataBase-name be exists
      - False if not exists
    :return  True or False
    """
    return database_exists('postgresql://postgres:%s@localhost:5432/%s' % (self.password, self.dbname))

  def connectionNewDB(self):

    """
    :return: The buil connection for a new database.
    """
    sqlTasks.__createdb(self)

    return create_engine("postgresql://postgres:%s@localhost:5432/%s" % (self.password, self.dbname))

  def templateTable(self):
    """
    : return:  The created templates for a new-db and returned tables from this's new db
    """
    metadata = MetaData()
    engine = sqlTasks.connectionNewDB(self)

    users = Table(
      'users', metadata,
      Column('id_vk', Integer(), primary_key=True),
      CheckConstraint('id_vk >= 1' and 'id_vk <= 9999999999', name='id_check'),
      Column('first_name', String(20), nullable=False),
      Column('last_name', String(20), nullable=False),
      Column('age', Integer(), default=18),
      CheckConstraint('age >= 18' and 'age <= 99', name='user_age'),
      Column('id_sity', Integer(), nullable=False),
      Column('tokens', String(150), nullable=False)
    )

    filters = Table(
      'filters', metadata,
      Column('id', Integer(), primary_key=True),
      Column('code_filter', String(50))
    )

    status = Table(
      'status', metadata,
      Column('id', Integer(), primary_key=True),
      Column('type_status', String(12), default='defauList')
    )

    elected_user = Table(
      'elected_users', metadata,
      Column('id_user', sqlalchemy.ForeignKey("users.id_vk"), nullable=False),
      Column('id_elected_user', Integer(), nullable=False),
      CheckConstraint('id_elected_user >= 1' and 'id_elected_user <= 9999999999', name='id_elected_user'),
      Column('id_status', sqlalchemy.ForeignKey("status.id"), nullable=False)

    )
    metadata.create_all(engine)
    return (users, filters, status, elected_user)
