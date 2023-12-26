from flask import Flask, request, render_template, send_from_directory
import subprocess
import os
import re
import psutil  # Ajout de psutil ici
import paramiko

app = Flask(__name__)

def remove_ansi_color_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/images/<path:filename>')
def get_image(filename):
    images_dir = os.path.join(os.getcwd(), 'images')
    return send_from_directory(images_dir, filename)

@app.route('/ui')
def ui():
    # Informations sur le CPU
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_cores = len(cpu_percent)

    # Informations sur la mémoire
    memory_stats = psutil.virtual_memory()

    # Informations sur le réseau
    network_stats = psutil.net_io_counters()

    # Informations sur le stockage
    disk_usage = psutil.disk_usage('/')

    # Transmettez ces informations au modèle HTML
    return render_template('ui.html', cpu_percent=cpu_percent, cpu_cores=cpu_cores,
                           memory_stats=memory_stats, network_stats=network_stats,
                           disk_usage=disk_usage)


@app.route('/application')
def application():
    return render_template('application.html')

@app.route('/a_propos')
def a_propos():
    return render_template('a_propos.html')


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
        hostname = '192.168.187.128'
        username = 'root'
        password = 'bonjour'

        try:
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
    app.run(debug=True)
