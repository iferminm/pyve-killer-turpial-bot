#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite

from libturpial.api.models.account import Account
from libturpial.api.core import Core

import argparse

core = Core()
accounts = core.list_accounts()

def register_account(username):
    account = username + '-twitter'
    if account in accounts:
        print('sorry, your account is already registered')
    else:
        new_access = Account.new('twitter')
        url = new_access.request_oauth_access()
        print("Please go to the following URL, log-in and allow access for Libturpial. Then write the PIN in here.")
        print url
        cod = raw_input('PIN:')
        new_access.authorize_oauth_access(cod)
        core.register_account(new_access)
        
def list_accounts():
    for account in accounts:
        print account

def send_message(username, message):
    account = username + '-twitter'
    if account in accounts:
        core.update_status(account, message)
    else:
        register_account(username)

def show_help():
    print('say something')
    
def cron_stuff():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help='list registred accounts', action='store_true')
    parser.add_argument('-r', '--register', nargs=1, help='add account to register')
    parser.add_argument('-s', '--sendtweet', nargs=2, help='send a tweet as a cli tool')
    args = parser.parse_args()
    if args.list:
        list_accounts()
    elif args.register:
        register_account(args.register[0])
    elif args.sendtweet:
        send_message(args.sendtweet[0], args.sendtweet[1])
    else:
        show_help()
