import streamlit as st
import json
from mistral_models.model import query

def main():
  st.title("Mistral Text-to-Text Chat App")

  # Chat history (list to store messages)
  chat_history = []

  # Function to add messages to the chat history
  def add_message(sender, message, is_user=True):
    chat_history.append({"sender": sender, "message": message, "is_user": is_user})

  # Initial message from the app
  add_message("Mistral", "Hi there! How can I assist you today?", is_user=False)

  # Input box for Hugging Face API key (Optional)
  hugging_face_api_key = st.text_input("Enter Hugging Face API Key")

  # Sidebar for model selection
  with st.sidebar:
    selected_model = st.selectbox("Select Model", [
      "Mixtral-8x7B-Instruct-v0.1",
      "Mistral-7B-Instruct-v0.2",
      "Mixtral-8x7B-v0.1",
      "Mistral-7B-Instruct-v0.1"
    ])

    # Description about Mistral models (replace with specific details)
    st.write("**About Mistral Models**")
    st.markdown("The provided Mistral models are large language models (LLMs) trained on a massive dataset of text and code. They can be used for various tasks, including:\n"
              "- **Text-to-text generation:** Generate different creative text formats,  like poems, code, scripts, musical pieces, email, letters, etc.\n"
              "- **Question answering:** Answer your questions in an informative way, even if they are open ended, challenging, or strange.\n"
              "- **Translation:** Translate languages.\n"
              "- **Summarization:** Provide summaries of factual topics or create stories.\n")

    st.info("**Proper Usage Tips**"
            "\n- Provide clear and concise prompts or questions for the model to understand your request.\n"
            "\n- Break down complex tasks into smaller, more manageable steps for the model.\n"
            "\n- Use the model's capabilities to explore ideas, generate creative text formats, or answer your questions in an informative way.\n"
            "\n- Be aware that LLMs are still under development and may sometimes produce incorrect or misleading outputs. It's important to critically evaluate the model's responses.")

  # Chat input for user
  user_input = st.chat_input("Type your message here...")

  # Process user input if submitted
  if user_input:
    # Send user message to your text-to-text API (replace with your logic)
    payload = {"inputs": user_input}

    # Potentially use the Hugging Face API key if provided
    if hugging_face_api_key:
      print(f"Using Hugging Face API with key: {hugging_face_api_key}")
      output = query(payload, model_name=selected_model, token=hugging_face_api_key)
    else:
      # Use your default Mistral query function (assuming it doesn't require an API key)
      output = query(payload, model_name=selected_model)

    # Assuming query returns a string, process it here (optional)
    if isinstance(output, str):
      output = output.replace('\\', '').replace('\n', ' ')  # Replace newlines and backslashes for regular text

    # Add user message and response to chat history
    add_message("User", user_input)
    add_message("Mistral", output, is_user=False)

  # Display chat history
  for message in chat_history:
    with st.chat_message(message["sender"]):
      st.write(message["message"])

if __name__ == "__main__":
  main()