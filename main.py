#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite

from libturpial.api.models.account import Account
from libturpial.api.core import Core

import argparse

MAX_STATUS_LENGTH = 140

core = Core()
accounts = core.list_accounts()

def build_account_id(username):
    return '%s-twitter' % username

def register_account(username):
    account = build_account_id(username)
    if account in accounts:
        print 'Your account is already registered. Nothing to do'
    else:
        new_access = Account.new('twitter')
        url = new_access.request_oauth_access()
        print "Please go to the following URL, log-in and allow access for libturpial. Then write the PIN in here."
        print url
        cod = raw_input('PIN:')
        new_access.authorize_oauth_access(cod)
        core.register_account(new_access)
        print "Account %s registered successfully" % new_access.id_

def list_accounts():
    for account in accounts:
        print account

def send_message(username, message, truncate):
    account = build_account_id(username)
    if account not in accounts:
        print "Your account is not registered yet, follow the steps to do it before you post"
        register_account(username)

    if message == '':
        print 'You must write something to post'
        return

    if len(message) > MAX_STATUS_LENGTH:
        if truncate:
            message = message[:MAX_STATUS_LENGTH]
        else:
            print "Your message is longer than %i chars and truncate is False" % MAX_STATUS_LENGTH
            return

    core.update_status(account, message)
    print "Message posted successfully"

def show_help():
    print 'say something'

def process_dms(truncate):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help='list registred accounts', action='store_true')
    parser.add_argument('-r', '--register', nargs=1, help='add account to register')
    parser.add_argument('-s', '--sendtweet', nargs=2, help='send a tweet as a cli tool')
    parser.add_argument('-t', '--truncate', help='truncate long messages', action='store_true')
    parser.add_argument('-p', '--processdms',
        help='fetch DMs from registered accounts and post them in TL', action='store_true')
    args = parser.parse_args()
    if args.list:
        list_accounts()
    elif args.register:
        register_account(args.register[0])
    elif args.sendtweet:
        send_message(args.sendtweet[0], args.sendtweet[1], args.truncate)
    elif args.processdms:
        process_dms(args.truncate)
    else:
        show_help()
