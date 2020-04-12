# -*- coding: utf-8 -*-

import sqlite3

class Shop():
    def __init__(self, name, description, phone_number, owner_id, categories):
        self.name = name
        self.description = description
        self.phone_number = phone_number
        self.owner_id = owner_id
        self.categories = categories

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
            self.cursor.execute('create table shops (id integer primary key, longitude real, ' + 
                                'latitude real, name text, description text, ' + 
                                'categories text, phone_number text)')
        self.connection.commit()

    def add(self, shop_id: int, longitude: float, latitude: float):
        self.cursor.execute('''insert or replace into shops (id, longitude, latitude) 
                               values (?, ?, ?)''', 
                             (shop_id, longitude, latitude))
        self.connection.commit()
    
    def set_phone_number(self, shop_id: int, phone_number: str):
        self.cursor.execute('update shops set phone_number = ? where id = ?', 
                            (phone_number,shop_id))
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
        if (cat_list != None and len(cat_list) > 0):
            cat_list = cat_list + ', ' + category
        else:
            cat_list = category

        self.set_categories(shop_id, cat_list)

    def set_categories(self, shop_id: int, categories: str):
        self.cursor.execute('update shops set categories = ? where id = ?', 
                            (categories, shop_id))
        self.connection.commit()
    
    def get_all(self):
            self.cursor.execute('''select * from shops''')
            shop_row = self.cursor.fetchall()
            shops = []
            for row in shop_row:
                print(row)
                new_shop = Shop(row[3], row[4], row[6], row[0], row[5])
                shops.append(new_shop)
            return shops

    def get(self, shop_id: int):
        self.cursor.execute('select * from shops where id = ?', (shop_id,))
        shop_row = self.cursor.fetchone()
        return Shop(shop_row[3], shop_row[4], shop_row[6], shop_row[0], shop_row[5])

    def remove(self, identifier: int):
        self.cursor.execute('''delete from shops where id=?''', (identifier,))
        self.connection.commit()

    def flush_db(self):
        self.cursor.execute('''delete from shops;''')
        self.connection.commit()