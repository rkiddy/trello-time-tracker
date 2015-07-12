#!/usr/bin/python

from os.path import expanduser

import urllib2
import json
import sys

prefs_file = open('%s/.trello' % expanduser("~"), 'r')

prefs = json.loads(prefs_file.read())

api_key = prefs['api_key']
api_secret = prefs['api_secret']
oath_token = prefs['oath_token']

list_todo = 0
list_doing = 0
list_done = 0
list_all = 0

for arg in sys.argv:
    if arg == 'todo':
        list_todo = 1
    if arg == 'doing':
        list_doing = 1
    if arg == 'done':
        list_done = 1
    if arg == 'all':
        list_all = 1

if not list_todo and not list_doing and not list_done and not list_all:
    print ''
    print 'Please tell me what to show: todo, doing, done, or all'
    print ''
    exit()

# user_url = "https://trello.com/1/members/me?key=%s&token=%s" % (api_key, oath_token)
# print "user_url: %s" % user_url

boards_url = "https://trello.com/1/members/my/boards?key=%s&token=%s" % (api_key, oath_token)
# print "boards_url: %s" % boards_url

boards = json.load(urllib2.urlopen(boards_url))

board_ids = {}

# print data

for board in boards:

    # we need only look at open boards.
    #
    if not board['closed']:

        org_url = "https://trello.com/1/boards/%s/organization?key=%s&token=%s" % (board['id'], api_key, oath_token)

        try:
            organization = json.load(urllib2.urlopen(org_url))
            org_name = organization['name']
        except urllib2.HTTPError, e:
            if e.code == 404:
                org_name = 'None'
            else:
                org_name = 'Else'

        if org_name != 'doitsa':

            board_ids[board['name']] = board['id']

            lists_url = "https://trello.com/1/boards/%s/lists?key=%s&token=%s" % (board['id'], api_key, oath_token)

            lists = json.load(urllib2.urlopen(lists_url))

            # print lists

            for list in lists:

                if list['closed']:
                    pass

                elif list_all or (list_doing and list['name'] == 'Doing'):
                    
                    cards_url = "https://trello.com/1/lists/%s/cards?key=%s&token=%s" % (list['id'], api_key, oath_token)

                    cards = json.load(urllib2.urlopen(cards_url))

                    for card in cards:

                        if not card['closed']:

                            print "\n%s, %s, %s (id: %s)" % (board['name'], list['name'], card['name'], card['id'])

                elif list_todo and (list['name'] == 'ToDo' or list['name'] == 'To Do'):

                    cards_url = "https://trello.com/1/lists/%s/cards?key=%s&token=%s" % (list['id'], api_key, oath_token)

                    cards = json.load(urllib2.urlopen(cards_url))

                    for card in cards:

                        if not card['closed']:

                            print "\n%s, %s, %s (id: %s)" % (board['name'], list['name'], card['name'], card['id'])

                elif list_done and list['name'] == 'Done':

                    cards_url = "https://trello.com/1/lists/%s/cards?key=%s&token=%s" % (list['id'], api_key, oath_token)

                    cards = json.load(urllib2.urlopen(cards_url))

                    for card in cards:

                        if not card['closed']:

                            print "\n%s, %s, %s (id: %s)" % (board['name'], list['name'], card['name'], card['id'])

print ''

#                        desc_url = "https://trello.com/1/cards/%s/desc?key=%s&token=%s" % (card['id'], api_key, oath_token)
#                        print "\n\ndesc: %s" % json.load(urllib2.urlopen(desc_url))
#                        members_url = "https://trello.com/1/cards/%s/members?key=%s&token=%s" % (card['id'], api_key, oath_token)
#                        print "\n\nmembers: %s" % json.load(urllib2.urlopen(members_url))
#                        print "\n"
#
# Examples from this point:
#
# $ curl 'https://trello.com/1/cards/BOARD_ID/desc?key=KEY&token=TOKEN'
# {"_value":"2015-04-22 12:30 - 13:00"}
# $
# $ curl 'https://trello.com/1/cards/BOARD_ID/desc?key=KEY&token=TOKEN'
# {"_value":"2014-04-22 13:00 - 14:00\n2014-04-22 14:30 - 16:30\n2014-04-22 12:00 - 14:00\n2014-04-24 16:00 - 17:30\n2014-04-27 12:00 -"}
# $
