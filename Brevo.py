from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("BREVO_API_KEY")

print(f"API KEY: {api_key}")
# Configure API key authorization: api-key

def init_brevo():
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    #Instanciation du client
    api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
    print(f"Instance API: {api_instance}")
    return api_instance
def get_lists(api_instance):
    try:
        # Récupérer toutes les listes
        api_response = api_instance.get_lists(limit=50, offset=0)
        pprint(api_response.lists)  # Affiche la liste des listes
    except ApiException as e:
        print("Erreur lors de la récupération des listes: %s\n" % e)

def create_user(api_instance, email, attributes, list_ids):
    contact = sib_api_v3_sdk.CreateContact(
        email=email,
        attributes=attributes,
        list_ids=list_ids  # ID(s) des listes dans lesquelles ajouter ce contact
    )

    '''contact = sib_api_v3_sdk.CreateContact(
        email="dimitri.vegas@meogroup-consulting.com",
        attributes={
            "FIRSTNAME": "Dimitri",
            "LASTNAME": "Vegas",
            "SMS": "+33123456789"
        },
        list_ids=[423]  # ID(s) des listes dans lesquelles ajouter ce contact
    )'''
    try:
        # Récupérer toutes les listes
        api_response = api_instance.create_contact(contact)
        pprint(api_response)  # Affiche la liste des listes
    except ApiException as e:
        print("Erreur lors de la création du contact: %s\n" % e)

'''if __name__ == "__main__":
    api_instance = init_brevo()
    #get_lists(api_instance)
    create_user(api_instance)'''
