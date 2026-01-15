import streamlit as st
from models import UserProfile
from agent_engine import run_chef_agent

st.set_page_config(page_title="AI Chef", layout="wide")

if "pantry" not in st.session_state: st.session_state.pantry = []
if "profile" not in st.session_state: st.session_state.profile = UserProfile()
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.header("🛒 Dispensa Reale")
    for i in st.session_state.pantry:
        st.write(f"**{i.nome.capitalize()}**: {i.quantita} {'⚠️' if i.in_scadenza else ''}")
    st.divider()
    st.header("👤 Preferenze")
    for p in st.session_state.profile.vincoli_salute:
        st.write(f"- {p}")

st.title("👨‍🍳 AI Chef Agent")

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if ui := st.chat_input("Cosa hai in frigo?"):
    st.session_state.messages.append({"role": "human", "content": ui})
    st.chat_message("human").write(ui)
    ans = run_chef_agent(ui)
    st.chat_message("assistant").write(ans)
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.rerun()
