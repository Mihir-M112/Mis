import streamlit as st
import json
from mistral_models.model import query

def main():
    st.set_page_config(page_title="Mistral Chat", layout="wide")
    st.title("🌀 Mistral Chat")

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Initialize user input in session state
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    # Function to add messages to the chat history
    def add_message(sender, message, is_user=True):
        st.session_state.chat_history.append({"sender": sender, "message": message, "is_user": is_user})

    # Initial message from the app (only once)
    if not st.session_state.chat_history:
        add_message("Mistral", "Hi there! How can I assist you today?", is_user=False)

    # Sidebar for model selection and API key input
    with st.sidebar:
        hugging_face_api_key = st.text_input("API Key", type="password", placeholder="Optional")
        selected_model = st.selectbox("Model", [
            "Mixtral-8x7B-Instruct-v0.1",
            "Mistral-7B-Instruct-v0.2",
            "Mixtral-8x7B-v0.1",
            "Mistral-7B-Instruct-v0.1"
        ])

    # Chat input for user
    user_input = st.text_input("Your message...", key="user_input")

    # Button to submit the user input
    if st.button("Send"):
        if st.session_state.user_input:
            payload = {"inputs": st.session_state.user_input}
            try:
                if hugging_face_api_key:
                    output = query(payload, model_name=selected_model, token=hugging_face_api_key)
                else:
                    output = query(payload, model_name=selected_model)

                if isinstance(output, str):
                    output = output.replace('\\', '').replace('\n', ' ')

                add_message("User", st.session_state.user_input)
                add_message("Mistral", output, is_user=False)
                st.session_state.user_input = ""  # Clear input after submission
                st.experimental_rerun()  
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["sender"]):
            st.write(message["message"])

if __name__ == "__main__":
    main()
