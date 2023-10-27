from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Replace with your Spotify API credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Initialize Spotipy client
sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Set a secret key for session management
app.secret_key = os.urandom(24)

# ... (Other routes and code)

@app.route('/<name>/overview', methods=['GET', 'POST'])
def overview(name):
    submissions_file = 'json/' + name  + '.json'
    events = []
    with open('events.json', 'r') as f:
        for line in f:
            event = json.loads(line)
            events.append(event)
    
    for event in events:
        if event['url'] == name:
            background_color = event['background_color']
            rname = event['name']
            vs = event['veranstalter']
            url = event['url']
            break
    event_exists = False
    for event in events:
        if event['url'] == name:
            event_exists = True
            break
    if not event_exists:
        return "Event not found"
    PASSWORD = event['password']
    pasw = name + "_password"
    if pasw not in session:
        return redirect("/" + name + "/login")
    if session[pasw] != PASSWORD:
        session.pop(pasw, None)
        return redirect("/" + name + "/login")

    # Read the submitted wishes from the JSON file
    wishes = []
    with open(submissions_file, 'r') as f:
        for line in f:
            wish = json.loads(line)
            wishes.append(wish)

    for wish in wishes:
        track_id = wish['selected_song']
        try:
            track_info = sp.track(track_id)
            wish['song_name'] = track_info['name']
            wish['artist_name'] = track_info['artists'][0]['name']
            if len(track_info['artists']) > 1:
                for i in range(2):
                    wish['artist_name'] += ", " + track_info['artists'][i]['name']
            wish['spotify_url'] = track_info['external_urls']['spotify']
            wish['thumbnail_url'] = track_info['album']['images'][0]['url']
        except Exception as e:
            # Handle errors (e.g., track not found)
            print(f"Error fetching track information: {str(e)}")

    # only show wishes without an status
    wishes = [w for w in wishes if 'status' not in w]
    #reverse the list to show the newest first
    wishes = wishes[::-1]

    # Handle wish deletion
    if request.method == 'POST':
        type = request.form.get('type')
        if type == "delete":
            wish_id_to_delete = request.form.get('delete')
            if wish_id_to_delete is not None:
                # Delete the wish from the list
                wishes = [w for w in wishes if w['selected_song'] == wish_id_to_delete]
                # set an deleted variable to true in the json file
                with open(submissions_file, 'r') as f:
                    lines = f.readlines()
                with open(submissions_file, 'w') as f:
                    for line in lines:
                        wish = json.loads(line)
                        if wish['selected_song'] == wish_id_to_delete:
                            wish['status'] = "deleted"
                        json.dump(wish, f)
                        f.write('\n')
        elif type == "played":
            wish_id_to_played = request.form.get('played')
            if wish_id_to_played is not None:
                # Delete the wish from the list
                wishes = [w for w in wishes if w['selected_song'] == wish_id_to_played]
                # set an deleted variable to true in the json file
                with open(submissions_file, 'r') as f:
                    lines = f.readlines()
                with open(submissions_file, 'w') as f:
                    for line in lines:
                        wish = json.loads(line)
                        if wish['selected_song'] == wish_id_to_played:
                            wish['status'] = "played"
                        json.dump(wish, f)
                        f.write('\n')
        return redirect(url_for('overview', name=name))
    
    return render_template('overview.html', wishes=wishes, name=rname, background_color=background_color, vs=vs, url=url)

@app.route('/<name>/overview/played')
def overviewplayed(name):
    submissions_file = 'json/' + name  + '.json'
    events = []
    with open('events.json', 'r') as f:
        for line in f:
            event = json.loads(line)
            events.append(event)
    event_exists = False
    for event in events:
        if event['url'] == name:
            event_exists = True
            break
    if not event_exists:
        return "Event not found"
    PASSWORD = event['password']
    pasw = name + "_password"
    if pasw not in session or session[pasw] != PASSWORD:
        return redirect("/" + name + "/login")

    # Read the submitted wishes from the JSON file
    wishes = []
    with open(submissions_file, 'r') as f:
        for line in f:
            wish = json.loads(line)
            wishes.append(wish)

    for wish in wishes:
        track_id = wish['selected_song']
        try:
            track_info = sp.track(track_id)
            wish['song_name'] = track_info['name']
            wish['artist_name'] = track_info['artists'][0]['name']
            wish['spotify_url'] = track_info['external_urls']['spotify']
            wish['thumbnail_url'] = track_info['album']['images'][0]['url']
        except Exception as e:
            # Handle errors (e.g., track not found)
            print(f"Error fetching track information: {str(e)}")

    # only show wishes without status played
    wishes = [w for w in wishes if 'status' in w and w['status'] == "played"]
    #reverse the list to show the newest first
    wishes = wishes[::-1]

    for event in events:
        if event['url'] == name:
            background_color = event['background_color']
            rname = event['name']
            vs = event['veranstalter']
            url = event['url']
            break
    return render_template('overview2.html', wishes=wishes, name=rname, background_color=background_color, vs=vs, url=url, type="Gespielte")

