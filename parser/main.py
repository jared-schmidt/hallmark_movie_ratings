"""
Main
"""

# import pymongo
import json
import time
import urllib
import requests

# myclient = pymongo.MongoClient("mongodb://admin:SuperPassword1!@ds059471.mlab.com:59471/hall_movies")
# mydb = myclient["hall_movies"]
# mycol = mydb["movies"]

# FILE = open("sample.txt", "r")

YEARS = [2014, 2015, 2016, 2017, 2018]

arr = []

for year in YEARS:
    FILE = open("parser/" + str(year) + ".txt", "r")
    for line in FILE.readlines():
        line = line.replace("\n", "")
        query = urllib.parse.quote(line)
        # print(query)
        url = "https://api.themoviedb.org/3/search/movie?api_key=afba8128a9cf4cde67b1f44dbb5f5e2f&language=en-US&query=" + query + "&page=1&include_adult=false&year=" + str(year)
        url_ratings = "http://www.omdbapi.com/?t=" + line.replace(" ", "+") +"&apikey=c68b89d4"
        resp = requests.get(url)
        data = resp.json()
        resp2 = requests.get(url_ratings)
        data2 = resp2.json()
        # print(data2)
        try:
            if data["total_results"] >= 1:
                # print("GOOD")
                d = data["results"][0]
                foo = {
                    "name": d["title"],
                    "vote_average": d["vote_average"],
                    "popularity": d["popularity"],
                    "vote_count": d["vote_count"],
                    "id": d["id"],
                    "ratings": data2["Ratings"],
                    "year": year
                }

                # print(data2["Ratings"])
                arr.append(foo)
                # print(json.dumps(data, indent=2, sort_keys=True))
            else:
                print("BAD : " + str(data["total_results"]))
                # print(data)
                # print(json.dumps(data, indent=2, sort_keys=True))
        except:
            print(url)
            print("BAD BAD ERROR: " + line)
            # print(json.dumps(data, indent=2, sort_keys=True))
            pass
        time.sleep(1)

    FILE.close()

FILE = open("data.txt", "w")
with open('your_file.txt', 'w') as f:
    FILE.write("[")
    for item in arr:
        FILE.write("%s,\n" % item)
    FILE.write("]")
FILE.close()
