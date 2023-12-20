from flask import Flask, request, render_template
import subprocess
import re
app = Flask(__name__)

def remove_ansi_color_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

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

@app.route('/execute_command', methods=['POST'])
def execute_command():
    if request.method == 'POST':
        command = request.form['command']
        if command.strip() == 'lynis audit system':
            try:
                result = subprocess.check_output(command, shell=True, text=True)
                resultat = remove_ansi_color_codes(result)
                # Utiliser Markup pour conserver la mise en forme HTML
                return "<pre>{}</pre>".format(resultat)
            except Exception as e:
                return str(e)
        else:
            return "Commande non autorisée."

if __name__=='__main__':
    app.run()