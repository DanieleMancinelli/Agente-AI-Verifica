import os, re
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools import tool_pantry, tool_pref

load_dotenv()
llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

def run_chef_agent(user_input):
    # FASE 1: ESTRAZIONE RIGIDISSIMA
    ext_prompt = f"""Analizza: '{user_input}'. 
    REGOLE:
    - ADD: nome, qta, True (SOLO se c'è una data o dice 'scade oggi'). Altrimenti scrivi False.
    - PREF: estrai solo allergie/diete reali. Se l'utente dice 'no' o 'tutto ok', NON scrivere PREF.
    Scrivi solo le righe ADD o PREF."""
    
    raw_ext = llm.invoke(ext_prompt).content
    for line in raw_ext.split("\n"):
        if "ADD:" in line:
            parts = line.split("ADD:")[-1].split(",")
            if len(parts) >= 1:
                tool_pantry(parts[0], parts[1] if len(parts)>1 else "?", parts[2] if len(parts)>2 else "False")
        if "PREF:" in line:
            tool_pref(line.split("PREF:")[-1].strip())

    # FASE 2: RISPOSTA (OBBLIGO DI RICETTE SE L'UTENTE DICE NO)
    p_status = ", ".join([f"{i.nome}({i.quantita}, scad:{i.in_scadenza})" for i in st.session_state.pantry])
    pref_status = ", ".join(st.session_state.profile.vincoli_salute)
    
    chat_prompt = f"""Sei l'assistente Chef. 
    DISPENSA: {p_status}
    VINCOLI: {pref_status}
    
    REGOLE:
    1. Se l'utente dice "no", "tutto a posto", "confermo" o simili, DEVI SMETTERE di fare domande.
    2. In quel caso, PROPONI IMMEDIATAMENTE 3 RICETTE DETTAGLIATE usando gli ingredienti in dispensa.
    3. Rispetta i vincoli (vegano, celiaco, ecc.) se presenti.
    4. Usa gli ingredienti con scadenza True come priorità.

    Messaggio utente: {user_input}
    Risposta:"""
    
    return llm.invoke(chat_prompt).content
