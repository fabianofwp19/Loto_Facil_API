import telebot
import time
import pandas as pd
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.env_loader import load_env
from utils.bot_starter import iniciar_bot

# Carregar API Key
API_KEY = load_env()
bot = telebot.TeleBot(API_KEY)

# Função para buscar o concurso no CSV
def buscar_concurso(concurso_num):
    try:
        df = pd.read_csv("resultado_loto.csv", dtype={"Concurso": str})
        
        # Filtra o concurso desejado
        concurso = df[df['Concurso'] == str(concurso_num)]
        
        if concurso.empty:
            return None
        
        return concurso
    except FileNotFoundError:
        return None

# Função para exibir os dados do concurso de forma bonita
def exibir_dados_concurso(concurso):
    if concurso is None:
        return "⚠️ Concurso não encontrado."
    
    concurso_data = concurso.iloc[0]  # Acessa a primeira linha do dataframe, que contém o concurso
    
    # Montando a resposta com formatação mais bonita
    resultado = (
        f"🎉 *Detalhes do Concurso {concurso_data['Concurso']}* - {concurso_data['Data']}\n\n"
        f"📍 *Local:* {concurso_data['Local']}\n"
        f"💰 *Valor Arrecadado:* R$ {concurso_data['ValorArrecadado']:.2f}\n"
        f"🔢 *Dezenas Sorteadas:*\n {concurso_data['Dezenas']}\n\n"
        f"🏆 *Premiações:* \n"
        f"  - 15 acertos: {concurso_data['Premiacoes'].split(';')[0]}\n"
        f"  - 14 acertos: {concurso_data['Premiacoes'].split(';')[1]}\n"
        f"  - 13 acertos: {concurso_data['Premiacoes'].split(';')[2]}\n"
        f"  - 12 acertos: {concurso_data['Premiacoes'].split(';')[3]}\n"
        f"  - 11 acertos: {concurso_data['Premiacoes'].split(';')[4]}\n\n"
        f"🔴 *Acumulou?* {'Sim' if concurso_data['Acumulou'] == 'True' else 'Não'}\n\n"
        f"🎯 *Próximo Concurso:* {concurso_data['ProximoConcurso']} - {concurso_data['DataProximoConcurso']}\n"
        f"💸 *Valor Estimado Próximo Concurso:* R$ {concurso_data['ValorEstimadoProximoConcurso']:.2f}"
    )
    
    return resultado

# Função para exibir os últimos 5 concursos (os mais recentes)
def exibir_ultimos_concursos():
    try:
        df = pd.read_csv("resultado_loto.csv", dtype={"Concurso": str})
        
        # Ordena os concursos pela data (decrescente) e pega os 5 últimos
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')  # Converte a coluna 'Data' para datetime
        ultimos_concursos = df[['Concurso', 'Data']].sort_values(by='Data', ascending=False).head(5)
        
        resultado = "🔎 *Últimos 5 Concursos:*\n\n"
        
        for _, concurso in ultimos_concursos.iterrows():
            resultado += (
                f"🎯 Concurso {concurso['Concurso']} - {concurso['Data'].strftime('%d/%m/%Y')}\n"
            )
        
        return resultado
    except FileNotFoundError:
        return "⚠️ Arquivo de resultados não encontrado."

