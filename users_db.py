import sqlite3
from enum import Enum

# 
class UserFlags(Enum):
     FLAG_ADD = 1
     FLAG_REMOVE = 2

class UsersDB():

    def __init__(self, file_path):
        self.file_path = file_path
        self.initialize_db()

    def initialize_db(self):
        self.connection = sqlite3.connect(self.file_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table'
                            AND name='users' ''')
        if (self.cursor.fetchone()[0] == 0):
            self.cursor.execute('create table users (id integer, ' + UserFlags.FLAG_ADD.name + 
                                ' boolean, ' + UserFlags.FLAG_REMOVE.name + ' boolean)')
        self.connection.commit()

    def add(self, user_id: int):
        self.cursor.execute('insert into users (id, ' + UserFlags.FLAG_ADD.name + ', ' +
                             UserFlags.FLAG_REMOVE.name + ') values (?, False, False)', 
                             (user_id,))
        self.connection.commit()
    
    def remove(self, identifier: int):
        self.cursor.execute('''delete from users where id=?''', (identifier,))
        self.connection.commit()

    def set_flag(self, userid: int, flag: UserFlags):
        self.change_flag(userid, flag, True)
    
    def unset_flag(self, userid: int, flag: UserFlags):
        self.change_flag(userid, flag, False)

    def change_flag(self, user_id: int, flag: UserFlags, value: bool):
        self.cursor.execute('update users set ' + flag.name + ' = ? where id = ?', 
                            (value, user_id))
        self.connection.commit()
    
    def get_flag(self, user_id: int, flag: UserFlags) -> bool:
        self.cursor.execute('select ' + flag.name + ' from users where id=?', 
                            (user_id,))
        return bool(self.cursor.fetchone()[0])

    def flush_db(self):
        self.cursor.execute('''delete from users;''')
        self.connection.commit()