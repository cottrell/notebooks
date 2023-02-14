#!/usr/bin/env python
import os
import json
import twitter
cred = json.load(open(os.path.expanduser('~/.cred/twitter/cred.json')))
api = twitter.Api(consumer_key=cred['consumer_key'],
                      consumer_secret=cred['consumer_secret'],
                      access_token_key=cred['access_token_key'],
                      access_token_secret=cred['access_token_secret'])
# To see if your credentials are successful:

print(api.VerifyCredentials())
# {"id": 16133, "location": "Philadelphia", "name": "bear"}

# the Gets
cmds = [
        'GetAppOnlyAuthToken',
        'GetHelpConfiguration',
        'GetShortUrlLength',
        'GetSearch',
        'GetUsersSearch',
        'GetTrendsCurrent',
        'GetTrendsWoeid',
        'GetUserSuggestionCategories',
        'GetUserSuggestion',
        'GetHomeTimeline',
        'GetUserTimeline',
        'GetStatus',
        'GetStatuses',
        'GetStatusOembed',
        'GetUserRetweets',
        'GetReplies',
        'GetRetweets',
        'GetRetweeters',
        'GetRetweetsOfMe',
        'GetBlocks',
        'GetBlocksPaged',
        'GetBlocksIDs',
        'GetBlocksIDsPaged',
        'GetMutes',
        'GetMutesPaged',
        'GetMutesIDs',
        'GetMutesIDsPaged',
        'GetFollowerIDsPaged',
        'GetFriendIDsPaged',
        'GetFollowerIDs',
        'GetFriendIDs',
        'GetFollowersPaged',
        'GetFriendsPaged',
        'GetFollowers',
        'GetFriends',
        'GetUser',
        'GetDirectMessages',
        'GetSentDirectMessages',
        'GetFavorites',
        'GetMentions',
        'GetSubscriptions',
        'GetMemberships',
        'GetListsList',
        'GetListTimeline',
        'GetListMembersPaged',
        'GetListMembers',
        'GetListsPaged',
        'GetLists',
        'GetStreamSample',
        'GetStreamFilter',
        'GetUserStream'
        ]

if __name__ == '__main__':
    cmds = [getattr(api, k) for k in cmds]
    import argh
    argh.dispatch_commands(cmds)
