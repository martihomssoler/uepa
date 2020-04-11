# -*- coding: utf-8 -*-

import sqlite3

class ShopDB():

    def __init__(self, file_path):
        self.file_path = file_path
        self.initialize_db()

    def initialize_db(self):
        self.connection = sqlite3.connect(self.file_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table'
                            AND name='shops' ''')
        if (self.cursor.fetchone()[0] == 0):
            self.cursor.execute('create table shops (id integer, longitude real, ' + 
                                'latitude real, name text, description text, categories text)')
        self.connection.commit()

    def add(self, shop_id: int, longitud: float, latitud: float):
        self.cursor.execute('insert into shops (id, longitude, latitude) values (?, ?, ?)', 
                             (shop_id, longitud, latitud))
        self.connection.commit()
    
    def set_name(self, shop_id: int, name: str):
        self.cursor.execute('update shops set name = ? where id = ?', 
                            (name,shop_id))
        self.connection.commit()
    
    def set_description(self, shop_id: int, description: str):
        self.cursor.execute('update shops set description = ? where id = ?', 
                            (description,shop_id))
        self.connection.commit()
    
    def add_category(self, shop_id: int, category: str):
        self.cursor.execute('select categories from shops where id = ?', 
                            (shop_id,))
        
        cat_list = self.cursor.fetchone()[0]
        if (cat_list != None):
            cat_list = cat_list + ', ' + category
        else:
            cat_list = category

        self.set_categories(shop_id, cat_list)

    def set_categories(self, shop_id: int, categories: str):
        self.cursor.execute('update shops set categories = ? where id = ?', 
                            (categories, shop_id))
        self.connection.commit()
    
    def get(self, shop_id: int):
        self.cursor.execute('select * from shops where id = ?', (shop_id,))
        ret_val = []
        for x in self.cursor.fetchone():
            ret_val.append(x)
        return ret_val

    def remove(self, identifier: int):
        self.cursor.execute('''delete from shops where id=?''', (identifier,))
        self.connection.commit()

    def flush_db(self):
        self.cursor.execute('''delete from shops;''')
        self.connection.commit()