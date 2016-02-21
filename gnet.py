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
        "gridWidget" : {
            "c1" : url_for('static', filename='c7.png'),
            "c2" : url_for('static', filename='c8.png'),
            "c3" : url_for('static', filename='c3.png'),
            "c4" : url_for('static', filename='c10.png'),
            "c5" : url_for('static', filename='c5.png'),
            "c6" : url_for('static', filename='c12.png'),
            "c7" : url_for('static', filename='c11.png'),
            "c8" : url_for('static', filename='c9.png'),
            "c9" : url_for('static', filename='c17.png'),
            "c10" : url_for('static', filename='c16.png'),
            "c11" : url_for('static', filename='c15.png'),
            "c12" : url_for('static', filename='c14.png'),
            "gridTitle" : "All Categories"
        },

        "announcerWidget" : {
            "image1" : url_for('static', filename='p7.png'),
            "text1" : "Fan Of Cakes?",
            "subText1" : "Get 30% off on cakes : CAKE30",

            "image2" : url_for('static', filename='p5.png'),
            "text2" : "Cops Love Donuts",
            "subText2" : "You will too! Get 10% off on first order.",

            "image3" : url_for('static', filename='sweets7.png'),
            "text3" : "More Cakes!",
            "subText3" : "We have every kind you can imagine.",

            "image4" : url_for('static', filename='honeycomb.png'),
            "text4" : "The Best Of Nature",
            "subText4" : "Now at your doorstep!",

            "image5" : url_for('static', filename='p9.png'),
            "text5" : "I Don't Know",
            "subText5" : "What these are. But they look tasty!"
        }
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