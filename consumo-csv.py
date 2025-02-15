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
