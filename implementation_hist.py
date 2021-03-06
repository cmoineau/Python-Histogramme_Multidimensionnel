"""
:author : Cyril MOINEAU
:creation_date : 12/02/20
:last_change_date : 17/03/20
:description : Script pour tester les histogrammes lors de l'implémentation.
"""

import MHIST.Mhist as mhist
import GENHIST.Genhist as genhist
import AVI.avi as avi
import STHOLES.Stholes as st
import utils
from STHOLES import Workload as w
import matplotlib.pyplot as plt
import time
import numpy as np


def test_mhist(tab_attribut, nom_dim, dim_estimer, intervalle_estimer):
    # Initialisation des paramètres ====================================================================================
    nombre_intervalle = 80

    # Création de l'histogramme ========================================================================================
    histogramme = mhist.Mhist(tab_attribut, nom_dim, nombre_intervalle)
    print('Hey')
    # Test =============================================================================================================
    o_avi = avi.Avi(tab_attribut)
    av_err = 0
    av_avi_err = 0
    nb_validation_q = 500
    workload = w.create_workload(tab_attribut, 0.05, nb_validation_q)
    for r in workload:
        est = histogramme.estimer(histogramme.attributes_name, r[0])
        est_avi = o_avi.estimation(range(len(tab_attribut)), r[0])
        print('est', est, 'avi', est_avi, 'real', r[1])
        av_err += abs(est - r[1])
        av_avi_err += abs(est_avi - r[1])
    print("Average Error :", av_err / nb_validation_q)
    print("Normalized Absolute Error :", av_err / av_avi_err)

    x = round(histogramme.estimer(histogramme.attributes_name, r[0]))
    print("Résultat estimé avec MHIST :   ", x)

    # Affichage de l'histogramme =======================================================================================
    histogramme.print()
    plt.scatter(tab_attribut[[nom_dim.index(d_e) for d_e in dim_estimer][0]],
                tab_attribut[[nom_dim.index(d_e) for d_e in dim_estimer][1]])
    plt.show()


def test_genhist(tab_data, nom_dim):
    # Initialisation des paramètres ====================================================================================
    b = 500
    xi = 20  # Qu'elle est une valeur classique ?
    alpha = (1/2)**(1/len(tab_data))
    test = tab_data.copy().tolist()  # Je fais une copie du tableau d'intervalle sous la forme d'une liste

    # Création de l'histogramme ========================================================================================
    histogramme = genhist.Genhist(tab_data, nom_dim, b, xi, alpha, verbeux=False)
    # histogramme.print()
    print(histogramme.estimer(['x'], [[-1, 1]]))
    # Test =============================================================================================================

    # print('nb_tot de tuple : ', histogramme.estimate(histogramme.dim_name, [[min(d), max(d)] for d in tab_data]))
    # print('Résultat estimé : ', histogramme.estimate(dim_estimer, intervalle_estimer))

                                #########################################
                                # TEST POUR TROUVER MEILLEUR XI ET B    #
                                #########################################


    # test_b = []
    # for b in range(25, 200):
    #     histogramme = genhist.Genhist(tab_data, nom_dim, b, xi, alpha, verbeux=False)
    #     moy = 0
    #     cpt = 0
    #     # workload = w.create_workload(tab_attribut, 0.05, 500)
    #     for r in workload:
    #         est = histogramme.estimer(histogramme.attributes_name, r[0])
    #         if r[1] != 0:
    #             err = (abs(est - r[1]) / r[1])
    #             # print("Estimation :", est, " Reel :", r[1], "Erreur :", err, " Bound :", r[0])
    #             # print("\n")
    #             moy += err
    #             cpt += 1
    #         # else:
    #         #     print("Estimation :", est, " Reel :", r[1], " Bound :", r[0])
    #         #     print("\n")
    #     # print("Erreur moyenne : ", moy / cpt)
    #     test_b.append(moy / cpt)
    # plt.plot(test_b)
    # plt.show()
    #
    # test_xi = []
    # b = 80
    # val_xi = range(5, 50)
    # for xi in val_xi:
    #     histogramme = genhist.Genhist(tab_data, nom_dim, b, xi, alpha, verbeux=False)
    #     moy = 0
    #     cpt = 0
    #     # workload = w.create_workload(tab_attribut, 0.05, 500)
    #     for r in workload:
    #         est = histogramme.estimer(histogramme.attributes_name, r[0])
    #         if r[1] != 0:
    #             err = (abs(est - r[1]) / r[1])
    #             # print("Estimation :", est, " Reel :", r[1], "Erreur :", err, " Bound :", r[0])
    #             # print("\n")
    #             moy += err
    #             cpt += 1
    #         # else:
    #         #     print("Estimation :", est, " Reel :", r[1], " Bound :", r[0])
    #         #     print("\n")
    #     # print("Erreur moyenne : ", moy / cpt)
    #     test_xi.append(moy / cpt)
    # plt.plot(test_xi)
    # plt.show()

    # Affichage de l'histogramme =======================================================================================
    # histogramme.print()
    # plt.scatter(tab_attribut[[nom_dim.index(d_e) for d_e in dim_estimer][0]],
    #             tab_attribut[[nom_dim.index(d_e) for d_e in dim_estimer][1]])
    # plt.show()


