from Data_base import DataBase
import csv
from groupe import Groupes

class GestionDuService:
    def __init__(self):
        self.data = DataBase()
        self.connection = self.data.get_connection()
        self.listeClient = Groupes()
    
    def Afficher_liste_creneaux_dispo_no(self):
        """ affiche la liste de toutes les creneaux meme si c'est pas dispo """
        cursor = self.connection.cursor(dictionary=True)
       
        cursor.execute("""
            SELECT 
                COALESCE(g.representant, '---') AS client,
                COALESCE(r.date_reservation, '---') AS date_reservation,
                c.heureDebut_creneaux,
                c.heureFin,
                COALESCE(r.statut, 'LIBRE') AS statut
            FROM creneaux c
            LEFT JOIN reservation r ON c.id_creneaux = r.id_creneaux
            LEFT JOIN Clients g ON g.id_client = r.id_client
            ORDER BY c.heureDebut_creneaux;
        """)

        resultat = cursor.fetchall()

        print("\n" + "="*90)
        print(f"{'CLIENTs':<15} {'DATE RESERVATION':<20} {'DEBUT':<20} {'FIN':<20} {'STATUT':<10}")
        print("="*90)

        for row in resultat:
            print(f"{row['client']:<15} "
                f"{str(row['date_reservation']):<20} "
                f"{str(row['heureDebut_creneaux']):<20} "
                f"{str(row['heureFin']):<20} "
                f"{row['statut']:<10}")

        print("="*90)
        cursor.close()


    def afficher_disponibilites(self, date_demandee):
        """ affiche la liste des creneaux dispo pour une date """
        cursor = self.connection.cursor(dictionary=True)

        query = """
            SELECT c.id_creneaux,
                c.heureDebut_creneaux,
                c.heureFin
            FROM creneaux c
            LEFT JOIN reservation r 
                ON c.id_creneaux = r.id_creneaux
                AND r.date_reservation = %s
            WHERE r.id_reservation IS NULL
            OR r.statut = 'annule'
            ORDER BY c.heureDebut_creneaux;
        """

        cursor.execute(query, (date_demandee,))
        resultats = cursor.fetchall()

        print("\n=== Créneaux Disponibles ===")
        print("-" * 40)
        print("\n" + "="*40)
        print(f"{'heureDebut':<15} {'heureFin':<20} ")
        print("="*40)
        for row in resultats:
            print(f"{str(row['heureDebut_creneaux']) :<15}"
                  f"{str(row['heureFin']) :<15}"
                  )

        print("-" * 40)
        cursor.close()
    

    def reservation(self):
        """ permet de faire une reservation """
        cursor = self.connection.cursor(dictionary=True)
        self.listeClient.liste_client()
        client= int(input("ID du client : "))
        motif_resrver = input("MOTIF DE RESERVATION : ")
        Date = input("DATE DU RESERVATION (ex: 2026-02-28)")
        cursor.execute("SELECT id_creneaux, heureDebut_creneaux, heureFin FROM creneaux")
        creneaux = cursor.fetchall()

        print("\n===== LISTE DES CRENEAUX =====")
        for c in creneaux:
            print(f"ID: {c['id_creneaux']} | {c['heureDebut_creneaux']} → {c['heureFin']}")

        id_creneaux = int(input("\nChoisir ID Créneau : "))

        cursor.execute(""" 
                         SELECT * FROM reservation
                        WHERE id_creneaux = %s
                        AND date_reservation = %s
                        AND statut = 'reserve'""",(id_creneaux,Date))
        
        exist = cursor.fetchone()

        if exist:
            print("Reservation rejete!\n Cause: Ce creneaux a ete deja pris")
            return

        cursor.execute(""" 
                        insert into reservation(type_reservation,date_reservation,id_client,id_creneaux,statut) 
                       values(%s,%s,%s,%s,'reserve')""",(motif_resrver, Date,client,id_creneaux))
        self.connection.commit()
        print("Reservation reussi !")
        cursor.close()


    def annuler_reservation(self):
        cursor = self.connection.cursor(dictionary=True)

        question = input("VOULEZ-VOUS ANNULER UNE RESERVATION (oui/non) : ").lower()

        if question == 'oui':

            cursor.execute("""
                SELECT * 
                FROM reservation 
                WHERE statut = 'reserve'
                ORDER BY date_reservation
            """)

            resultat = cursor.fetchall()

            if not resultat:
                print(" Aucune réservation à annuler.")
                return

            print("\n" + "="*90)
            print(f"{'ID':^5} | {'Motif':^15} | {'Date':^15} | {'Client':^10} | {'Creneau':^10} | {'Statut':^10}")
            print("="*90)

            for row in resultat:
                print(f"{row['id_reservation']:^5} | "
                    f"{row['type_reservation']:^15} | "
                    f"{str(row['date_reservation']):^15} | "
                    f"{row['id_client']:^10} | "
                    f"{row['id_creneaux']:^10} | "
                    f"{row['statut']:^10}")

            choix = input("\nID de la reservation à annuler : ")

            cursor.execute("""
                SELECT * 
                FROM reservation 
                WHERE id_reservation = %s 
                AND statut = 'reserve'
            """, (choix,))

            existe = cursor.fetchone()

            if not existe:
                print("ID invalide ou réservation déjà annulée.")
                return

            cursor.execute("""
                UPDATE reservation
                SET statut = 'annule'
                WHERE id_reservation = %s
            """, (choix,))

            self.connection.commit()

            print(" Réservation annulée avec succès.")

        else:
            print("Annulation annulée.")

        cursor.close()

    def supprime_reservation_annule(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(""" select * from reservation where statut = 'annule' """)
        resultat = cursor.fetchall()

        if not resultat:
            print("Aucune reservation n'a ete annulee!")
            return
        

        print("\n" + "="*90)
        print(f"{'ID':^5} | {'Motif':^15} | {'Date':^15} | {'Client':^10} | {'Creneau':^10} | {'Statut':^10}")
        print("="*90)

        for row in resultat:
            print(f"{row['id_reservation']:^5} | "
                f"{row['type_reservation']:^15} | "
                f"{str(row['date_reservation']):^15} | "
                f"{row['id_client']:^10} | "
                f"{row['id_creneaux']:^10} | "
                f"{row['statut']:^10}")
    
        choix = int(input("ID du reservation a supprimer : "))

        cursor.execute(""" delete from reservation where id_reservation =%s """,(choix,))
        self.connection.commit()
        print("Suppression avec succes !")
        cursor.close()


    def exporter_csv(self):
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                c.heureDebut_creneaux,
                c.heureFin,
                g.nomgroupe AS groupe,
                r.type_reservation AS motif,
                r.date_reservation AS date,
                g.representant AS responsable
            FROM reservation r
            JOIN creneaux c ON r.id_creneaux = c.id_creneaux
            JOIN Clients g ON r.id_client = g.id_client
            WHERE r.statut = 'reserve'
            ORDER BY c.heureDebut_creneaux;
        """)

        resultats = cursor.fetchall()

        with open("planning_journalier.csv", "w", newline="", encoding="utf-8") as fichier:

            writer = csv.writer(fichier)

            writer.writerow([
                "Heure Debut",
                "Heure Fin",
                "Groupe",
                "Motif",
                "Responsable",
                "Date"
            ])

            for row in resultats:
                writer.writerow([
                    row["heureDebut_creneaux"],
                    row["heureFin"],
                    row["groupe"],
                    row["motif"],
                    row["responsable"],
                    row["date"]
                ])

        print("Export terminé : planning_journalier.csv")

