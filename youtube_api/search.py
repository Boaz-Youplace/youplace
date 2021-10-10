#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
# from Google import Create_Service

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDweYriWH-xpyKILmBNK1fdg-yx4yA6Azg"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

search_response = youtube.search().list(
q = "제주 동부 vlog",
order = "date",
part = "snippet",
maxResults = 30
).execute()

# video_response = youtube.videos().list(
# q = "제주 동부 vlog",
# order = "date",
# part = "snippet",
# maxResults = 10
# ).execute()

titles = []
descriptions = []

for i in search_response['items']:
  #print(i)
  titles.append(i['snippet']['title'])
  descriptions.append(i['snippet']['description'])
  #video = i['id']['videoId']
  # video_response = youtube.videos().list(
  # id = i['id']).execute()
  #print(video_response)
  #descriptions.append(i['id']['videoId']['description'])
  #print('######################')
# print("000000000000000000000000000000000000",video_response)
print("title!!!",titles)
print("description!!!",descriptions)
print(len(titles), len(descriptions))
