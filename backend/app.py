from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import os
import json

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Initializing db
db=SQLAlchemy(app)

#Class for pokemon
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)# key increases automatically
    name = db.Column(db.String(50),unique=True)
    sprite = db.Column(db.String(150))
    cardColours = db.Column(db.String(150))

def __init__(self,name,sprite,cardColours):
    self.name=name
    self.sprite=sprite
    self.cardColours=cardColours



@app.errorhandler(404)  
def page_not_found(error=None):
  return ('Error 404'), 404

@app.errorhandler(500)
def page_not_found_500(e):
    return render_template('404.html'), 404

@app.route('/api/pokemon/', methods=['POST'])
def pokemon_post(id):
    name=request.json['name']        
    sprite=request.json['sprite']
    cardColours=request.json['cardColours']

    new_pokemon = Pokemon(name,sprite,cardColours)

    db.session.add(new_pokemon)
    db.session.commit()

    return jsonify(new_pokemon)
        
#Run Server
if __name__ == '__main__':
    app.run(host='localhost',debug=True,port=8006)

    