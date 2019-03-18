#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import socket
import json

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

class TweetsListener(StreamListener):

    def __init__(self, socket):
        print('Tweet listener initialized')
        # Transmite o stream dos tweets para um socket na máquina local
        self.client_socket = socket

    def on_data(self, data):
        try:
            json_msg = json.loads(data)
            msg = json_msg['text'].encode('utf-8')
            print(msg)
            self.client_socket.send(msg)
        except BaseException as e:
            print('Error on data: {}'.format(str(e)))
        return True

    def on_error(self, status):
        print(status)
        return True

def connect_to_twitter(connection):
    j = json.loads(open('./secret.json').read())
    api_key = j['api_key']
    api_secret = j['api_secret']
    access_token = j['access_token']
    access_token_secret = j['access_token_secret']

    # Conecta com a API do Twitter
    auth = OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Stream que receber os tweets
    twitter_stream = Stream(auth, TweetsListener(connection))
    # Filtra somente por mensagens com hashtags
    twitter_stream.filter(track=['#'])

if __name__ == '__main__':
    s = socket.socket()
    host = 'localhost'
    port = 7777
    s.bind((host, port))

    print('Listening on port: {}'.format(port))

    s.listen(5)

    connection, client_address = s.accept()

    print('Received request from: {}'.format(client_address))

    connect_to_twitter(connection)