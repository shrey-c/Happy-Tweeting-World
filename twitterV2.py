#!/usr/bin/env python

#-----------------------------------------------------------------------
# twitter-search-geo
#  - performs a search for tweets close to New Cross, London,
#    and outputs them to a CSV file.
#-----------------------------------------------------------------------

from twitter import *

import sys
import csv
import time
consumer_key = 'T7eP9f6XoHjYS6qITDlRA5VTc'

consumer_secret = 'LjXdLvvYc0SdYDJGuOnaLuS7zRK4vIyHhRWBrXrUKh1TShV4aj'

access_key = '1034296635243737088-kFHM3Hi5szDKMdhWdQg4GuDP0ca4HZ'

access_secret = '2ZEwElzsVvS4M7Eh5aeNYYQlhwUCzmFcYsTRQcYpo06KO'

for index, row in citiesmergedf.iterrows():
    if(index < 565):
        continue
    latitude = row['lat']    # geographical centre of search
    longitude = row['lng']    # geographical centre of search
    max_range = 50             # search range in kilometres
    num_results = 100        # minimum results to obtain
    outfile = 'lang_output' + row['Country name'] + '.csv'  # output file
    country = row['Country name']

    #-----------------------------------------------------------------------
    # load our API credentials
    #-----------------------------------------------------------------------
    import sys
    sys.path.append(".")
    #import config

    #-----------------------------------------------------------------------
    # create twitter API object
    #-----------------------------------------------------------------------
    twitter = Twitter(auth=OAuth(access_key,
                                 access_secret,
                                 consumer_key,
                                 consumer_secret))

    #-----------------------------------------------------------------------
    # open a file to write (mode "w"), and create a CSV writer object
    #-----------------------------------------------------------------------
    csvfile = open(outfile, "w")
    csvwriter = csv.writer(csvfile)

    #-----------------------------------------------------------------------
    # add headings to our CSV file
    #-----------------------------------------------------------------------
    row = ["user", "text", "country", "id"]
    csvwriter.writerow(row)
    #-----------------------------------------------------------------------
    # the twitter API only allows us to query up to 100 tweets at a time.
    # to search for more, we will break our search up into 10 "pages", each
    # of which will include 100 matching tweets.
    #-----------------------------------------------------------------------
    result_count = 0
    last_id = None
    fetch_count = 0
    while result_count < num_results:
        #-----------------------------------------------------------------------
        # perform a search based on latitude and longitude
        # twitter API docs: https://dev.twitter.com/rest/reference/get/search/tweets
        #-----------------------------------------------------------------------
        query = twitter.search.tweets(q="", geocode="%f,%f,%dkm" % (latitude, longitude, max_range), lang='en', count=100, max_id=last_id)

        for result in query["statuses"]:
            # if result["geo"]:
            user = result["user"]["screen_name"]
            text = result["text"]
            text = text.encode('ascii', 'replace')
            # print(text)
            id = result["id"]
            # latitude = result["geo"]["coordinates"][0]
            # longitude = result["geo"]["coordinates"][1]

            #-----------------------------------------------------------------------
            # now write this row to our CSV file
            #-----------------------------------------------------------------------
            row = [user, text, country, id]  # , latitude, longitude ]
            csvwriter.writerow(row)
            result_count += 1
            last_id = result["id"]

        #-----------------------------------------------------------------------
        # let the user know where we're up to
        #-----------------------------------------------------------------------
        print("got %d results" % result_count)
        fetch_count += 1
        if(fetch_count > 5):  # number of repeats for a new tweet that it needs to do per request
            repeater.append(country)
            break

    #-----------------------------------------------------------------------
    # we're all finished, clean up and go home.
    #-----------------------------------------------------------------------
    csvfile.close()

    print("written to %s" % outfile)
