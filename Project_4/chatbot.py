"""
PROJECT 4: Google Cloud Platform
AUTHOR: Cat Luong
Email: luongcn@mail.uc.edu

THIS IS THE CODE TO BE RAN IN THE CLI
"""

import os
from google.cloud import dialogflow
import uuid

def detect_intent(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    
    return response

def get_credentials():
    project_id = "cs6065"
    session_id = str(uuid.uuid4())
    language_code = "en"
    return project_id, session_id, language_code

def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\My Stuff\Classes\Spring 2024\CS 6065\Project_4\credentials.json"
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/credentials.json"
    project_id, session_id, language_code = get_credentials()
    
    first_time = True
    while True:
        if first_time:
            print("\nUser Information:")
            firstname = input("First Name: ")
            lastname = input("Last Name: ")
            email = input("Email Address: ")
            print("\nStart chatting")
            print("----------------")
            first_time = False

        text = input("\nYou: ")
        response = detect_intent(project_id, session_id, text, language_code)
        chat_response = response.query_result.fulfillment_text
        print("Chatbot: " + chat_response)

        if (response.query_result.intent.display_name == "end"):
            print("\nUser Information: ")
            print("First name: " + firstname)
            print("Last Name: " + lastname)
            print("Email: " + email)

            print("\nCreator Information: ")
            print("First name: Cat")
            print("Last Name: Luong")
            print("Email: luongcn@mail.uc.edu")
            break


if __name__ == "__main__":
    main()