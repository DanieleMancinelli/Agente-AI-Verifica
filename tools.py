import streamlit as st
from models import Ingredient

def tool_pantry(nome, qta, scad):
    nome = nome.strip().lower().replace("*", "")
    if len(nome) < 2: return
    
    qta = qta.strip()
    # FORZATURA: Scadenza True solo se l'input contiene ESPLICITAMENTE "true"
    scad_bool = str(scad).lower().strip() == "true"
    
    for i in st.session_state.pantry:
        if i.nome == nome:
            if qta not in ["?", "non specificata"]: i.quantita = qta
            i.in_scadenza = scad_bool
            return
    st.session_state.pantry.append(Ingredient(nome=nome, quantita=qta, in_scadenza=scad_bool))

def tool_pref(testo):
    testo = testo.strip().capitalize()
    blacklist = ["No", "Niente", "Tutto a posto", "Ok", "Si", "Nulla"]
    if any(b in testo for b in blacklist) or len(testo) < 3: return
    if testo not in st.session_state.profile.vincoli_salute:
        st.session_state.profile.vincoli_salute.append(testo)
