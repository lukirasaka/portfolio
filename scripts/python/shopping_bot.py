from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import os

ORDERS_FILE = "orders.txt"
PRICE_PER_GRAM = 1.9
PRICE_FOR_1KG = 1450.0

def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "Vítejte v našem objednávkovém systému!\n\n"
        "📋 Použijte příkaz /menu k zobrazení nabídky.\n"
        "📩 Po výběru zadejte své kontaktní údaje, abychom vás mohli kontaktovat.\n\n"
        "Pokud máte jakékoliv dotazy, napište nám!\n\n"
        "Příkaz /menu pro zobrazení nabídky."
    )
    update.message.reply_text(welcome_message)

def menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Zelený", callback_data='zeleny')],
        [InlineKeyboardButton("Bílý", callback_data='bily')],
        [InlineKeyboardButton("Červený", callback_data='cerveny')],
        [InlineKeyboardButton("Mix", callback_data='mix')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Vyberte si z nabídky:", reply_markup=reply_markup)

def show_breeds(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    breeds = [
        [InlineKeyboardButton("Maeng Da", callback_data=f"{query.data}_maengda")],
        [InlineKeyboardButton("Dragon", callback_data=f"{query.data}_dragon")],
        [InlineKeyboardButton("Borneo", callback_data=f"{query.data}_borneo")]
    ]
    reply_markup = InlineKeyboardMarkup(breeds)
    query.edit_message_text(text="Vyberte druh:", reply_markup=reply_markup)

def show_weights(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    try:
        category, breed = query.data.split("_", 1)
    except ValueError:
        query.edit_message_text(text="Error processing your selection. Please try again.")
        return

    context.user_data['selection'] = {
        "category": category.capitalize(),
        "breed": breed.capitalize()
    }

    weights = [
        [InlineKeyboardButton("50g", callback_data=f"{query.data}_50")],
        [InlineKeyboardButton("100g", callback_data=f"{query.data}_100")],
        [InlineKeyboardButton("250g", callback_data=f"{query.data}_250")],
        [InlineKeyboardButton("500g", callback_data=f"{query.data}_500")],
        [InlineKeyboardButton("1kg", callback_data=f"{query.data}_1000")]
    ]
    reply_markup = InlineKeyboardMarkup(weights)
    query.edit_message_text(text="Vyberte hmotnost produktu:", reply_markup=reply_markup)

def handle_weight_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    try:
        category, breed, weight = query.data.split("_", 2)
    except ValueError:
        query.edit_message_text(text="Vyskytla se chyba při příjímání Vašeho požadavku. Prosíme, opakujte požadavek znova.")
        return

    weight_grams = int(weight) if weight.isdigit() else 0
    if weight_grams == 1000:
        price = PRICE_FOR_1KG
    else:
        price = weight_grams * PRICE_PER_GRAM

    context.user_data['order'] = {
        "category": category.capitalize(),
        "breed": breed.capitalize(),
        "weight": f"{weight_grams}g",
        "price": f"{price:.2f} Kč"
    }

    query.edit_message_text(
        text=f"Děkujeme! Vaše objednávka: {category.capitalize()} - {breed.capitalize()}, {weight_grams}g, Cena: {price:.2f} Kč.\n\n"
             "Prosím, napište své kontaktní údaje (např. telefonní číslo nebo e-mail):"
    )
    context.user_data['awaiting_contact'] = True

def save_contact(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('awaiting_contact'):
        contact_info = update.message.text
        order = context.user_data.get('order', {})
        if order:
            order_text = (
                f"Category: {order['category']}, Breed: {order['breed']}, Weight: {order['weight']}, "
                f"Price: {order['price']}, Contact: {contact_info}\n"
            )
            with open(ORDERS_FILE, "a") as file:
                file.write(order_text)
                file.flush()
            update.message.reply_text("Děkujeme, ozveme se Vám co nejdříve.")
        else:
            update.message.reply_text("Chybí data objednávky, prosíme, zkuste to znovu.")
        context.user_data['awaiting_contact'] = False
    else:
        update.message.reply_text("Pro pokračování prosím napište /menu.")

def fallback(update: Update, context: CallbackContext) -> None:
    if not context.user_data.get('awaiting_contact'):
        update.message.reply_text("Použijte /menu pro objednání.")

def main() -> None:
    updater = Updater("API_KEY", use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("menu", menu))
    dispatcher.add_handler(CallbackQueryHandler(show_breeds, pattern='^(zeleny|bily|cerveny|mix)$'))
    dispatcher.add_handler(CallbackQueryHandler(show_weights, pattern='^(zeleny|bily|cerveny|mix)_(maengda|dragon|borneo)$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_weight_selection, pattern='^(zeleny|bily|cerveny|mix)_(maengda|dragon|borneo)_(50|100|250|500|1000)$'))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, save_contact))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, fallback))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
