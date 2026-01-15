import streamlit as st
from models import UserProfile
from agent_engine import run_chef_agent

st.set_page_config(page_title="AI Chef Assistant", layout="wide")

# Inizializzazione Stato
if "pantry" not in st.session_state: st.session_state.pantry = []
if "profile" not in st.session_state: st.session_state.profile = UserProfile()
if "messages" not in st.session_state: st.session_state.messages = []

# SIDEBAR (Richiesta dalla verifica)
with st.sidebar:
    st.header("🛒 Dispensa Reale")
    if not st.session_state.pantry:
        st.info("Nessun ingrediente.")
    for i in st.session_state.pantry:
        st.write(f"**{i.nome}** ({i.quantita}) {'⚠️' if i.in_scadenza else ''}")
    
    st.divider()
    st.header("👤 Preferenze")
    for p in st.session_state.profile.vincoli_salute:
        st.write(f"- {p}")

# CHAT INTERFACE
st.title("👨‍🍳 Progetto Agente AI Cucina")

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if ui := st.chat_input("Ciao! Cosa hai in frigo?"):
    st.session_state.messages.append({"role": "human", "content": ui})
    st.chat_message("human").write(ui)
    
    with st.spinner("L'agente sta pensando..."):
        answer = run_chef_agent(ui)
        st.chat_message("assistant").write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
