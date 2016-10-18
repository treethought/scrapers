#!/usr/bin/env
import shutil
import os

from bs4 import BeautifulSoup as bs
import praw
import requests
from pprint import pprint

from reddit_secrets import *
from config import *

import youtube_dl as yt


class RedditBot(object):
    """docstring for RedditBot"""

    def __init__(self, user_agent=USER_AGENT, username=USERNAME, password=PASSWORD):

        self.user_agent = user_agent
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login()

    def login(self):
        self._r = praw.Reddit(user_agent=USER_AGENT)
        self._r.login(self.username, self.password, disable_warning=True)

    def get_soup(url):
        response = requests.get(url)
        response.raise_for_status()
        return bs(response.text, 'html.parser')

    @property
    def reddit(self):
        if not self._r:
            self.login()
        return self._r

    def get_new_posts(self, subreddit, limit=25):
        sub = self.reddit.get_subreddit(subreddit)
        for post in sub.get_new(limit=limit):
            yield post

    def download_image(self, post):  # TODO: some posts don't have preview key
        print('Dowloading {}'.format(post.title))
        try:
            img_url = post.preview['images'][0]['source']['url']
            sub_dir = os.path.join(PICS, str(post.subreddit))
            os.makedirs(sub_dir, exist_ok=True)

            response = self.session.get(img_url, stream=True)
            response.raise_for_status()
            with open(os.path.join(sub_dir, post.title + '.png'), 'wb+') as f:
                shutil.copyfileobj(response.raw, f)

        except AttributeError as e:
            print(e)
            print('{} didnt work id --- {}'.format(post.title, post.id))

    def download_audio(self, post, audio_only=True):  # TODO: downloads as opus right now, audio missing when mp3

        if audio_only:
            sub_dir = os.path.join(MUSIC, str(post.subreddit))
        else:
            sub_dir = os.path.join(VIDEO, str(post.subreddit))

        os.makedirs(sub_dir, exist_ok=True)
        title = post.title.split(' [')[0]
        out_file = sub_dir + '/{}'.format(title)

        audio_options = {
            'format': 'bestaudio/best',  # choice of quality
            'extractaudio': audio_only,  # only keep the audio
            'audioformat': "opus",  # convert to mp3
            'outtmpl': out_file,  # name the file the ID of the video
            'noplaylist': True,  # only download single song, not playlist
            # 'addmetadata': True,
            'quiet': True,
        }


        with yt.YoutubeDL(audio_options) as youtube:
            youtube.download([post.url])


    def detect_media_type(self, post):

        if not post.media:
            print('No media for {}'.format(post.title))
            print('Domain was {}'.format(post.domain))

        if post.media:
            if post.domain == 'imgur.com':
                return 'img'
            else:
                try:
                    print('trying to download {} from {}'.format(post.title, post.domain))
                    self.download_audio(post)
                except Exception as e:
                    print(e)
                    print('Cant download {} from {}'.format(str(post.title), post.domain))

        else:
            self.download_image(post)



if __name__ == '__main__':

    bot=RedditBot()
    posts=bot.get_new_posts('truemusic')
    for post in posts:
        bot.detect_media_type(post)
