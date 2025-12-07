main.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json, os

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot de tareas activo ✅\n\n"
        "Comandos:\n"
        "/add tarea | fecha\n"
        "/list\n"
        "/done tarea"
    )

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace("/add", "").strip()
    if "|" not in text:
        await update.message.reply_text("Formato: /add tarea | fecha")
        return
    task, date = text.split("|")
    tasks = load_tasks()
    tasks.append({"task": task.strip(), "date": date.strip(), "done": False})
    save_tasks(tasks)
    await update.message.reply_text("✅ Tarea guardada")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    pending = [t for t in tasks if not t["done"]]

    if not pending:
        await update.message.reply_text("No tienes tareas pendientes 🎉")
        return

    msg = "📌 Tareas pendientes:\n\n"
    for t in pending:
        msg += f"- {t['task']} (📅 {t['date']})\n"

    await update.message.reply_text(msg)

async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.replace("/done", "").strip()
    tasks = load_tasks()
    for t in tasks:
        if t["task"].lower() == name.lower():
            t["done"] = True
            save_tasks(tasks)
            await update.message.reply_text("✅ Completada")
            return
    await update.message.reply_text("⚠️ No encontrada")

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_task))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("done", done_task))

    print("Bot activo...")
    app.run_polling()
