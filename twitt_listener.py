# -*- coding: utf8 -*-

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import SQL_util
import datetime

ckey =
csecret = 
atoken =
asecret = 
keywords = ['니다.', '다.', '아요.', '한다.', '했다.', '있다.', '없다.', '다!', '까?']
month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


class Listener(StreamListener):
    def on_data(self, data):
        print('\n----------------------------------------------------')
        try:
            data = data.encode("utf-8")
            data = data.decode('unicode_escape')
            for keyword in keywords:
                if data.find(keyword) > 0:
                    data = data.replace('{','')
                    data = data.replace('}','')
                    data_list = data.split(',"')
                    a = 1
                    insert_list = []

                    for tweet in data_list:
                        tweet_item = tweet.split('":')[-1]
                        tweet_item = tweet_item.replace('"','')
                        if a == 1:
                            self.seperater_date(tweet_item)
                            insert_list.append(self.seperater_date(tweet_item))
                        elif a == 3:
                            a += 1
                            continue
                        else:
                            insert_list.append(tweet_item)
                        a += 1
                        if a == 5:
                            break
                    print(insert_list)

                    insert_data = "'"+insert_list[0]+"', "+insert_list[1]+", '"+insert_list[2]+"'"
                    print(insert_data)
                    try:
                        SQL_util.insert(insert_data)
                        continue
                    except:
                        print('error')


        except UnicodeEncodeError:
            print("UnicodeEncodeError")
        print('----------------------------------------------------\n')
        return True

    def on_error(self, status):
        print('error : ', status)

    def seperater_date(self, row_str):
        date = '2016 '
        date += row_str[4:16]
        date = date.replace(' ','')
        date_obj = datetime.datetime.strptime(date, '%Y%b%d%H:%M')
        date_diff = date_obj + datetime.timedelta(hours=9)
        result = ('%s/%s/%s' % (date_diff.year, date_diff.month, date_diff.day))
        print(':',result, ':')
        return result



auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, Listener())
twitterStream.filter(track=keywords)
#twitterStream.filter(languages='ko')
