"""
PROJECT 4: Google Cloud Platform
AUTHOR: Cat Luong
Email: luongcn@mail.uc.edu
"""

import streamlit as st
import os
from chatbot import detect_intent
from chatbot import get_credentials


def ss_init() -> None:
    if "start" not in st.session_state:
        st.session_state["start"] = True
    if "query_done" not in st.session_state:
        st.session_state["query_done"] = [False, False, False]
    if "info_queries" not in st.session_state:
        st.session_state["info_queries"] = [
            "What is your Firstname?",
            "What is your Lastname?",
            "What is your Email?",
        ]
    if "user_info" not in st.session_state:
        st.session_state["user_info"] = [False, None, None, None]
    if "query_count" not in st.session_state:
        st.session_state["query_count"] = 0
    if "start_chat" not in st.session_state:
        st.session_state["start_chat"] = True
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "project_id" not in st.session_state:
        st.session_state["project_id"] = None
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = None
    if "language_code" not in st.session_state:
        st.session_state["language_code"] = None


def clear_ss() -> None:
    # Delete all the items in Session state
    for key in st.session_state.keys():
        del st.session_state[key]


def set_credentials(ss) -> None:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/credentials.json"
    ss.project_id, ss.session_id, ss.language_code = get_credentials()


def chat(ss) -> None:
    # Periodically populates previous messages to the chat everytime the website re-renders
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Say something")

    # Start prompting for information about Firstname, Lastname, and Email
    if ss.start:
        with st.chat_message("assistant"):
            text = "Before we get started please provide some information!"
            st.markdown(text)
        ss.messages.append({"role": "assistant", "content": text})

        with st.chat_message("assistant"):
            st.markdown(ss.info_queries[0])
        ss.messages.append({"role": "assistant", "content": ss.info_queries[0]})

        ss.start = False

    if not ss.start and not ss.user_info[0]:
        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)
            ss.user_info[ss.query_count + 1] = prompt
            ss.messages.append({"role": "user", "content": prompt})

            if ss.user_info[ss.query_count + 1] and ss.query_count < 2:
                with st.chat_message("assistant"):
                    st.markdown(ss.info_queries[ss.query_count + 1])
                ss.messages.append(
                    {
                        "role": "assistant",
                        "content": ss.info_queries[ss.query_count + 1],
                    }
                )
                ss.query_count += 1

    if ss.user_info[3] and ss.start_chat:
        with st.chat_message("assistant"):
            start_message = "Thank you for your information. Now we can start chatting!"
            st.markdown(start_message)
        ss.messages.append({"role": "assistant", "content": start_message})
        ss.start_chat = False

    if ss.user_info[0] and prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        ss.messages.append({"role": "user", "content": prompt})

        response = detect_intent(ss.project_id, ss.session_id, prompt, ss.language_code)
        response_text = response.query_result.fulfillment_text

        with st.chat_message("assistant"):
            st.markdown(response_text)

            ss.messages.append({"role": "assistant", "content": response_text})

            if response.query_result.intent.display_name == "end":
                st.markdown("\nUser Information: ")
                st.markdown("First name: " + ss.user_info[1])
                st.markdown("Last Name: " + ss.user_info[2])
                st.markdown("Email: " + ss.user_info[3])

                st.markdown("\nCreator Information: ")
                st.markdown("First name: Cat")
                st.markdown("Last Name: Luong")
                st.markdown("Email: luongcn@mail.uc.edu")

                st.stop()
                clear_ss()

    if ss.user_info[1] and ss.user_info[2] and ss.user_info[3]:
        ss.user_info[0] = True


def main():
    st.title("College Chatbot")
    ss_init()
    ss = st.session_state
    set_credentials(ss)
    chat(ss)


if __name__ == "__main__":
    main()
