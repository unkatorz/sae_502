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


@app.route('/execute_ssh_command', methods=['POST'])
def execute_ssh_command():
    if request.method == 'POST':
        command = request.form['command']
        hostname = '192.168.187.128'  # Remplacez par l'adresse de votre machine distante
        username = 'root'        # Remplacez par votre nom d'utilisateur SSH
        password = 'bonjour'       # Remplacez par votre mot de passe SSH (ou utilisez une méthode plus sécurisée)

        try:
            import paramiko

            # Établir la connexion SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=username, password=password)

            # Exécuter la commande
            stdin, stdout, stderr = ssh.exec_command(command)

            # Lire la sortie de la commande
            resultat = stdout.read().decode('utf-8')

            # Fermer la connexion SSH
            ssh.close()
            resultat = remove_ansi_color_codes(resultat)
            return "<pre>{}</pre>".format(resultat)

        except Exception as e:
            return f"Erreur lors de l'exécution de la commande : {str(e)}"

if __name__=='__main__':
    app.run()