@app.route('/<name>/overview/deleted')
def overviewdeleted(name):
    submissions_file = 'json/' + name  + '.json'
    events = []
    with open('events.json', 'r') as f:
        for line in f:
            event = json.loads(line)
            events.append(event)
    event_exists = False
    for event in events:
        if event['url'] == name:
            event_exists = True
            break
    if not event_exists:
        return "Event not found"

    PASSWORD = event['password']
    pasw = name + "_password"
    if pasw not in session or session[pasw] != PASSWORD:
        return redirect("/" + name + "/login")

    # Read the submitted wishes from the JSON file
    wishes = []
    with open(submissions_file, 'r') as f:
        for line in f:
            wish = json.loads(line)
            wishes.append(wish)

    for wish in wishes:
        track_id = wish['selected_song']
        try:
            track_info = sp.track(track_id)
            wish['song_name'] = track_info['name']
            wish['artist_name'] = track_info['artists'][0]['name']
            wish['spotify_url'] = track_info['external_urls']['spotify']
            wish['thumbnail_url'] = track_info['album']['images'][0]['url']
        except Exception as e:
            # Handle errors (e.g., track not found)
            print(f"Error fetching track information: {str(e)}")

    # only show wishes without status played
    wishes = [w for w in wishes if 'status' in w and w['status'] == "deleted"]
    #reverse the list to show the newest first
    wishes = wishes[::-1]

    for event in events:
        if event['url'] == name:
            background_color = event['background_color']
            rname = event['name']
            vs = event['veranstalter']
            url = event['url']
            break
    return render_template('overview2.html', wishes=wishes, name=rname, background_color=background_color, vs=vs, url=url, type="Gelöschte")

@app.route('/<name>/login', methods=['GET', 'POST'])
def login(name):
    events = []
    with open('events.json', 'r') as f:
        for line in f:
            event = json.loads(line)
            events.append(event)
    for event in events:
        if event['url'] == name:
            background_color = event['background_color']
            rname = event['name']
            vs = event['veranstalter']
            vsurl = event['url']
            break
    event_exists = False
    for event in events:
        if event['url'] == name:
            event_exists = True
            break
    if not event_exists:
        return "Event not found"
    PASSWORD = event['password']

    if request.method == 'POST':
        password_attempt = request.form.get('password')
        # set the password to the one defined in the event.json file
        pasw = name + "_password"
        if password_attempt == PASSWORD:
            session[pasw] = PASSWORD
            return redirect("/" + name + "/overview")
        else:
            return render_template('login.html', vs = vs, rname=rname, background_color=background_color, vsurl=vsurl, error=True)
    else:
        pasw = name + "_password"
        if pasw in session and session[pasw] == PASSWORD:
            return redirect("/" + name + "/overview")
        else:
            return render_template('login.html', vs = vs, rname=rname, background_color=background_color, vsurl=vsurl, error=False)

@app.route('/<name>/logout')
def logout(name):
    pasw = name + "_password"
    session.pop(pasw, None)
    return redirect("/" + name + "/login")


@app.route('/<name>', methods=['GET', 'POST'])
def index(name):
    #check in the events.json file if the event exists
    events = []
    with open('events.json', 'r') as f:
        for line in f:
            event = json.loads(line)
            events.append(event)
    event_exists = False
    for event in events:
        if event['url'] == name:
            event_exists = True
            break
    if not event_exists:
        return "Event not found"
    submissions_file = 'json/' + name  + '.json'
    if request.method == 'POST':
        name = request.form['name']
        selected_song = request.form['selected_song']
        message = request.form['message']

        submission = {
            'name': name,
            'selected_song': selected_song,
            'message': message,
        }

        # Save the submission to a JSON file
        with open(submissions_file, 'a') as f:
            json.dump(submission, f)
            f.write('\n')

        return redirect(url_for('submitted', name=event['url']))

    #return the index with the background_color variable from the events.json file
    for event in events:
        if event['url'] == name:
            background_color = event['background_color']
            rname = event['name']
            vs = event['veranstalter']
            break
    return render_template('index.html', background_color=background_color, name=name, rname=rname, vs=vs)

@app.route('/search_song', methods=['POST'])
def search_song():
    query = request.form['query']
    if query:
        results = sp.search(q=query, type='track', limit=10)
        tracks = results['tracks']['items']
        # Add image URL to each track
        for track in tracks:
            if len(track['album']['images']) > 0:
                track['image_url'] = track['album']['images'][0]['url']
            else:
                track['image_url'] = None
    else:
        tracks = []
    return jsonify(tracks)

@app.route('/<name>/submitted')
def submitted(name):
    events = []
    with open('events.json', 'r') as f:
        for line in f:
            event = json.loads(line)
            events.append(event)
        
    for event in events:
        if event['url'] == name:
            background_color = event['background_color']
            rname = event['name']
            vs = event['veranstalter']
            vsurl = event['url']
            break
    return render_template('submitted.html', vs = vs, rname=rname, background_color=background_color, vsurl=vsurl)

@app.route('/media/<file>')
def media(file):
    return send_file("./media/" + file)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')