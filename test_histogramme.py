# -*- coding: UTF-8 -*-

"""
:author : Cyril MOINEAU
:description : Script pour tester les histogrammes. Potentiellement plus à jour /!\
"""
import json
import MHIST.Mhist as mhist
import GENHIST.Genhist as genhist
import AVI.avi as avi
from STHOLES import Stholes as st
import matplotlib.pyplot as plt
from STHOLES import Workload as w
import time
import utils

# Définition des variables =============================================================================================
nb_tuple = 10000
nb_req_test = 1000


def init_histogramme(data_set):
    t_time = []
    nb_intervalle = 1000
    print("Création des histogrammes")
    t = time.time()
    # MHIST ============================================================================================================
    histo_mhist = mhist.Mhist(data_set[1], data_set[0], nb_intervalle)

    # histo_mhist.print(data_set[0])
    # plt.scatter(data_set[1][0], data_set[1][1], marker='+')
    # plt.show()
    # histo_mhist.save('./histo_mhist')
    t_time.append(time.time()-t)
    print('MHIST initialisé !')

    # GENHIST ==========================================================================================================
    # Variables pour GENHIST :
    b = 50
    xi = 10  # nombre d'intervalle selon une dimension pour les partition régulière de l'espace
             # (Devrait être aux alentours de 100)
    alpha = (1 / 2) ** (1 / len(data_set[1]))
    t = time.time()
    histo_genhist = genhist.Genhist(data_set[1], data_set[0], b, xi, alpha, verbeux=False)
    # histo_genhist.save('./histo_genhist')
    # histo_genhist.print()
    # plt.scatter(data_set[1][0], data_set[1][1], marker='+')
    # plt.show()
    t_time.append(time.time() - t)
    print('GENHIST initialisé !')

    # STHOLES ==========================================================================================================
    nb_requete = 700
    histo_st = st.Stholes(data_set[0], nb_intervalle, verbeux=True)
    t = time.time()
    workload = w.create_workload_full(data_set[1], 0.01, nb_requete)
    # Initialisation en prenant l'ensemble du jeu de donnée
    # histo_st.BuildAndRefine([([[min(a), max(a)] for a in data_set[1]], len(data_set[1][0]))])
    # Raffinement à l'aide de requête généré aléatoirement
    histo_st.BuildAndRefine(workload)
    t_time.append(time.time() - t)
    # histo_st.print(tab_attribut=data_set[1])
    # histo_st.save('./histo_st')
    # AVI ==============================================================================================================
    o_avi = avi.Avi(data_set[1], data_set[0])
    return histo_mhist, histo_genhist, histo_st, o_avi, t_time


def test_data_set(data_set, tab_intervalles_est):
    histo_mhist, histo_genhist, histo_st, o_avi, t_time = init_histogramme(data_set)
    dict_data = {'size': {'MHIST': histo_mhist.get_size(),
                          'GENHIST': histo_genhist.get_size(),
                          'STHOLE': histo_st.get_size()},
                 'time': {'MHIST': t_time[0],
                          'GENHIST': t_time[1],
                          'STHOLE': t_time[2]}}
    cpt_nb_intervalle = 0
    for intervalle in tab_intervalles_est:
        # Initialisation du dictionnaire de résultat
        dic_intervalle = {'attribut': intervalle[0], 'boundary': intervalle[1]}

        # Calcul du nombre réel de tuple ===============================================================================
        res = 0
        t = time.time()
        nb_tuple = len(data_set[1][0])
        for i in range(nb_tuple):
            if utils.est_inclus([att[i] for cpt, att in enumerate(data_set[1]) if (data_set[0][cpt] in intervalle[0])],
                                intervalle[1]):
                res += 1
        dic_intervalle['reel'] = {'resultat': res, 'temps': time.time()-t}

        # Estimation avec MHIST ========================================================================================
        t = time.time()
        res = histo_mhist.estimer(intervalle[0], intervalle[1])
        dic_intervalle['MHIST'] = {'resultat': res, 'temps': time.time() - t}

        # Estimation avec GENHIST ======================================================================================
        t = time.time()
        res = histo_genhist.estimer(intervalle[0], intervalle[1])
        dic_intervalle['GENHIST'] = {'resultat': res, 'temps': time.time() - t}

        # Estimation avec STHOLES ======================================================================================
        t = time.time()
        res = histo_st.estimer(intervalle[0], intervalle[1])
        dic_intervalle['STHOLES'] = {'resultat': res, 'temps': time.time() - t}

        # Estimation avec AVI ==========================================================================================
        t = time.time()
        res = round(o_avi.estimation(intervalle[0], intervalle[1]))
        dic_intervalle['AVI'] = {'resultat': res, 'temps': time.time() - t}

        dict_data[cpt_nb_intervalle] = dic_intervalle
        cpt_nb_intervalle += 1
    return dict_data


def create_artificial_data_set():
    # CREATION DU JEU DE DONNÉES ARTIFICIEL ============================================================================
    path = "./DATA/fake_data.txt"
    att1 = []
    att2 = []
    att3 = []
    att4 = []
    att5 = []
    with open(path, "r") as f:
        for line in f:
            line = line.split(',')
            att1.append(float(line[0]))
            att2.append(float(line[1]))
            att3.append(float(line[2]))
            att4.append(float(line[0]) * 2)
            att5.append(float(line[1]) + float(line[0]))
    data_set = (['x', 'y', 'z', 'x2', 'y2'], [att1, att2, att3, att4, att5])
    return data_set


