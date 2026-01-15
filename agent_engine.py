import re, os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools import tool_pantry, tool_pref

load_dotenv()

llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

SYSTEM_PROMPT = """Sei l'assistente Chef. Il tuo obiettivo è accompagnare l'utente in un percorso dialogico.

REGOLE STRINGENTI (Segui alla lettera):
1. Se l'utente nomina ingredienti, usa tool_pantry (Formato: Nome, Quantita, True/False). Se non sai la quantità o scadenza, scrivi 'non specificata' e 'False'.
2. NON PROPORRE RICETTE finché non hai chiesto e ottenuto la QUANTITÀ e la SCADENZA di ogni ingrediente.
3. NON ASSUMERE di avere ingredienti che l'utente non ha citato (es. melanzane, panna).
4. Se hai informazioni sufficienti, proponi esattamente 3 ricette includendo: Nome, Tempo, Ingredienti con dosi e Preparazione.
5. Usa tool_pref per allergie o gusti.

FORMATO RISPOSTA:
Thought: (riflessione)
Action: (tool_pantry o tool_pref o NONE)
Action Input: (input tool)
Final Answer: (la tua risposta all'utente)

User: {input}"""

def run_chef_agent(user_input):
    scratchpad = ""
    for i in range(10):
        full_prompt = f"{SYSTEM_PROMPT.format(input=user_input)}\n{scratchpad}"
        response = llm.invoke(full_prompt).content
        print(f"\n--- RAGIONAMENTO CICLO {i+1} ---\n{response}\n")

        if "Final Answer:" in response:
            return response.split("Final Answer:")[-1].strip()

        action = re.search(r"Action:\s*(\w+)", response)
        action_input = re.search(r"Action Input:\s*(.*)", response)

        if action and "NONE" not in action.group(1).upper():
            act_name = action.group(1).strip()
            act_in = action_input.group(1).strip() if action_input else ""
            
            if "pantry" in act_name.lower(): obs = tool_pantry(act_in)
            elif "pref" in act_name.lower(): obs = tool_pref(act_in)
            else: obs = "Errore tool."
            
            scratchpad += f"\nThought: {response}\nObservation: {obs}\n"
        else:
            return response.replace("Thought:", "").strip()
    return "L'agente è confuso. Prova a dare un comando semplice."
