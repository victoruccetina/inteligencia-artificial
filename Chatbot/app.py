import os

import streamlit as st
from dotenv import find_dotenv, load_dotenv
from google import genai
from openai import OpenAI

MODELS = {
    "Gemini": ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.8-flash"],
    "OpenAI": ["gpt-5.6-luna", "gpt-4o-mini"],
}
GEMINI_KEY_URL = "https://aistudio.google.com/apikey"
OPENAI_KEY_URL = "https://platform.openai.com/api-keys"

load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("Chatbot")


def missing_key_message(provider: str) -> str:
    if provider == "Gemini":
        return (
            f"Missing `GEMINI_API_KEY`. Create a key at [{GEMINI_KEY_URL}]({GEMINI_KEY_URL}) "
            "and put it in `.env`."
        )
    return (
        f"Missing `OPENAI_API_KEY`. Create a key at [{OPENAI_KEY_URL}]({OPENAI_KEY_URL}) "
        "and put it in `.env`."
    )


def api_error(provider: str, exc: Exception) -> str:
    text = str(exc)
    if provider == "Gemini" and "leaked" in text.lower():
        return (
            "This API key was reported as leaked and Google disabled it. "
            f"Create a **new** key at [{GEMINI_KEY_URL}]({GEMINI_KEY_URL}) and put it in "
            "`.env` as `GEMINI_API_KEY`."
        )
    return f"Could not call {provider}: {exc}"


def reset_chat(provider: str, model: str) -> None:
    st.session_state.provider = provider
    st.session_state.model = model
    st.session_state.messages = []
    if provider == "Gemini":
        client = genai.Client(api_key=GEMINI_API_KEY)
        st.session_state.gemini_client = client
        st.session_state.gemini_chat = client.chats.create(model=model)
        st.session_state.openai_client = None
    else:
        st.session_state.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        st.session_state.gemini_client = None
        st.session_state.gemini_chat = None


with st.sidebar:
    provider = st.selectbox("Proveedor", list(MODELS))
    model = st.selectbox("Modelo", MODELS[provider])
    if st.button("Nuevo chat"):
        reset_chat(provider, model)
        st.rerun()

api_key = GEMINI_API_KEY if provider == "Gemini" else OPENAI_API_KEY
if not api_key:
    st.error(missing_key_message(provider))
    st.stop()

if (
    st.session_state.get("provider") != provider
    or st.session_state.get("model") != model
    or "messages" not in st.session_state
):
    reset_chat(provider, model)


def reply_from_model(prompt: str) -> str:
    if provider == "Gemini":
        response = st.session_state.gemini_chat.send_message(prompt)
        return response.text or ""
    response = st.session_state.openai_client.responses.create(
        model=model,
        input=st.session_state.messages,
    )
    return response.output_text or ""


prompt = st.chat_input("Escribe un mensaje")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Pensando..."):
        try:
            reply = reply_from_model(prompt)
        except Exception as exc:
            reply = api_error(provider, exc)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Only render from history so each message appears once (no duplicate on rerun).
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
