import requests
import pandas as pd
import os

URL = "https://loteriascaixa-api.herokuapp.com/api/lotofacil"
CSV_FILE = "resultado_loto.csv"

# Função para buscar dados
def buscar_dados():
    try: 
        response = requests.get(URL)
        if response.status_code == 200: 
            return response.json()
        else:
            print(f"Erro ao acessar a API: {response.status_code}")
            return None       
    except Exception as e: 
        print(f"Erro ao acessar o banco de dados: {e}")
        return None
    
# Função para salvar os dados
def salvar_dados(dados):
    if not dados: 
        print("Nenhum dado para salvar")
        return 
    
    # Estrutura dos dados com novos campos
    listas_resultados = []
    for concurso in dados:
        premiacoes = concurso.get("premiacoes", [])
        premiacoes_info = "; ".join([f"{p['descricao']} (Ganhadores: {p['ganhadores']}, Premio: {p['valorPremio']})" for p in premiacoes])
        
        listas_resultados.append({
            "Concurso": concurso.get("concurso"),
            "Data": concurso.get("data"),
            "Local": concurso.get("local"),
            "ValorArrecadado": concurso.get("valorArrecadado"),
            "Dezenas": ", ".join(concurso.get("dezenas", [])),
            "Premiacoes": premiacoes_info,
            "Acumulou": concurso.get("acumulou"),
            "ProximoConcurso": concurso.get("proximoConcurso"),
            "DataProximoConcurso": concurso.get("dataProximoConcurso"),
            "ValorAcumuladoConcurso_0_5": concurso.get("valorAcumuladoConcurso_0_5"),
            "ValorEstimadoProximoConcurso": concurso.get("valorEstimadoProximoConcurso")
        })
    
    df_novo = pd.DataFrame(listas_resultados)
    
    if os.path.exists(CSV_FILE):
        df_existente = pd.read_csv(CSV_FILE, dtype={"Concurso": str})
        df_final = pd.concat([df_existente, df_novo]).drop_duplicates(subset=["Concurso"], keep="last")
    else: 
        df_final = df_novo
        
    df_final.to_csv(CSV_FILE, index=False, encoding="utf-8-sig") 
    print(f"dados salvos em {CSV_FILE}")

# Executa o código
if __name__ == "__main__":
    dados = buscar_dados() 
    salvar_dados(dados)
