from flask import Flask, render_template, request

import json
import sys

app = Flask(__name__)
developer_db = json.load(open('resources/sponsors.json', 'r'))
sponsors_db = json.load(open('resources/sponsorees.json', 'r'))
ams_db = json.load(open('resources/ams.json', 'r'))
active_db = json.load(open('resources/active.json', 'r'))

def traverse(developer, tree):
    ret = {}
    active = {}
    try:
        active[developer] = active_db[developer]
        ret[developer] = tree[developer]
        for entity in tree[developer]:

            r, a = traverse(entity, tree)
            ret.update(r)
            active.update(a)
    except KeyError:
        pass
    for dev in ret:
        active[dev] = active_db[dev]
    return ret, active

def get_sponsor_tree(developer):
    return traverse(developer, developer_db)

def get_sponsorees_tree(developer):
    return traverse(developer, sponsors_db)

def get_ams_tree(developer):
    return traverse(developer, ams_db)

def get_nodes(developer):
    active = {}
    sponsors, aSpon = get_sponsor_tree(developer)
    active.update(aSpon)
    sponsorees, aSpon = get_sponsorees_tree(developer)
    active.update(aSpon)
    ams, aAM = get_ams_tree(developer)
    active.update(aAM)
    return ( sponsors, sponsorees, ams, active )

@app.route("/")
def index():
    return render_template('index.html', **{})

@app.route("/view/<username>")
def view(username):
    return render_template('view.html', **{
        "person": username
    })

@app.route("/user/<username>/endpoint.json")
def user(username):
    sponsors, sponsorees, ams, active = get_nodes(username)
    return json.dumps({
        "advocates": sponsors,
        "advocated": sponsorees,
        "am": ams,
        "active": active
    })

if __name__ == "__main__":
    app.run(debug=True)
