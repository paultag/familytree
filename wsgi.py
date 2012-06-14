from flask import Flask, render_template, request

import json
import sys

app = Flask(__name__)
developer_db = json.load(open('resources/sponsors.json', 'r'))
sponsors_db = json.load(open('resources/sponsorees.json', 'r'))

def traverse(developer, tree):
    ret = {}
    try:
        ret[developer] = tree[developer]
        for entity in tree[developer]:
            ret.update(traverse(entity, tree))
    except KeyError:
        pass
    return ret

def get_sponsor_tree(developer):
    return traverse(developer, developer_db)

def get_sponsorees_tree(developer):
    return traverse(developer, sponsors_db)

def get_nodes(developer):
    sponsors = get_sponsor_tree(developer)
    sponsorees = get_sponsorees_tree(developer)
    return ( sponsors, sponsorees )

@app.route("/")
def index():
    return render_template('index.html', **{})

@app.route("/user/<username>/endpoint.json")
def user(username):
    try:
        sponsors, sponsorees = get_nodes(username)
    except KeyError as e:
        return "KeyError " + str(e)
    return json.dumps({
        "advocates": sponsors,
        "advocated": sponsorees
    })

if __name__ == "__main__":
    app.run()
