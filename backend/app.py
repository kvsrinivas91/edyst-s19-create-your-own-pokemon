from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import os
import json

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initializing db
db=SQLAlchemy(app)

#Class for pokemon
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)# key increases automatically
    name = db.Column(db.String(40),unique=True,nullable=False)
    sprite = db.Column(db.String(150),nullable=False)
    fg = db.Column(db.String(20),nullable=False)
    bg = db.Column(db.String(20),nullable=False)
    desc = db.Column(db.String(20),nullable=False)

    def __init__(self,name,sprite,fg,bg,desc):
        self.name=name
        self.sprite=sprite
        self.fg=fg
        self.bg=bg
        self.desc=desc

#Handling Error 404
@app.errorhandler(404)  
def page_not_found(error=None):
  return ('Error 404'), 404

@app.errorhandler(500)
def page_not_found_500(e):
    return render_template('404.html'), 404

#Create a pokemon
@app.route('/api/pokemon', methods=['POST'])
def pokemon_post():
    #Getting the json data
    pokemon=request.json['pokemon']
    name=pokemon['name']
    if  len(name)>40 or len(name)<1: #Validating name
        return("Enter proper name of lenght between 1 and 40 charecters")
    sprite=pokemon['sprite']
    if  len(sprite)>150 or len(sprite)<1: #Validating sprite name
        return("Enter proper sprite name of lenght between 1 and 150 charecters")
    fg=pokemon['cardColours']['fg']
    bg=pokemon['cardColours']['bg']
    desc=pokemon['cardColours']['desc']
    new_pokemon=Pokemon(name,sprite,fg,bg,desc)#Data passed from Postman

    db.session.add(new_pokemon)
    db.session.commit()

    pokemon=Pokemon.query.filter(Pokemon.name==name).first()
    new_pokemon={'pokemon' : {'id' : pokemon.id, 'name' : pokemon.name, 'sprite' : pokemon.sprite, 'cardColours' : {'fg' : pokemon.fg, 'bg' : pokemon.bg, 'desc' : pokemon.desc}}}
    return jsonify(new_pokemon)
        
#Getting Pokemon Deatails
@app.route('/api/pokemon/<int:id>', methods=['GET'])
def pokemon_get(id):
    if id<=0:
        return("Enter proper Pokemon id")
    pokemon=Pokemon.query.get(id)

    if pokemon!=None:
        pokemon_details={'pokemon':{'id':pokemon.id,'name':pokemon.name,'sprite':pokemon.sprite,'cardColours':{'fg':pokemon.fg,'bg':pokemon.bg,'desc':pokemon.desc}}}
        return jsonify(pokemon_details)
    else:
        return("Pokeomon not found")

#Update the product
@app.route('/api/pokemon/<int:id>', methods=['PATCH'])
def pokemon_patch(id):
    
    pokemondb=Pokemon.query.get(id)
    if pokemondb==None:
        return("Pokemon not found")
    pokemon=request.json['pokemon']

    if 'name' in pokemon:
        if  len(pokemon['name'])>40 or len(pokemon['name'])<1: #Validating name
            return("Enter proper name of lenght between 1 and 40 charecters")
        else:
            pokemondb.name=pokemon['name']

    if 'sprite' in pokemon:        
        if  len(pokemon['sprite'])>150 or len(pokemon['sprite'])<1: #Validating sprite name
            return("Enter proper sprite name of lenght between 1 and 150 charecters")
        else:    
            pokemondb.sprite=pokemon['sprite']

    if 'cardColours' in pokemon:        
        carColours1=pokemon['cardColours']
        if 'fg' in carColours1:
            pokemondb.fg=pokemon['cardColours']['fg']
        if 'bg' in carColours1:
            pokemondb.bg=pokemon['cardColours']['bg']
        if 'desc' in carColours1:    
            pokemondb.desc=pokemon['cardColours']['desc']
    
    db.session.commit()

    pokemondb=Pokemon.query.filter(Pokemon.id==id).first()
    new_pokemon={'pokemon' : {'id' : pokemondb.id, 'name' : pokemondb.name, 'sprite' : pokemondb.sprite, 'cardColours' : {'fg' : pokemondb.fg, 'bg' : pokemondb.bg, 'desc' : pokemondb.desc}}}
    return jsonify(new_pokemon)

#deleting pokemon data
@app.route('/api/pokemon/<int:id>', methods=['DELETE'])
def pokemon_delete(id):
    if id<=0:
        return("Enter proper Pokemon id")
    pokemon=Pokemon.query.get(id)

    if pokemon!=None:
        pokemon_details={'pokemon':{'id':pokemon.id,'name':pokemon.name,'sprite':pokemon.sprite,'cardColours':{'fg':pokemon.fg,'bg':pokemon.bg,'desc':pokemon.desc}}}
        db.session.delete(pokemon)
        db.session.commit()
        return jsonify(pokemon_details)
    else:
        return("Enter correct pokemon id")

#Run Server
if __name__ == '__main__':
    db.create_all()
    app.run(host='localhost',debug=True,port=8006)

    