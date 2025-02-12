from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import random

# Configuração do Bot
TOKEN = "8049712315:AAHENfpd2N5sQXw4DOwxtFeIOsAvK7AZO0Y"
bot = Bot(token=TOKEN)

# Lista de sugestões de refeições e receitas detalhadas
receitas = {
    "cafe": {
        "nome": "Crepioca com Frango",
        "ingredientes": [
            "1 ovo",
            "2 colheres de sopa de goma de tapioca",
            "50g de frango desfiado",
            "Sal e temperos a gosto"
        ],
        "preparo": "Misture o ovo com a goma de tapioca até obter uma massa homogênea. Despeje em uma frigideira quente e adicione o frango desfiado. Cozinhe por 2-3 minutos de cada lado."
    },
    "almoco": {
        "nome": "Frango Grelhado com Salada",
        "ingredientes": [
            "100g de peito de frango",
            "Folhas verdes (alface, rúcula, agrião)",
            "Tomate cereja cortado ao meio",
            "1 colher de sopa de azeite"
        ],
        "preparo": "Tempere o frango com sal e temperos a gosto. Grelhe até dourar. Monte a salada com folhas verdes, tomate cereja e regue com azeite."
    },
    "lanche": {
        "nome": "Shake Proteico",
        "ingredientes": [
            "200ml de leite desnatado",
            "1 banana",
            "1 colher de sopa de aveia",
            "1 dose de whey protein (opcional)"
        ],
        "preparo": "Bata todos os ingredientes no liquidificador até obter uma mistura homogênea. Sirva gelado."
    },
    "jantar": {
        "nome": "Sopa de Abóbora com Frango",
        "ingredientes": [
            "200g de abóbora cabotiá",
            "100g de peito de frango desfiado",
            "1 dente de alho",
            "Sal e temperos a gosto"
        ],
        "preparo": "Cozinhe a abóbora até ficar macia. Bata no liquidificador até obter um creme. Refogue o alho, adicione o frango desfiado e misture com o creme de abóbora. Tempere a gosto."
    }
}

# Função para iniciar o bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Olá! Eu sou o NutriBot 🤖. Digite /menu para ver as opções de refeições ou /receita seguido do tipo de refeição para ver o modo de preparo. Exemplo: /receita cafe")

# Função para sugerir refeições
def sugerir_refeicao(update: Update, context: CallbackContext) -> None:
    mensagem = "Escolha o tipo de refeição:\n" \
              "/cafe - Café da manhã ☕\n" \
              "/almoco - Almoço 🍽️\n" \
              "/lanche - Lanche da tarde 🥪\n" \
              "/jantar - Jantar 🌙"
    update.message.reply_text(mensagem)

# Função para enviar receitas detalhadas
def enviar_receita(update: Update, context: CallbackContext) -> None:
    tipo_refeicao = " ".join(context.args).strip().lower()
    if tipo_refeicao in receitas:
        receita = receitas[tipo_refeicao]
        mensagem = f"🍽️ {receita['nome']}\n\nIngredientes:\n- " + "\n- ".join(receita['ingredientes']) + "\n\nModo de Preparo:\n" + receita['preparo']
        update.message.reply_text(mensagem)
    else:
        update.message.reply_text("Opção inválida. Use /receita cafe, /receita almoco, /receita lanche ou /receita jantar.")

# Configuração do Bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", sugerir_refeicao))
    dp.add_handler(CommandHandler("receita", enviar_receita, pass_args=True))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
