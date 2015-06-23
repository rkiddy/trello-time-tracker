
from os.path import expanduser

import urllib2
import json

prefs_file = open('%s/.trello' % expanduser("~"), 'r')

prefs = json.loads(prefs_file.read())

api_key = prefs['api_key']
api_secret = prefs['api_secret']
oath_token = prefs['oath_token']

# user_url = "https://trello.com/1/members/me?key=%s&token=%s" % (api_key, oath_token)
# print "user_url: %s" % user_url

boards_url = "https://trello.com/1/members/my/boards?key=%s&token=%s" % (api_key, oath_token)
# print "boards_url: %s" % boards_url

boards = json.load(urllib2.urlopen(boards_url))   

# print data

for board in boards:

    if board['closed']:
        print "\nboard: %s (CLOSED)" % board['name']
    else:
        print "\nboard: %s, id: %s" % (board['name'], board['id'])

        lists_url = "https://trello.com/1/boards/%s/lists?key=%s&token=%s" % (board['id'], api_key, oath_token)
        # print lb2.urlopen(boards_url)lists_url

        lists = json.load(urllib2.urlopen(lists_url))

        # print lists

        for list in lists:

            if list['closed']:
                print "\n    list: %s, id: %s (CLOSED)" % (list['name'], list['id'])
            else:
                print "\n    list: %s, id: %s" % (list['name'], list['id'])

                cards_url = "https://trello.com/1/lists/%s/cards?key=%s&token=%s" % (list['id'], api_key, oath_token)

                cards = json.load(urllib2.urlopen(cards_url))

                for card in cards:

                    if card['closed']:
                        print "\n        card: %s, id: %s (CLOSED)" % (card['name'], card['id'])
                    else:
                        print "\n        card: %s, id: %s" % (card['name'], card['id'])

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
