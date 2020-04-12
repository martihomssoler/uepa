#!/bin/sh

nohup python3 source/client_bot.py > source/client.out  2 > source/client_2.out &

nohup python3 source/shop_bot.py > source/shop.out 2 > source/shop_2.out &