def test_st(tab_attribut, nom_dim):
    nb_intervalle = 500
    nb_req_entrainement = 200
    # Création de l'histogramme ========================================================================================
    print("Création d'un set d'entraînement pour ST-Holes ...")
    nf_histogramme = st.Stholes(nom_dim, nb_intervalle, verbeux=True)
    histogramme = st.Stholes(nom_dim, nb_intervalle, verbeux=True)
    train_workload = w.create_workload_full(tab_attribut, 0.01, nb_req_entrainement)
    histogramme.BuildAndRefine([([[min(a), max(a)] for a in tab_attribut], len(tab_attribut[0]))])
    histogramme.BuildAndRefine(train_workload)
    # histogramme.print(tab_attribut=tab_attribut)  # tab attribut permet d'afficher les points du jeu de donnée (2D)
    nf_histogramme.BuildAndRefine(train_workload)
    # nf_histogramme.print(tab_attribut=tab_attribut)  # tab attribut permet d'afficher les points du jeu de donnée (2D)

    # w.print_workload(train_workload)
    print("Lancement de la construction de St-Holes !")
    o_avi = avi.Avi(tab_attribut, nom_dim)
    # On commence avec une requête sur l'ensemble des données
    t = time.time()
    # histogramme.BuildAndRefine([([[min(a), max(a)] for a in tab_attribut], len(tab_attribut[0]))])

    print("Temps initialisation new ", time.time() - t)
    nb_validation_q = 500
    # test_workload = train_workload
    test_workload = w.create_workload(tab_attribut, 0.05, nb_validation_q)
    av_err = 0
    nf_av_err = 0
    av_avi_err = 0
    for r in test_workload:
        est = round(histogramme.estimer(histogramme.attributes_name, r[0]))
        nf_est = round(nf_histogramme.estimer(r[0], histogramme.attributes_name))

        est_avi = o_avi.estimation(histogramme.attributes_name, r[0])
        print('est', est, 'nf_est', nf_est, 'real', r[1])
        av_err += abs(est - r[1])
        av_avi_err += abs(est_avi - r[1])
        nf_av_err += abs(nf_est - r[1])
    print("Average Error :", av_err / nb_validation_q)
    print("Average nf Error :", nf_av_err / nb_validation_q)
    print("Normalized Absolute Error :", av_err / av_avi_err)


def test_avi(tab_attribut, nom_dim):
    o_avi = avi.Avi(tab_attribut, nom_dim)
    nb_validation_q = 500
    test_workload = w.create_workload(tab_attribut, 0.05, nb_validation_q)
    erreur = 0
    for r in test_workload:
        x = round(o_avi.estimation(nom_dim, r[0]))
        erreur += abs(x - r[1])
        print("reel:", r[1], " estimé:", x, " erreur ")
    print("Erreur absolus moyenne", erreur/nb_validation_q )


if __name__ == '__main__':
    # Lecture des données ==============================================================================================
    path = "./DATA/fake_data.txt"
    att1 = []
    att2 = []
    att3 = []
    with open(path, "r") as f:
        for line in f:
            line = line.split(',')
            att1.append(float(line[0]))
            att2.append(float(line[1]))
            att3.append(float(line[2]))

    # path = './DOCKER/BaseDeDonnee/2008.csv'
    # h_dep = []
    # h_arr = []
    # dist = []
    # ret_dep = []
    # ret_arr = []
    # nb_tuple = 10000
    # with open(path, 'r') as file:
    #     header = True
    #     cpt = 0
    #     for line in file:
    #         if header:
    #             header = False
    #         else:
    #             line = line.split(',')
    #             if (line[4] != 'NA' and line[6] != 'NA' and line[18] != 'NA' and \
    #                     line[14] != 'NA' and line[15] != 'NA') and nb_tuple > cpt:
    #                 h_dep.append(int(line[4]))
    #                 h_arr.append(int(line[6]))
    #                 dist.append(int(line[18]))
    #                 ret_dep.append(int(line[14]))
    #                 ret_arr.append(int(line[15]))
    #                 cpt += 1
    # data_set = [['heure_depart', 'heure_arrive', 'distance', 'retard_depart', 'retard_arrive'],
    #             [h_dep, h_arr, dist, ret_dep, ret_arr]]

    # Paramètres =======================================================================================================
    #
    # # att1_square = np.array(att1).copy() ** 2
    # att2_lin = np.array(att1).copy() * 2
    # #
    tab_attribut = np.array([att1, att3])
    nom_dim = ['x', 'y']
    #
    # tab_attribut = np.array(data_set[1][:2])
    # nom_dim = data_set[0][:2]
    #
    #
    # # Lancement des tests ==============================================================================================
    # print('===============================================TEST======================================================')
    # # test_avi(tab_attribut, nom_dim)
    # test_st(tab_attribut, nom_dim)
    # # test_mhist(tab_attribut, nom_dim, dim_estimer, intervalle_estimer)
    test_genhist(tab_attribut, nom_dim)

