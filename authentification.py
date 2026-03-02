import bcrypt
from datetime import datetime
from Data_base import DataBase
import os
from dotenv import load_dotenv
load_dotenv()

class Authentification():
    def __init__(self):
        self.data = DataBase()
        self.connection = self.data.get_connection()

    def hash_password(self,password):
        """ hacher un mot de passe avec bcrypt """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def veryfication_password(self,password,password_hash):
        """ verifie le mot de passe si sa correspond au password hacher """
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def inscrire(self):
        """ Gere les incription et aussi hash le mot de passe """
        print("Formulaire 'inscription")
        cursor = self.connection.cursor(dictionary=True)
        while True:
            nom = input("Nom : ")
            prenom = input("Prenom : ")
            email = os.getenv('DB_email')
            password = os.getenv('DB_PASSWORDad')
            password_hacher = self.hash_password(password)
            role = os.getenv('DB_role')
            cursor.execute("select * from Users where email_user = %s", (email,))
            user = cursor.fetchone()

            if user:
                print("Ce mail a deja ete utiliser !")
                return False
            else:
                try:
                    cursor.execute("""
                                insert into Users(nom_user, prenom_user, email_user, password, role_user)
                                VALUES (%s, %s, %s, %s, %s)
                                   """, (nom, prenom, email, password_hacher, role))
                    # print(cursor)
                    # print(cursor.execute())
                    self.connection.commit()
                    print("Inscription reussi !")
                except Exception as e:
                    print(e)
                cursor.close()
                break

    def connexion(self):
        """ gere la connexion  """
        print("Connection")
        cursor = self.connection.cursor(dictionary=True)

        email = input("Mail : ")
        password = input("Mot de passe : ")
        cursor.execute("select * from Users where email_user = %s", (email,))
        user = cursor.fetchone()

        if not user:
            print("Compte introuvable !")
            return None
        
        if not self.veryfication_password(password, user['password']):
            print("Mot de passe incorrect !")
            return None
        
        print(f"Bienvenu {user['prenom_user']} {user['role_user']}")
        print("-"*40)
        return user['id_user'], user['role_user'] 
        

# c = Authentification()
# c.inscrire()



