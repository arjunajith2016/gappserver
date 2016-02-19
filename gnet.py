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
        "c1" : url_for('static', filename='c1.png'),
        "c2" : url_for('static', filename='c2.png'),
        "c3" : url_for('static', filename='c3.png'),
        "c4" : url_for('static', filename='c4.png'),
        "c5" : url_for('static', filename='c5.png'),
        "c6" : url_for('static', filename='c6.png'),
        "c7" : url_for('static', filename='c7.png'),
        "c8" : url_for('static', filename='c8.png'),
        "c9" : url_for('static', filename='c9.png'),
        "c10" : url_for('static', filename='c10.png')
    }
    return jsonify({'result' : data})

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