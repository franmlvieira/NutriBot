from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, JobQueue
import datetime
import random

# Configuração do Bot
TOKEN = "8049712315:AAHENfpd2N5sQXw4DOwxtFeIOsAvK7AZO0Y"
bot = Bot(token=TOKEN)

# Lista de sugestões de refeições
refeicoes = {
    "cafe": ["Crepioca com frango", "Pão integral com ovos", "Bolo proteico de banana"],
    "almoco": ["Frango grelhado com salada", "Peixe assado com legumes", "Arroz integral com carne magra"],
    "lanche": ["Shake proteico", "Iogurte com aveia", "Pudim de chia com whey"],
    "jantar": ["Omelete de vegetais", "Sopa de abóbora com frango", "Wrap de frango com salada"]
}

# Função para iniciar o bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Olá! Eu sou o NutriBot 🤖. Vou te ajudar com sua alimentação! Digite /menu para ver as opções.")

# Função para sugerir refeições
def sugerir_refeicao(update: Update, context: CallbackContext) -> None:
    mensagem = "Escolha o tipo de refeição:\n"               "/cafe - Café da manhã ☕\n"               "/almoco - Almoço 🍽️\n"               "/lanche - Lanche da tarde 🥪\n"               "/jantar - Jantar 🌙"
    update.message.reply_text(mensagem)

# Função para enviar sugestões baseadas na refeição escolhida
def enviar_sugestao(update: Update, context: CallbackContext) -> None:
    tipo_refeicao = update.message.text.strip("/")
    if tipo_refeicao in refeicoes:
        sugestao = random.choice(refeicoes[tipo_refeicao])
        update.message.reply_text(f"Sugestão para {tipo_refeicao}: {sugestao}")
    else:
        update.message.reply_text("Opção inválida. Use /menu para ver as opções.")

# Função para lembretes automáticos
def enviar_lembrete(context: CallbackContext) -> None:
    chat_id = context.job.context
    context.bot.send_message(chat_id, text="Hora da refeição! Veja opções com /menu")

# Configuração dos lembretes
def configurar_lembretes(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    job_queue = context.job_queue
    horarios = [(7, 0), (12, 0), (15, 0), (19, 0)]  # Café, almoço, lanche e jantar
    
    for hora, minuto in horarios:
        tempo = datetime.time(hour=hora, minute=minuto)
        job_queue.run_daily(enviar_lembrete, tempo, context=chat_id)
    
    update.message.reply_text("Lembretes configurados para suas refeições! 🍽️")

# Configuração do Bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", sugerir_refeicao))
    dp.add_handler(CommandHandler("cafe", enviar_sugestao))
    dp.add_handler(CommandHandler("almoco", enviar_sugestao))
    dp.add_handler(CommandHandler("lanche", enviar_sugestao))
    dp.add_handler(CommandHandler("jantar", enviar_sugestao))
    dp.add_handler(CommandHandler("configurar", configurar_lembretes))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
