from flask import Flask
import json
from flask_httpauth import HTTPDigestAuth
from flask import request, jsonify
app = Flask(__name__)
app.config['SECRET_KEY'] = "vikash"
auth = HTTPDigestAuth()
users = {
"vikash": "vikash",
"admin" : "admin"
}
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

    

@app.route('/', methods=['HEAD'])
@auth.login_required
def home():
    return "done",200


@app.route('/', methods=['GET'])
@auth.login_required
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
@auth.login_required
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
        if 'id' in request.args:
            id = int(request.args['id'])
        else:
            return "Error: No id field provided. Please specify an id."

        # Create an empty list for our results
        results = []

        # Loop through the data and match results that fit the requested ID.
        # IDs are unique, but other fields might return many results
        for book in books:
            if book['id'] == id:
                results.append(book)

        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
        return jsonify(results)

max_id = 3


@app.route("/post", methods=["POST"])
@auth.login_required
def post_id():
        if request.method == "POST":
            new_id= books[len(books)-1]['id']+1
            req_Data = request.data
            data=json.loads(req_Data)
            title = data['title']
            author = data['author']
            new_book = {"id": new_id, "title": title, "author": author, "first_sentence": "Who cares?", "published": 1994}
            books.append(new_book)
            return new_book, 201


@app.route("/put", methods=["PUT"])
@auth.login_required
def put_id():
    #if request.authorization and request.authorization.username == 'vikash' and request.authorization.password == 'vikash':
        if request.method == "PUT":
            new_id= books[len(books)-1]['id']+1
            title = request.args.get('title')
            author = request.args.get('author')
            new_book = {"id": new_id, "title": title, "author": author, "first_sentence": "Who cares?", "published": 1994}
            books.append(new_book)
            return new_book, 201


@app.route("/delete", methods=["DELETE"])
@auth.login_required
def delete():
    #if request.authorization and request.authorization.username == 'vikash' and request.authorization.password == 'vikash':
        return '''<h1>Distant Reading Archive</h1>
        <p>An example for deleting</p>'''


if __name__ == '__main__':
    app.run(host='9mxlhm2', port=3001, debug=True)


