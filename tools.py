import streamlit as st
from models import Ingredient

def tool_pantry(input_str: str):
    """Aggiunge o aggiorna un ingrediente. Formato: Nome, Quantita, True/False"""
    try:
        nome, qta, scad = [x.strip() for x in input_str.split(",")]
        # Cerchiamo se esiste già
        for i in st.session_state.pantry:
            if i.nome.lower() == nome.lower():
                i.quantita = qta
                i.in_scadenza = scad.lower() == "true"
                return f"SISTEMA: {nome} aggiornato."
        
        nuovo = Ingredient(nome=nome, quantita=qta, in_scadenza=scad.lower()=="true")
        st.session_state.pantry.append(nuovo)
        return f"SISTEMA: {nome} aggiunto alla dispensa."
    except:
        return "SISTEMA: Errore. Formato corretto: Nome, Quantità, True/False"

def tool_pref(info: str):
    """Salva preferenze o allergie."""
    st.session_state.profile.vincoli_salute.append(info)
    return f"SISTEMA: Preferenza '{info}' salvata."
