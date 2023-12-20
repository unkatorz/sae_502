from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ui')
def ui():
    return render_template('ui.html')

@app.route('/audit')
def audit():
    return render_template('audit.html')

@app.route('/ssl')
def ssl():
    return render_template('ssl.html')

if __name__=='__main__':
    app.run()