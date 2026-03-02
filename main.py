from Gestion import GestionDuService
from authentification import Authentification
from groupe import Groupes


class Menu():
    def __init__(self):
        self.gerer = GestionDuService()
        self.client = Groupes()

    def lancer(self):

        while True:
            print("\n" + "="*50)
            print("        SYSTEME DE GESTION")
            print("="*50)
            print("1 - Ajouter Client")
            print("2 - Liste des Clients")
            print("3 - Voir Créneaux")
            print("4 - Voir Disponibilités")
            print("5 - Faire une Réservation")
            print("6 - Annuler une Réservation")
            print("7 - Exporter en CSV")
            print("8 - Supprimer une reservation annulee")
            print("0 - Quitter")
            print("="*50)

            choix = input("Votre choix : ")

            match choix:

                case "1":
                    self.client.ajouter_client()

                case "2":
                    self.client.liste_client()

                case "3":
                    self.gerer.Afficher_liste_creneaux_dispo_no()

                case "4":
                    date = input("Entrer la date (YYYY-MM-DD) : ")
                    self.gerer.afficher_disponibilites(date)

                case "5":
                    self.gerer.reservation()

                case "6":
                    self.gerer.annuler_reservation()

                case "7":
                    self.gerer.exporter_csv()
                case "8":
                        self.gerer.supprime_reservation_annule()

                case "0":
                    print(" Au revoir !")
                    break

                case _:
                    print(" Choix invalide, réessayez.")

Connexion = Authentification()

if Connexion.connexion():
    Menu().lancer()
