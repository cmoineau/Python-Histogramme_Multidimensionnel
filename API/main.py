# -*- coding: UTF-8 -*-
import sys
sys.path.append('../')
from API import wrapper
from flask import Flask, jsonify, request

app = Flask(__name__)

wrapper = wrapper.Histogramme_wrapper()


@app.route('/creer/STHoles/', methods=['POST'])
def creer_stholes():
    """
    Exemple de requête :
    curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/creer/stholes/ --data '{"nom_attributs":["x"], "nom_histogramme":"toto"}'
    :return:
    """
    # récupère sous la forme d'un json les paramètres.
    payload = request.get_json()
    try:
        attributes_name = payload['nom_attributs']
        path = payload['nom_histogramme']
    except Exception as e:
        return jsonify(status='False', message="Vous devez spécifier le nom des attributs et le nom de l'histogramme")
    result = wrapper.creer_STHoles(attributes_name, path)
    if result:
        return jsonify(status='True', message='Histogramme crée avc succès !')
    return jsonify(status='False', message="Erreur lors de la création de l'histogramme ...")


@app.route('/creer/mhist/', methods=['POST'])
def creer_mhist():
    """
    Exemple de requête :
    curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/creer/mhist/ --data '{"nom_attributs":["x"], "nom_histogramme":"toto", "donnee": [[1, 2, 3, 4, 5, 6 ,1]]}'
    :return:
    """
    # récupère sous la forme d'un json les paramètres.
    payload = request.get_json()
    print(payload)
    try:
        attributes_name = payload['nom_attributs']
        path = payload['nom_histogramme']
        data = payload['donnee']
    except Exception as e:
        return jsonify(status='False', message="Vous devez spécifier le nom des attributs et le nom de l'histogramme")
    print('test')
    result = wrapper.creer_MHIST(data, attributes_name, path)
    if result:
        print("hi")
        return jsonify(status='True', message='Histogramme crée avec succès !')
    return jsonify(status='False', message="Erreur lors de la création de l'histogramme ...")


@app.route('/creer/genhist/', methods=['POST'])
def creer_genhist():
    """
    Exemple de requête :
    curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/creer/genhist/ --data '{"nom_attributs":["x"], "nom_histogramme":"toto", "donnee": [[1, 2, 3, 4, 5, 6 ,1]]}'
    :return:
    """
    # récupère sous la forme d'un json les paramètres.
    payload = request.get_json()
    try:
        attributes_name = payload['nom_attributs']
        path = payload['nom_histogramme']
        data = payload['donnee']
    except Exception as e:
        return jsonify(status='False', message="Vous devez spécifier le nom des attributs et le nom de l'histogramme")
    result = wrapper.creer_GENHIST(data, attributes_name, path)
    if result:
        return jsonify(status='True', message='Histogramme crée avec succès !')
    return jsonify(status='False', message="Erreur lors de la création de l'histogramme ...")


# J'aurais aimé utiliser GET mais je n'ai pas trouver comment avoir un payload avec GET
@app.route('/<nom_histogramme>/estimer', methods=['POST'])
def estimer(nom_histogramme=None):
    """
    Exemple de requête :
    curl -X POST -H 'Content-Type: application/json' -i 'http://localhost:5000/test.genhist/estimer' --data '{"nom_attributs": ["x"], "zone":[[-1, 1]]}'
    :param nom_histogramme:
    :return:
    """

    payload = request.json
    print(payload)
    path = "./saved_hist/" + nom_histogramme

    try:
        attributes_name = payload['nom_attributs']
        zone = payload["zone"]

    except Exception as e:
        return jsonify(status='False', message="Vous devez spécifier le nom des attributs et le nom de l'histogramme")

    try:
        wrapper.charger_histogramme(path)
    except Exception as e:
        return jsonify(status='False', message="Impossible de trouver l'histogramme\n")
    result = wrapper.estimer(attributes_name, zone)
    return jsonify(status='True', resultat=result, message='Estimation réalisée avec succès !')


@app.route('/<nom_histogramme>', methods=['DELETE'])
def supprimer(nom_histogramme=None):
    print(nom_histogramme)
    path = "./saved_hist/" + nom_histogramme
    if wrapper.remove_hist(path):
        return jsonify(status='True')
    else:
        return jsonify(status='False', message="Impossible de supprimer l'histogramme :" + nom_histogramme)


@app.route('/lister', methods=['GET'])
def lister():
    list_histogramme = [path.split('/')[-1] for path in wrapper.list_hist()]
    return jsonify(status='True', resultat=list_histogramme)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
