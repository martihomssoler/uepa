import sqlite3


class Advertisement:
    def __init__(self, message, identifier, owner_id):
        self.message = message
        self.id = identifier
        self.owner_id = owner_id

    def get_message(self):
        return self.message


class AdvertisementDB():

    def __init__(self, file_path):
        self.file_path = file_path
        self.initialize_db()

    def initialize_db(self):
        self.connection = sqlite3.connect(self.file_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table'
                            AND name='advertisements' ''')
        if (self.cursor.fetchone()[0] == 0):
            self.cursor.execute('''create table advertisements
                        (id integer primary key, advertisement_message text,
                owner_id integer, date date)''')

        self.connection.commit()

    def get_all(self):
        self.cursor.execute(''' select * from advertisements ''')
        ad_rows = self.cursor.fetchall()
        ads = []
        for row in ad_rows:
            print(row)
            new_ad = Advertisement(row[1], row[0], row[2])
            ads.append(new_ad)
        return ads

    def add(self, message):
        self.cursor.execute('''insert into advertisements
                            (advertisement_message, owner_id, date) values
                            (?, 1, '2020-04-10') ''', (message,))
        self.connection.commit()
    
    def remove(self, identifier):
        self.cursor.execute('''delete from advertisements where id=?''', (identifier,))
        self.connection.commit()

    def flush_db(self):
        self.cursor.execute(''' delete from advertisements; ''')
