<div align="center">
    <h1 id="titulo">Loto_Facil_API_Telegram</h1>
    <p>Um bot do Telegram para consultar resultados de concursos da Lotofácil. Oferece uma interface interativa e fácil de usar para acessar os detalhes dos concursos passados e do próximo concurso.</p>
</div>

## Índice

1. [Visão Geral](#visao-geral)
2. [Instalação](#instalacao)
3. [Como Usar](#como-usar)
4. [Exemplos](#exemplos)
5. [Scripts](#scripts)
6. [Contribuições](#contribuicoes)
7. [Licença](#licenca)

### Visão Geral

O **LotoBot** é um bot do Telegram construído em Python que permite aos usuários consultar os resultados dos concursos da Lotofácil diretamente no Telegram. O bot fornece recursos interativos, como botões para visualizar os 5 últimos concursos com suas respectivas datas e a capacidade de consultar informações completas sobre qualquer concurso, utilizando o número do concurso.

O bot integra-se a uma API pública para buscar os dados mais recentes e os salva em um arquivo CSV local. O arquivo CSV é utilizado para mostrar os resultados completos dos concursos quando o número do concurso é fornecido.

### Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/fabianofwp19/Tele_bot.git
    ```

2. Instale as dependências necessárias:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure o seu arquivo `.env` com a chave da API do Telegram:

    ```bash
    API_KEY=sua_chave_api_do_telegram
    ```

4. Execute o bot:

    ```bash
    python telegram.py
    ```

### Como Usar

1. **Iniciar o Bot**: Envie `/start` para iniciar o bot no seu chat do Telegram.
2. **Consultar os Últimos Concursos**: Utilize o botão interativo "Consultar Concurso" para visualizar os 5 últimos concursos com suas respectivas datas.
3. **Consultar um Concurso Específico**: Envie o comando `/concurso <número>` para obter detalhes completos de um concurso específico (exemplo: `/concurso 3319`).
4. **Comandos Interativos**: O bot responde a interações de botões, permitindo que você explore os recursos de maneira simples e eficaz.

### Exemplos

#### Exemplo 1: Últimos 5 Concursos

Quando você clica no botão **Consultar Concurso**, o bot exibe os últimos 5 concursos com suas datas.

**Exemplo de resposta**:

🔎 *Últimos 5 Concursos:*

🎯 Concurso 3319 - 13/02/2025<br>
🎯 Concurso 3318 - 12/02/2025<br>
🎯 Concurso 3317 - 11/02/2025<br>
🎯 Concurso 3316 - 10/02/2025<br>
🎯 Concurso 3315 - 08/02/2025<br>


#### Exemplo 2: Detalhes de um Concurso

Quando você envia o comando `/concurso 3319`, o bot retorna detalhes como o local, as dezenas sorteadas, as premiações e mais:

**Exemplo de resposta**:

🎉 Detalhes do Concurso 3319 - 13/02/2025

📍 Local: ESPAÇO DA SORTE em SÃO PAULO, SP<br>
💰 Valor Arrecadado: R$ 19651002.00<br>
🔢 Dezenas Sorteadas:<br>
 01, 04, 05, 06, 07, 14, 15, 16, 17, 19, 20, 21, 22, 23, 25

🏆 Premiações: 
  - 15 acertos: 15 acertos (Ganhadores: 1, Premio: 1934268.46)
  - 14 acertos:  14 acertos (Ganhadores: 210, Premio: 1931.3)
  - 13 acertos:  13 acertos (Ganhadores: 6302, Premio: 30.0)
  - 12 acertos:  12 acertos (Ganhadores: 83337, Premio: 12.0)
  - 11 acertos:  11 acertos (Ganhadores: 493205, Premio: 6.0)


### Scripts

#### Script 1: Consulta de Resultados e Exibição dos Detalhes

Este script permite que você consulte os concursos e veja os detalhes de um concurso específico de maneira formatada e colorida no terminal. Ele utiliza a biblioteca **pandas** para ler o arquivo CSV que contém os dados dos concursos e apresenta as informações de maneira organizada.

```python
import pandas as pd
from tabulate import tabulate
from colorama import Fore, Style

# Função para buscar o concurso pelo número
def buscar_concurso(concurso_num):
    try:
        df = pd.read_csv("resultado_loto.csv", dtype={"Concurso": str})
        
        # Filtra o concurso desejado
        concurso = df[df['Concurso'] == str(concurso_num)]
        
        if concurso.empty:
            print(Fore.RED + f"O concurso {concurso_num} não foi encontrado no arquivo." + Style.RESET_ALL)
            return None
        
        return concurso
    except FileNotFoundError:
        print(Fore.RED + "Arquivo CSV não encontrado. Por favor, gere o CSV primeiro." + Style.RESET_ALL)
        return None

# Função para exibir os últimos concursos
def ultimos_concursos():
    try:
        df = pd.read_csv("resultado_loto.csv", dtype={"Concurso": str})
        ultimos = df[['Concurso', 'Data']].tail(5)  # Exibe os últimos 5 concursos
        print(Fore.YELLOW + "\nÚltimos Concursos:")
        print(tabulate(ultimos, headers=["Concurso", "Data"], tablefmt="fancy_grid", numalign="center") + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + "Arquivo CSV não encontrado. Por favor, gere o CSV primeiro." + Style.RESET_ALL)

# Função para exibir os dados do concurso de forma colorida
def exibir_dados_concurso(concurso):
    if concurso is None:
        return
    
    concurso_data = concurso.iloc[0]  # Acessa a primeira linha do dataframe, que contém o concurso
    
    print(Fore.GREEN + f"\nDetalhes do Concurso {concurso_data['Concurso']} - {concurso_data['Data']}" + Style.RESET_ALL)
    print(Fore.CYAN + f"Local: {concurso_data['Local']}" + Style.RESET_ALL)
    print(Fore.MAGENTA + f"Valor Arrecadado: R$ {concurso_data['ValorArrecadado']:.2f}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Dezenas Sorteadas: {concurso_data['Dezenas']}" + Style.RESET_ALL)
    print(Fore.BLUE + f"Premiações: {concurso_data['Premiacoes']}" + Style.RESET_ALL)
    print(Fore.RED + f"Acumulou: {concurso_data['Acumulou']}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Próximo Concurso: {concurso_data['ProximoConcurso']} - {concurso_data['DataProximoConcurso']}" + Style.RESET_ALL)
    print(Fore.CYAN + f"Valor Estimado Próximo Concurso: R$ {concurso_data['ValorEstimadoProximoConcurso']:.2f}" + Style.RESET_ALL)

# Função principal que integra tudo
def main():
    ultimos_concursos()
    
    concurso_num = input(Fore.YELLOW + "\nDigite o número do concurso que você deseja consultar: " + Style.RESET_ALL)
    concurso = buscar_concurso(concurso_num)
    
    if concurso is not None:
        exibir_dados_concurso(concurso)

if __name__ == "__main__":
    main()


"""Script 2: Importação dos Dados da API e Armazenamento no CSV
Este script busca os dados da Lotofácil a partir de uma API pública e os salva em um arquivo CSV. Ele também lida com a duplicação de dados ao adicionar novos concursos, para garantir que não haja registros duplicados no CSV."""

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
    print(f"Dados salvos em {CSV_FILE}")

# Executa o código
if __name__ == "__main__":
    dados = buscar_dados() 
    salvar_dados(dados)








