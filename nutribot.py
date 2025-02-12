from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackContext, Dispatcher
import logging
import os
from flask import Flask, request

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do Bot
TOKEN = "8049712315:AAHENfpd2N5sQXw4DOwxtFeIOsAvK7AZO0Y"
PORT = int(os.environ.get("PORT", 5000))
bot = Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot, None, use_context=True)

# Banco de dados de receitas
receitas = {
    "cafe": {
        "nome": "Crepioca de Frango",
        "ingredientes": [
            "1 ovo",
            "2 colheres de sopa de goma de tapioca",
            "50g de frango desfiado",
            "Sal e temperos a gosto"
        ],
        "preparo": "Misture o ovo com a tapioca e leve a uma frigideira aquecida. Adicione o frango desfiado e deixe dourar dos dois lados."
    },
    "almoco": {
        "nome": "Frango Grelhado com Salada",
        "ingredientes": [
            "100g de peito de frango",
            "Folhas verdes (alface, rúcula, agrião)",
            "Tomate cereja cortado ao meio",
            "1 colher de sopa de azeite"
        ],
        "preparo": "Tempere o frango com sal e grelhe até dourar. Monte a salada com as folhas verdes e tomate, temperando com azeite."
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
        "preparo": "Cozinhe a abóbora até ficar macia, bata no liquidificador e misture com o frango refogado com alho. Tempere a gosto."
    }
}

# Função para iniciar o bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Olá! Eu sou o NutriBot 🤖. Digite /menu para ver as opções de refeições ou /receita seguido do tipo de refeição para ver o modo de preparo. Exemplo: /receita cafe")

# Função para exibir o menu de refeições
def menu(update: Update, context: CallbackContext) -> None:
    mensagem = "Escolha o tipo de refeição:\n" \
              "/cafe - Café da manhã ☕\n" \
              "/almoco - Almoço 🍽️\n" \
              "/lanche - Lanche da tarde 🥪\n" \
              "/jantar - Jantar 🌙"
    update.message.reply_text(mensagem)

# Função para enviar a receita detalhada
def receita(update: Update, context: CallbackContext) -> None:
    args = context.args
    if not args:
        update.message.reply_text("Por favor, informe o tipo de refeição. Exemplo: /receita cafe")
        return
    
    tipo = args[0].lower()
    if tipo in receitas:
        r = receitas[tipo]
        mensagem = f"🍽️ {r['nome']}\n\nIngredientes:\n- " + "\n- ".join(r['ingredientes']) + "\n\nModo de Preparo:\n" + r['preparo']
        update.message.reply_text(mensagem)
    else:
        update.message.reply_text("Tipo de refeição não encontrado. Use: /receita cafe, /receita almoco, /receita lanche ou /receita jantar.")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("menu", menu))
    dispatcher.add_handler(CommandHandler("receita", receita, pass_args=True))
    app.run(host="0.0.0.0", port=PORT)

