import os
from hubspot import HubSpot
from hubspot.crm.contacts import ApiException
import requests
import random as r
import json

def main(event):
    hs_contacts_api_secret = HubSpot(access_token=os.getenv('hs_contacts_api_secret'))
    lms_api_key = HubSpot(access_token=os.getenv('lms_api_key'))
    email = event.get("inputFields").get("email")
    firstname = event.get("inputFields").get("firstname")
    lastname = event.get("inputFields").get("lastname")
    hs_object_id = event.get("inputFields").get("hs_object_id")
    hs_headers={'Content-Type': 'application/json','Authorization': 'Bearer '+ os.getenv('hs_contacts_api_secret')}
    '''hs_api_response = (requests.get("https://api.hubapi.com/contacts/v1/contact/email/" + email + "/profile", headers=hs_headers)).json()
    print(hs_api_response.get('vid'))'''

    lms_headers={'Content-Type': 'application/json'}
    lms_api_response = (requests.get("https://usi.matrixlms.com/api/v2/users?api_key=" + os.getenv('lms_api_key') + "&email=" + email, headers=lms_headers)).json()
    if lms_api_response.get('data')[0]:
        print("Users exists in LMS, userid: " +str(lms_api_response.get('data')[0].get('id')))
        lms_learner_id = lms_api_response.get('data')[0].get('id')
    else: 
        print("User with email id: " + email + " doesnot exist in LMS")
         
    hs_update_payload = {
    "properties": {
        "lms_learner_id": lms_learner_id
        }
    }
    hs_update_response = requests.patch("https://api.hubapi.com/crm/v3/objects/contacts/" + hs_object_id, data=json.dumps(hs_update_payload), headers=hs_headers)
    return {
        "outputFields": {
            "contact_id": hs_object_id,
            "lms_learner_id": lms_learner_id,
        }
    }
