import pusher
from flask import render_template, jsonify, request, Blueprint,redirect
import json
import sys
import spotipy
import spotipy.util as util

pusher_client = pusher.Pusher(
  app_id='541241',
  key='d199b9ff7984c46c4f83',
  secret='e0d579e55a6e83dd7397',
  cluster='us2',
  ssl=True
)
username = '12158815080'
playlist_id = '4eEdWa9SqJIIvJd4HpTl1Y'
scope = 'playlist-modify-public playlist-modify-private user-read-playback-state user-read-currently-playing user-modify-playback-state'
redirect = 'http://albertcastaned.pythonanywhere.com/callback/q'
main = Blueprint('main', __name__)


@main.route("/home")
def home():
    return render_template('home.html', title='Home')



@main.route("/about")
def about():
    return render_template('about.html', title='About')


index_add_counter = 0
@main.route("/callback/q")
def callback():
    return render_template('playlist.html')


@main.route("/playlist")
def playlist():
    token = util.prompt_for_user_token(username, scope, redirect_uri=redirect)
    if token:
        print(token)
    else:
        print("Can't get token for", username)
    return render_template('playlist.html',token=token,title='Playlist')


def skip_song():
    token = util.prompt_for_user_token(username, scope, redirect_uri=redirect)
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        sp.next_track()
    else:
        print("Can't get token for", username)


@main.route('/vote', methods=['POST'])
def vote():
    try:
        print("method accessed")
        global index_add_counter # means: in this scope, use the global name
        index_add_counter+=1
        print(index_add_counter)
        if index_add_counter == 3:
            skip_song()
            index_add_counter=0
        pusher_client.trigger('chatchannel', 'update-count', {'count':index_add_counter})
        return jsonify({'result' : 'success'})
    except:
        print('ERROR')
        return jsonify({'result' : 'failure'})


@main.route("/get-vote",methods=['POST'])
def get_vote():
    try:
        #Test
        global index_add_counter # means: in this scope, use the global name
        pusher_client.trigger('chatchannel', 'update-count', {'count':index_add_counter})
        return jsonify({'result' : 'success'})
    except:
        print('ERROR')
        return jsonify({'result' : 'failure'})