def create_flight_data_set():
    path = './DOCKER/BaseDeDonnee/2008.csv'
    h_dep = []
    h_arr = []
    dist = []
    ret_dep = []
    ret_arr = []
    with open(path, 'r') as file:
        header = True
        cpt = 0
        for line in file:
            if header:
                header = False
            else:
                line = line.split(',')
                if line[4] != 'NA' and line[6] != 'NA' and line[18] != 'NA' and \
                   line[14] != 'NA' and line[15] != 'NA' and cpt < nb_tuple:
                    h_dep.append(int(line[4]))
                    h_arr.append(int(line[6]))
                    dist.append(int(line[18]))
                    ret_dep.append(int(line[14]))
                    ret_arr.append(int(line[15]))
                    cpt += 1
    data_set = [['heure_depart', 'heure_arrive', 'distance', 'retard_depart', 'retard_arrive'],
                [h_dep, h_arr, dist, ret_dep, ret_arr]]
    return data_set


def compute_correlation(data_set):
    nb_attribut = len(data_set[0])
    dict_corell = {}
    for iterrator_1 in range(nb_attribut - 1):
        for iterrator_2 in range(iterrator_1 + 1, nb_attribut):
            dict_corell[data_set[0][iterrator_1] + ', ' + data_set[0][iterrator_2]] = \
                utils.coef_correlation([data_set[1][iterrator_1], data_set[1][iterrator_2]])
    return dict_corell


def test_hyper_5D():
    """
    Dans ce test, les histogrammes sont en 2D, les requêtes à estimer sont des hyper-cubes.
    :return:
    """
    print("Création du jeu de données ...")

    # data_set = create_flight_data_set()
    # nom_fichier_test = "test_flight_hyper.json"
    data_set = create_artificial_data_set()
    nom_fichier_test = "test_artificial_hyper.json"
    data_set = [data_set[0], data_set[1]]
    print('Calcul des corrélations ...')
    dict_data = {'nb_tuple': len(data_set[1][0]),
                 'correlation': compute_correlation(data_set)
                 }

    print('Génération des requêtes ...')
    tab_intervalles_est = w.create_workload(data_set[1], 1, nb_req_test)
    tab_intervalles_est = [(data_set[0], i[0]) for i in tab_intervalles_est]
    print("Début des tests !")
    dict_data['Resultat'] = test_data_set(data_set, tab_intervalles_est)

    print('Écriture des résultats ...')
    with open('./DATA/' + nom_fichier_test, 'w') as f:
        f.write(json.dumps(dict_data, indent=4))


def test_hyper_2D():
    """
    Dans ce test, les histogrammes sont en 2D, les requêtes à estimer sont des hyper-cubes.
    :return:
    """
    print("Création du jeu de données ...")

    data_set = create_flight_data_set()
    nom_fichier_test = "test_flight_hyper_2D_nc.json"
    # data_set = create_artificial_data_set()
    # nom_fichier_test = "test_artificial_hyper_2D.json"
    # data_set = [data_set[0][:2], data_set[1][:2]]
    data_set = [[data_set[0][0], data_set[0][3]], [data_set[1][0], data_set[1][3]]]
    print('Calcul des corrélations ...')
    dict_data = {'nb_tuple': len(data_set[1][0]),
                 'correlation': compute_correlation(data_set)
                 }

    print('Génération des requêtes ...')
    tab_intervalles_est = w.create_workload(data_set[1], 1, nb_req_test)
    tab_intervalles_est = [(data_set[0], i[0]) for i in tab_intervalles_est]
    print("Début des tests !")
    dict_data['Resultat'] = test_data_set(data_set, tab_intervalles_est)

    print('Écriture des résultats ...')
    with open('./DATA/' + nom_fichier_test, 'w') as f:
        f.write(json.dumps(dict_data, indent=4))


def test_5D():
    """
    Dans ce test, les histogrammes sont en 2D, les requêtes sont aléatoire et ne portent pas necessairement sur tous les
    attributs.
    :return:
    """
    print("Création du jeu de données ...")
    data_set = create_flight_data_set()
    nom_fichier_test = "test_flight.json"
    # data_set = create_artificial_data_set()
    # nom_fichier_test = "test_artificial.json"
    data_set = [data_set[0], data_set[1]]
    print('Calcul des corrélations ...')
    dict_data = {'nb_tuple': len(data_set[1][0]),
                 'correlation': compute_correlation(data_set)
                 }

    print('Génération des requêtes ...')
    tab_intervalles_est = utils.generate_req(nb_req_test, data_set)
    print("Début des tests !")
    dict_data['Resultat'] = test_data_set(data_set, tab_intervalles_est)

    print('Écriture des résultats ...')
    with open('./DATA/'+nom_fichier_test, 'w') as f:
        f.write(json.dumps(dict_data, indent=4))


def test_2D():
    """
    Dans ce test, les histogrammes sont en 2D, les requêtes sont aléatoire et ne portent pas necessairement sur tous les
    attributs.
    :return:
    """
    print("Création du jeu de données ...")
    # data_set = create_flight_data_set()
    # nom_fichier_test = "test_flight_2D.json"
    data_set = create_artificial_data_set()
    nom_fichier_test = "test_artificial_2D.json"
    # data_set = [data_set[0][:2], data_set[1][:2]]
    data_set = [[data_set[0][0], data_set[0][3]], [data_set[1][0], data_set[1][3]]]
    print('Calcul des corrélations ...')
    dict_data = {'nb_tuple': len(data_set[1][0]),
                 'correlation': compute_correlation(data_set)
                 }

    print('Génération des requêtes ...')
    tab_intervalles_est = utils.generate_req(nb_req_test, data_set)
    print("Début des tests !")
    dict_data['Resultat'] = test_data_set(data_set, tab_intervalles_est)

    print('Écriture des résultats ...')
    with open('./DATA/'+nom_fichier_test, 'w') as f:
        f.write(json.dumps(dict_data, indent=4))


if __name__ == '__main__':
    test_hyper_2D()
    # test_5D()