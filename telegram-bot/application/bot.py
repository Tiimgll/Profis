import telebot
import sqlite3
import config

BOT_TOKEN = '6630545631:AAEHEPPCImjcgS6L3hKkhMTAB6RSR0eVcmw'
ADMIN_ID = 1943452091

bot = telebot.TeleBot(BOT_TOKEN)

def init_database():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  sender TEXT,
                  description TEXT,
                  fixed_date TEXT)''')
    conn.commit()
    conn.close()

init_database()

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("Сообщить о проблеме", callback_data='report_problem')
    keyboard.add(button1)
    bot.send_message(message.chat.id, "Добро пожаловать! Чтобы сообщить о проблеме, нажмите кнопку ниже.", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'report_problem':
        bot.answer_callback_query(callback_query_id=call.id, text="Введите описание проблемы.")
        bot.send_message(call.message.chat.id, "Пожалуйста, введите описание проблемы.")
        bot.register_next_step_handler(call.message, create_ticket)

def create_ticket(message):
    admin_id = ADMIN_ID
    bot.send_message(admin_id, f"Новая заявка от {message.from_user.first_name} {message.from_user.last_name}\nОписание: {message.text}")
    bot.send_message(message.chat.id, "Ваша заявка была успешно отправлена администратору.")

    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("INSERT INTO tickets (date, sender, description) VALUES (?,?,?)", (message.date, message.from_user.first_name + ' ' + message.from_user.last_name, message.text))
    conn.commit()
    conn.close()

def get_tickets():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tickets")
    tickets = c.fetchall()
    conn.close()
    return tickets

@bot.message_handler(commands=['tickets'])
def view_tickets(message):
    if message.chat.id == ADMIN_ID:
        tickets = get_tickets()
        for ticket in tickets:
            bot.send_message(message.chat.id, f"Заявка #{ticket[0]} от {ticket[1]}: {ticket[3]}\nОтправитель: {ticket[2]}\nДата исправления: {ticket[4]}")

def fix_ticket(ticket_id, message):  # Добавляем параметр message
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("UPDATE tickets SET fixed_date =? WHERE id =?", (message.date, ticket_id))
    conn.commit()
    conn.close()

@bot.message_handler(commands=['fix'])
def fix_ticket_command(message):
    if message.chat.id == ADMIN_ID:
        ticket_id = message.text.split()[1]
        fix_ticket(ticket_id, message)  # Передаем параметр message
        bot.send_message(message.chat.id, f"Заявка #{ticket_id} была отмечена как исправленная.")


@bot.message_handler(commands=['fix'])
def fix_ticket_command(message):
    if message.chat.id == ADMIN_ID:
        ticket_id = message.text.split()[1]
        fix_ticket(ticket_id)
        bot.send_message(message.chat.id, f"Заявка #{ticket_id} была отмечена как исправленная.")

if __name__ == '__main__':
    bot.polling()