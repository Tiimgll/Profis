# python 3.9.13
# python-telegram-bot==13.7
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime, timedelta

tasks = {}

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    update.message.reply_text(f'Привет, {user_name}! Я бот-органайзер. Чтобы узнать как работает бот, используйте команду /help.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Этот бот поможет вам организовать ваши задачи. Используйте команду /add для добавления задачи и /tasks для просмотра задач.')

def add_task(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    task_args = context.args
    if len(task_args) >= 2:
        task_text = ' '.join(task_args[:-1])
        remind_time = task_args[-1]
        try:
            remind_time = timedelta(minutes=int(remind_time))
            remind_at = datetime.now() + remind_time
            remind_at_str = remind_at.strftime('%Y-%m-%d %H:%M:%S')
            if user_id not in tasks:
                tasks[user_id] = []
            tasks[user_id].append({'text': task_text, 'remind_at': remind_at_str})
            update.message.reply_text(f'Задача добавлена: {task_text}. Напомню вам в {remind_at_str}')
            context.job_queue.run_once(send_reminder, remind_time.seconds, context={'user_id': user_id, 'text': task_text})
        except ValueError:
            update.message.reply_text('Некорректное время.')
    else:
        update.message.reply_text('Пожалуйста, укажите текст задачи и время напоминания после команды /add.')

def send_reminder(context: CallbackContext) -> None:
    user_id = context.job.context['user_id']
    task_text = context.job.context['text']
    context.bot.send_message(chat_id=user_id, text=f'Напоминаю: {task_text}')

def show_tasks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in tasks and tasks[user_id]:
        task_list = '\n'.join([f"{task['text']} (напомнить в {task['remind_at']})" for task in tasks[user_id]])
        update.message.reply_text(f'Ваши задачи:\n{task_list}')
    else:
        update.message.reply_text('У вас нет задач.')

def main() -> None:
    updater = Updater("your-token")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("add", add_task, pass_args=True))
    dp.add_handler(CommandHandler("tasks", show_tasks))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
