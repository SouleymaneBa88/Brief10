from Data_base import DataBase

class Groupes:
    def __init__(self):
        self.data = DataBase()
        self.connection = self.data.get_connection()

    def ajouter_client(self):
        """ Permet d'ajouter un client(gropue) """
        cusror = self.connection.cursor(dictionary=True)
        nomgroupe = input("NOM du groupe : ")
        representant = input("REPRESENTANT : ")
        telephone = input("Telephone du client : ")

        cusror.execute(""" select * from Clients
                    where telephone_client = %s """,(telephone,))
        
        existe = cusror.fetchone()

        if existe:
            print("Numero de telephone deja utilise !")
            return
        try:
            cusror.execute(""" 
                            insert into Clients (nomgroupe , representant, telephone_client)
                        values(%s, %s, %s) """,
                        (nomgroupe, representant, telephone))
            self.connection.commit()
            print("Client ajoute avec sucess !")
        except Exception as e:
            print(f"VOus avez commit une erreur")
        cusror.close()


    def liste_client(self):
        """ Affiche la liste des clients ajouter """
        cusror = self.connection.cursor(dictionary=True)

        cusror.execute("select id_client,nomgroupe,representant,telephone_client from Clients")
        resultat = cusror.fetchall()

        print("\n" + "="*50)
        print(f"{'ID':<15} | {'Groupe':<20} | {'NOM':<20} | {'TELEPHONE':<20} ")
        print("="*50)
        for client in resultat:
            print(f"{client['id_client']:<15} "
                f"{str(client['nomgroupe']):<20} "
                f"{str(client['representant']):<20} "
                f"{str(client['telephone_client']):<20} "
            )
        cusror.close()