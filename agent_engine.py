import os, re
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools import tool_pantry, tool_pref

load_dotenv()
llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

def run_chef_agent(user_input):
    # --- FASE 1: ESTRAZIONE RIGIDA ---
    # Obblighiamo l'AI a non inventare scadenze
    ext_prompt = f"""Analizza: '{user_input}'. 
    REGOLE ESTRAZIONE:
    1. Per ogni cibo scrivi: ADD: nome, quantita, scadenza
    2. SCADENZA: Scrivi 'True' SOLO se l'utente indica una data vicina o dice 'scade oggi/a breve'. 
       In TUTTI gli altri casi (anche se è in frigo), scrivi 'False'.
    3. VINCOLI: Se vedi allergie, celiachia o diete (vegano), scrivi: PREF: testo.
    
    Rispondi solo con le righe ADD o PREF."""
    
    raw_ext = llm.invoke(ext_prompt).content
    for line in raw_ext.split("\n"):
        if "ADD:" in line:
            parts = line.split("ADD:")[-1].split(",")
            if len(parts) >= 1:
                tool_pantry(parts[0], parts[1] if len(parts)>1 else "?", parts[2] if len(parts)>2 else "False")
        if "PREF:" in line:
            tool_pref(line.split("PREF:")[-1].strip())

    # --- FASE 2: RAGIONAMENTO E RISPOSTA ---
    p_status = ", ".join([f"{i.nome}({i.quantita}, scad:{i.in_scadenza})" for i in st.session_state.pantry])
    pref_status = ", ".join(st.session_state.profile.vincoli_salute)
    
    chat_prompt = f"""Sei l'assistente Chef. 
    DISPENSA ATTUALE: {p_status}
    VINCOLI ALIMENTARI: {pref_status}
    
    REGOLE DI RISPOSTA:
    1. Se mancano quantita (?) o scadenze per gli ingredienti principali, chiedile.
    2. Se l'utente menziona CELIACI o VEGANI, segnali nelle PREFERENZE e proponi SOLO ricette adatte (es. senza glutine, senza derivati animali).
    3. Solo se hai tutto, proponi 3 RICETTE DETTAGLIATE.
    4. Usa un tono professionale ma amichevole.
    
    Messaggio utente: {user_input}"""
    
    return llm.invoke(chat_prompt).content
