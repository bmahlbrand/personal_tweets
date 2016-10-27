from FileFunc import FileFunc
from twokenize import simpleTokenize


def split(filename):
    tweets = FileFunc.read_file_into_list_unicode('tweets.csv')

    data = []
    for tweet in tweets:
        tmp = tweet.split(',')
        data.append({'user': tmp[0], 'tweet': simpleTokenize(tmp[1])})

    return data


def get_hashtag_users(hashtag):
    pass


def parse():
    hashtags = FileFunc.read_file_into_list('allhashtags.csv') #gather hashtags

    tweets = split('tweets.csv') #parse the tweet data
    tweets.pop(0) #remove header


    users = [] #collect all unique users
    for tweet in tweets:
        if tweet['user'] not in users:
            users.append(tweet['user'])
    # print(users)
    # print(tweets)

    tagdict = {}
    for hashtag in hashtags: #initialize lists
        tagdict[hashtag] = []

    for tweet in tweets: #check all tweets, hashtags and map users to hashtags
        for hashtag in hashtags:
            if hashtag in tweet['tweet']:
                if tweet['user'] not in tagdict[hashtag]:
                    tagdict[hashtag].append(tweet['user'])
                # print(tweet) #add user to hashtag dictionary

    edgemap = {}

    for hashtag in tagdict:
        if len(tagdict[hashtag]) > 1:
            tagdict[hashtag].sort()

    for hashtag in tagdict:
        if len(tagdict[hashtag]) > 1:

            for user1 in tagdict[hashtag]:
                for user2 in tagdict[hashtag]:
                    if user1 != user2:
                        l = sorted((user1, user2))
                        key = (l[0], l[1])
                        if key in edgemap:
                            edgemap[key] += 1
                        else:
                            edgemap[key] = 1

    # print(edgemap)
    # print(tagdict)
    with open('edge.csv', 'w') as f:
         f.write('User1,User2,ComFreq\n')

    with open('edge.csv', 'a') as f:
        for edge in edgemap.items():
            f.write(str(edge[0][0]) + ',' + str(edge[0][1]) + ',' + str(edge[1]) + '\n')


def combine(filename1, filename2):
    list1 = FileFunc.read_file_into_list(filename1)

    list2 = FileFunc.read_file_into_list(filename2)

    print(list1)

    combinedMap = {}

    list1.pop(0)

    for e in list1:
        tokens = e.split(',')
        combinedMap[(tokens[0], tokens[1])] = 0

    list2.pop(0)
    for e in list2:
        tokens = e.split(',')
        combinedMap[(tokens[0], tokens[1])] = 0


    for e in list1:
        tokens = e.split(',')
        combinedMap[(tokens[0], tokens[1])] += int(tokens[2])

    for e in list2:
        tokens = e.split(',')
        combinedMap[(tokens[0], tokens[1])] += int(tokens[2])

    with open('combinedEdges.csv', 'w') as f:
        f.write('User1,User2,ComFreq\n')

    with open('combinedEdges.csv', 'a') as f:
        for edge in combinedMap.items():
            f.write(str(edge[0][0]) + ',' + str(edge[0][1]) + ',' + str(edge[1]) + '\n')

    # print(combinedMap)
    # for e in list2:
    #     combinedMap[]

if __name__ == '__main__':
    # parse()
    combine('edge.csv', 'data/User_Network_Table.csv')