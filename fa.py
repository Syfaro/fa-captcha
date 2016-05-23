from flask import Flask, request, render_template, session, redirect, make_response, jsonify
from pprint import pprint
import requests
import uuid

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a_secret_key'

request_sessions = {}
request_cookies = {}


@app.route('/')
def home():
	if 'uuid' not in session:
		session['uuid'] = uuid.uuid1()

	request_sessions[session['uuid']] = requests.session()
	r = request_sessions[session['uuid']].get('https://www.furaffinity.net/login/')

	request_cookies[session['uuid']] = r.cookies['b']

	return render_template('homepage.html')


@app.route('/captcha')
def captcha():
	if 'uuid' not in session:
		return redirect('/')

	r = request_sessions[session['uuid']].get('https://www.furaffinity.net/captcha.jpg')
	resp = make_response(r.content)
	resp.headers['Content-type'] = 'image/jpeg'

	return resp


@app.route('/login', methods=['POST'])
def login():
	if 'uuid' not in session:
		return redirect('/')

    values = {
    	'action': 'login',
    	'name': request.form['username'],
    	'pass': request.form['password'],
    	'captcha': request.form['captcha']
    }

    r = request_sessions[session['uuid']].post('https://www.furaffinity.net/login/', data=values, allow_redirects=False)

    return jsonify({
    	'a': r.cookies['a'],
    	'b': request_cookies[session['uuid']]
    })

if __name__ == '__main__':
	app.run(debug=True)
