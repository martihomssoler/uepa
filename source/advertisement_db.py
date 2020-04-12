import sqlite3

class Advertisement:
    def __init__(self, message, identifier, owner_id):
        self.message = message
        self.id = identifier
        self.owner_id = owner_id

class AdvertisementDB():

    def __init__(self, file_path):
        self.file_path = file_path
        self.initialize_db()

    def initialize_db(self):
        self.connection = sqlite3.connect(self.file_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table'
                            AND name='advertisements' ''')
        if (self.cursor.fetchone()[0] == 0):
            self.cursor.execute('''create table advertisements
                        (id integer primary key, advertisement_message text, owner_id integer)''')

        self.connection.commit()

    def get_all(self):
        self.cursor.execute('''select * from advertisements''')
        ad_rows = self.cursor.fetchall()
        ads = []
        for row in ad_rows:
            print(row)
            new_ad = Advertisement(row[1], row[0], row[2])
            ads.append(new_ad)
        return ads

    def get(self, identifier: int):
        self.cursor.execute('''select * from advertisements where id=?''', (identifier,))
        ad_row = self.cursor.fetchone()
        return Advertisement(ad_row[1], ad_row[0], ad_row[2])

    def add(self, owner_id: int, message: str):
        self.cursor.execute('''insert into advertisements
                            (advertisement_message, owner_id) values (?, ?) ''',
                            (message, owner_id))
        self.connection.commit()
    
    def remove(self, identifier: int):
        self.cursor.execute('''delete from advertisements where id=?''', (identifier,))
        self.connection.commit()

    def flush_db(self):
        self.cursor.execute(''' delete from advertisements; ''')
        self.connection.commit()
