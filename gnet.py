# all the imports
import os
import datetime
from flask import Flask, jsonify, request, session, redirect, url_for, render_template, flash, send_from_directory, abort, make_response
from flask.ext.triangle import Triangle

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
Triangle(app)
app.config.from_object(__name__)

# setting up views

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getalljson')
def getalljson():
    data = {
        "gridWidget" : 
            [{"image" : url_for('static', filename='c7.png')},
            {"image" : url_for('static', filename='c8.png')},
            {"image" : url_for('static', filename='c3.png')},
            {"image" : url_for('static', filename='c10.png')},
            {"image" : url_for('static', filename='c5.png')},
            {"image" : url_for('static', filename='c12.png')},
            {"image" : url_for('static', filename='c11.png')},
            {"image" : url_for('static', filename='c9.png')},
            {"image" : url_for('static', filename='c17.png')},
            {"image" : url_for('static', filename='c16.png')},
            {"image" : url_for('static', filename='c15.png')},
            {"image" : url_for('static', filename='c14.png')}],

        "gridTitle" : "All Categories",

        "announcerWidget" : [{
            "image" : url_for('static', filename='p7.jpg'),
            "text" : "Fan Of Cakes?",
            "subText" : "Get 30% off on cakes : CAKE30"},

            {"image" : url_for('static', filename='p5.jpg'),
            "text" : "Cops Love Donuts",
            "subText" : "You will too! Get 10% off on first order."},

            {"image" : url_for('static', filename='sweets7.jpg'),
            "text" : "More Cakes!",
            "subText" : "We have every kind you can imagine."},

            {"image" : url_for('static', filename='honeycomb.jpg'),
            "text" : "The Best Of Nature",
            "subText" : "Now at your doorstep!"},

            {"image" : url_for('static', filename='p9.jpg'),
            "text" : "I Don't Know",
            "subText" : "What these are. But they look tasty!"
        }],

        "pagerWidget" : [
            {"image" : url_for('static', filename='marshmallow.jpg'),
            "text" : "Marshmallow"},

            {"image" : url_for('static', filename='lollipop.jpg'),
            "text" : "Lollipop"},

            {"image" : url_for('static', filename='kitkat.jpg'),
            "text" : "Kitkat"},

            {"image" : url_for('static', filename='jellybean.jpg'),
            "text" : "Jellybean"},

            {"image" : url_for('static', filename='ics.jpg'),
            "text" : "Ice Cream Sandwich"},

            {"image" : url_for('static', filename='honeycomb.jpg'),
            "text" : "Honeycomb"},

            {"image" : url_for('static', filename='gingerbread.jpg'),
            "text" : "Gingerbread"},

            {"image" : url_for('static', filename='froyo.jpg'),
            "text" : "Froyo"},

            {"image" : url_for('static', filename='eclair.jpg'),
            "text" : "Eclair"},

            {"image" : url_for('static', filename='donut.jpg'),
            "text" : "Donut"},

            {"image" : url_for('static', filename='cupcake.jpg'),
            "text" : "Cupcake"},

            {"image" : url_for('static', filename='brownie.jpg'),
            "text" : "Brownie"},

            {"image" : url_for('static', filename='angelcake.jpg'),
            "text" : "Angel Cake"}
        ]
    }
    return jsonify(data)

@app.route('/add', methods=['POST'])
def add_entry():
    t=datetime.datetime.now()
    current_date=str(getattr(t,'day'))+'-'+str(getattr(t,'month'))+'-'+str(getattr(t,'year'))
    if getattr(t,'hour') < 12:
        current_time=str(getattr(t,'hour'))+':'+str(getattr(t,'minute'))+' AM'
    elif getattr(t,'hour') == 12:
        current_time=str(getattr(t,'hour'))+':'+str(getattr(t,'minute'))+' PM'
    elif getattr(t,'hour') > 12:
        current_time=str(getattr(t,'hour')-12)+':'+str(getattr(t,'minute'))+' PM'

    if not session.get('logged_in'):
        abort(401)
    if not request.json or not 'title' in request.json:
        abort(400)
    else:
        g.db.execute('insert into entries (title, text, date, time, user) values (?, ?, ?, ?, ?)', [request.json['title'], request.json['text'], current_date, current_time, session['user']])
        g.db.commit()
        flash('New entry was successfully posted')
    return redirect(url_for('home'))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 404, 'message' : 'Not found'}), 404)

# to start the server
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)