import datetime
import json
import os
from dotenv import load_dotenv
import requests
import msal

processed_users_file_name = "processed_users.json"
processed_users = {}
def getNewUsers():
    print('Beggining ...')
    try:
        load_dotenv()
        tenant_id = os.getenv("TENANT_ID")
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        lookback_days = 2

        # Date de filtre
        since = (datetime.datetime.now() - datetime.timedelta(days=lookback_days))
        since_iso = since.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Authentification via MSAL
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        app = msal.ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret
        )

        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" not in result:
            raise Exception(f"Erreur d'authentification : {result.get('error_description')}")

        token = result["access_token"]

        # Appel Graph API
        #url = f"https://graph.microsoft.com/v1.0/users?$select=id,displayName,mail,userPrincipalName,userType,department,manager,officeLocation,companyName,jobTitle,createdDateTime&$filter=createdDateTime ge {since_iso}"
        url = f"https://graph.microsoft.com/v1.0/users?$select=id,displayName,mail,userPrincipalName,userType,department,manager,officeLocation,companyName,jobTitle,createdDateTime&$filter=createdDateTime ge {since_iso} and userType eq 'Member'"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers)

        if resp.status_code != 200:
            raise Exception(f"Erreur Graph API : {resp.text}")

        return resp.json()   # retourne le dict Python directement

    except Exception as e:
        print(f"Erreur : {str(e)}")
        return {"error": str(e)}


def getProcessedUsers():
    if os.path.exists(processed_users_file_name):
        with open(processed_users_file_name, "r") as file:
            try:
                processed_users = json.load(file)
                if not processed_users:
                    processed_users = {}
                return processed_users
            except json.JSONDecodeError:
                # Gérer le cas où le fichier est vide ou corrompu
                print("Le fichier est vide ou corrompu, on démarre avec un dictionnaire vide.")
    else:
        return {}

def updateProcessedUsers(old_processed_users):
    with open(processed_users_file_name, "w") as file:
        json.dump(old_processed_users, file, indent=4)

if __name__ == "__main__":
    # Récupération des utilisateurs AD rajoutés sur les 24h dernières heures
    data = getNewUsers()
    # Ouverture du fichier des utilisateurs déjà traités
    old_processed_users = getProcessedUsers()
    #print(f"Processed users: {old_processed_users}")

    # Itération sur le dictonnaire
    '''for cle, valeur in old_processed_users.items():
        print(f"La clé est : {cle} et la valeur est : {valeur}")
    print("fin de la boucle des users traités")'''
    #print("Data",data)

    #Itération sur les nouveaux utilisateurs
    for user in data.get("value", []):
        print(f"User: {user.get('displayName')} - userPrincipalName: {user.get('userPrincipalName')} - createdDateTime: {user.get('createdDateTime')} - jobTitle: {user.get('jobTitle')}- officeLocation:{user.get('officeLocation')}- companyName:{user.get('companyName')} - userType:{user.get('userType')} - manager:{user.get('manager')}")
        processed_user = user.copy()
        processed_user['processed'] = True
        if user.get('id') not in old_processed_users:
            old_processed_users[processed_user['id']] = processed_user
            updateProcessedUsers(old_processed_users) # Mise à jour du fichier des users traités
        else:
            print(f"L'utilisateur {user.get('displayName')} existe déjà.")