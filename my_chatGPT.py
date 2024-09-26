import streamlit as st
from openai import OpenAI

# Title for the app
st.title("Welcome to KapurGPT 😎")

# Initialize OpenAI client
client = OpenAI()

# Helper function to initialize session state
def init_session_state():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    # Flag to check if the "Kapur" message was sent
    if "kapur_init" not in st.session_state:
        st.session_state["kapur_init"] = False

# Function to send the hidden "Your name is Kapur" message
def send_kapur_message():
    if not st.session_state["kapur_init"]:
        # Hidden message that tells the model its name is Kapur
        st.session_state.messages.append(
            {"role": "system", "content": "Your name is Kapur and you are a cool, sassy assistant."}
        )
        # Send this hidden message to ChatGPT
        _ = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=False,
        )
        # Set the flag to True so this is only done once
        st.session_state["kapur_init"] = True

# Function to render chat messages
def render_chat():
    for message in st.session_state.messages:
        if message["role"] != "system":  # Skip rendering system messages
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Function to get assistant response and stream it
def get_assistant_response():
    try:
        with st.chat_message("assistant"):
            # Send request to OpenAI and get streamed response
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)  # Handle the stream correctly
        return response
    except Exception as e:
        st.error(f"Error fetching response: {e}")
        return None

# Initialize session state variables
init_session_state()

# Send the hidden "Your name is Kapur" message
send_kapur_message()

# Render chat messages
render_chat()

# Chat input handling
if prompt := st.chat_input("What is up?"):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Render user's input
    with st.chat_message("user"):
        st.markdown(prompt)

    # Fetch assistant's response
    response = get_assistant_response()

    # Append assistant's response if valid
    if response:
        st.session_state.messages.append({"role": "assistant", "content": response})