# /start
@bot.message_handler(commands=["start"])
def start_command(message):
    text = (   
        "🤖 **Bem-vindo ao Meu Primeiro Bot!**\n\n"
        "Estou aqui para tornar sua experiência com logs na nuvem mais simples, rápida e eficiente.\n\n"
        "Com recursos interativos e fáceis de usar, você pode gerenciar informações e consultar logs sem complicação.\n\n"
        "🚀 **O que eu posso fazer por você?**\n"
        "- 📌 **Consultas Rápidas**: Acesse logs instantaneamente com um clique.\n"
        "- 🔒 **Segurança e Confiabilidade**: Gerencie suas informações com total segurança.\n"
        "- ⚡ **Facilidade de Uso**: Interface intuitiva para uma experiência fluida e prática.\n\n"
        "👨‍💻 Criado por [fabianofwp19](https://github.com/fabianofwp19). Faça parte da comunidade e explore todas as possibilidades!"
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Sobre", callback_data="sobre"))
    markup.add(InlineKeyboardButton("Comandos", callback_data="comandos"))
    markup.add(InlineKeyboardButton("Consultar Concurso", callback_data="consultar_concurso"))
    markup.add(InlineKeyboardButton("GitHub Oficial", url="https://github.com/fabianofwp19"), InlineKeyboardButton("Criador", url="https://t.me/Thazfwp_bot"))

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "sobre":
        sobre_markup = InlineKeyboardMarkup()
        sobre_markup.add(InlineKeyboardButton("Voltar", callback_data="voltar"))
        sobre_text = (
            "Com este bot, você tem a liberdade de criar e personalizar sua própria experiência. 🔧\n\n"
            "🎯 **Principais Recursos**:\n"
            "- Adicione novas funções conforme necessário.\n"
            "- Crie e personalize botões interativos.\n"
            "- Modifique textos, mensagens e crie respostas exclusivas para os usuários.\n\n"
            "💡 Este bot é altamente flexível, permitindo que você adapte as interações e funcionalidades ao seu gosto!\n"
            "Seja para automatizar processos, facilitar consultas ou criar comandos personalizados, o Telegram_Interactive_Button faz tudo isso e muito mais!\n\n"
            "🚀 **Por que escolher o Telegram_Interactive_Button?**\n"
            "- Rápido e eficiente na recuperação de logs e informações.\n"
            "- Fácil de personalizar e expandir.\n"
            "- Perfeito para integrar funções na nuvem às tarefas diárias.\n\n"
            "Orgulhosamente criado por [fabianofwp19!](https://github.com/fabianofwp19). Explore e descubra o poder da personalização!"
        )
        bot.edit_message_text(sobre_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=sobre_markup, parse_mode='Markdown')

    elif call.data == "comandos":
        comandos_markup = InlineKeyboardMarkup()
        comandos_markup.add(InlineKeyboardButton("/start", callback_data="start_command"))
        comandos_markup.add(InlineKeyboardButton("/comandos", callback_data="comandos_comando"))
        comandos_markup.add(InlineKeyboardButton("Voltar", callback_data="voltar"))
        bot.edit_message_text("Aqui estão os comandos disponíveis:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=comandos_markup)

    elif call.data == "consultar_concurso":
        bot.send_message(call.message.chat.id, "Aqui estão os **últimos 5 concursos**:\n")
        ultimos_concursos = exibir_ultimos_concursos()
        bot.send_message(call.message.chat.id, ultimos_concursos)
        bot.send_message(call.message.chat.id, "\nPara consultar os detalhes de um concurso, digite o comando `/concurso <número>`, por exemplo: `/concurso 3000`.")

    elif call.data == "voltar":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        start_command(call.message)

# /comandos
@bot.message_handler(commands=['comandos'])
def lista_comandos(message):
    response = (
        "📋 *Comandos Disponíveis:*\n\n"
        "`/start` - Inicia o bot e exibe os módulos disponíveis.\n"
        "`/comandos` - Mostra esta lista de comandos.\n"
        "`/concurso <número>` - Consulta as informações de um concurso específico.\n"
    )

    bot.reply_to(message, response, parse_mode='Markdown')

# /concurso
@bot.message_handler(commands=['concurso'])
def consultar_concurso(message):
    try:
        # Obtém o número do concurso após o comando
        concurso_num = message.text.split()[1]
        
        concurso = buscar_concurso(concurso_num)
        
        if concurso is None:
            bot.reply_to(message, "⚠️ Concurso não encontrado.")
        else:
            dados_concurso = exibir_dados_concurso(concurso)
            bot.reply_to(message, dados_concurso, parse_mode='Markdown')
    except IndexError:
        bot.reply_to(message, "❗ Para consultar um concurso, use o formato `/concurso <número>`, por exemplo: `/concurso 3000`.")

if __name__ == '__main__':
    iniciar_bot(bot)
