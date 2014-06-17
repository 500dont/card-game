from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
   return 'index'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name="Unknown user"):
	return render_template('dom-html.html', name = name)

if __name__ == '__main__':
   app.debug = True
   app.run()