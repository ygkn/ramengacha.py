import urllib.request
import json

apikey = "AIzaSyAOqwUYekkyQ4y3EgmXmhST4oMqckVmiVU"
def get_ramenshop(location, radius):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=" +  apiKey + "&location=" + str(location.lat) + "," + str(location.lng) + "&radius=" + str(radius) + "&keyword=ラーメン屋"

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = json.load(res)

        print(body)

if __name__ == '__main__'
    get_ramenshop({lat:34.9821826 ,lng:135.9610467}, 4000)