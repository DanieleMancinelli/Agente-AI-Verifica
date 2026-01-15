import streamlit as st
from models import Ingredient

def tool_pantry(nome, qta, scad):
    nome = nome.strip().lower().replace("*", "")
    if len(nome) < 2: return
    
    qta = qta.strip()
    # Accetta True solo se è scritto esplicitamente, altrimenti sempre False
    scad_bool = "true" in str(scad).lower()
    
    for i in st.session_state.pantry:
        if i.nome == nome:
            if qta != "?": i.quantita = qta
            i.in_scadenza = scad_bool
            return
    st.session_state.pantry.append(Ingredient(nome=nome, quantita=qta, in_scadenza=scad_bool))

def tool_pref(testo):
    testo = testo.strip().capitalize()
    if testo and testo not in st.session_state.profile.vincoli_salute:
        st.session_state.profile.vincoli_salute.append(testo)
