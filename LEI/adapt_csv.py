import csv
with open('dataset.csv', newline='', encoding="utf-8") as csvfile:
    csv_reader = csv.DictReader(csvfile,  fieldnames=["id","conversation_id","created_at","date","time","timezone","user_id","username",	"name","place",	"tweet","language",	"mentions",	"urls",	"photos","replies_count",	"retweets_count","likes_count",	"hashtags",	"cashtags",	"link","retweet",	"quote_url",	"video",	"thumbnail"	,"near"	,"geo"	,"source",	"user_rt_id","user_rt","retweet_id",	"reply_to",	"retweet_date",	"translate",	"trans_src",	"trans_dest"] )
    csv_reader.__next__()
    
    for row in csv_reader:
        print(row["tweet"])