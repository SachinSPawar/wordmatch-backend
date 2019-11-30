from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_restful import reqparse
import checkword
from flask_cors import CORS, cross_origin
from flask import request

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)

from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
chars=""
words=[]

@app.route('/word/validate', methods=['GET'])
def validateWord():
    word = request.args.get('word')
    global chars
    global words
    print "word : "+word
    print "chars :"+chars
    isValid=checkword.checkword(word,chars)
    if isValid and not word in words:
        words.append(word)
    return {'result': isValid}

@app.route('/word/new', methods=['GET'])
def getRandomLetters():
    global chars
    global words
    chars=checkword.getRandomLetters(6)
    words=[]
    return {    
                'words':words,
                'characters':chars,
                'score':checkword.calculateScore(words,chars)
            }

@app.route('/word/state', methods=['GET'])
def getGameState():
    global chars
    global words
    return {
                'words':words,
                'characters':chars,
                'score':checkword.calculateScore(words,chars)
            }

@app.route('/word/end', methods=['GET'])
def gameOver():
    global chars
    global words
    score=checkword.calculateScore(words,chars)
    return{
            'words':words,
            'characters':chars,
            'score':checkword.calculateScore(words,chars)
        }

@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

if __name__ == '__main__':
    app.run(debug=True)