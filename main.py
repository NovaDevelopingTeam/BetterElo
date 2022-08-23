from telethon import TelegramClient, Button
from telethon.events import NewMessage, CallbackQuery
from db import create_db
from ranking import Ranking
from leaderboard import Leaderboard
import sqlite3
import random
import time
import json

leaderboard_first_grade = Leaderboard(200)
leaderboard_second_grade = Leaderboard(200)

maintenance = [False, ""]

statuses = {}

ranking = Ranking(400, 650, 875, 1000, 1300, 1700)

create_db()
db = sqlite3.connect("betterelo.db")
c = db.cursor()

c.execute("SELECT telegram_id, first_grade_elo FROM betterelo ORDER BY first_grade_elo DESC LIMIT 200")
results = c.fetchall()
if results:
    for result in results:
        leaderboard_first_grade.add_user(result[0], result[1])
        leaderboard_first_grade.re_sort()

c.execute("SELECT telegram_id, second_grade_elo FROM betterelo ORDER BY second_grade_elo DESC LIMIT 200")
results = c.fetchall()
if results:
    for result in results:
        leaderboard_second_grade.add_user(result[0], result[1])
        leaderboard_second_grade.re_sort()

ranking_text = "QUALI SONO I RANK?\n\nBRONZO: 0-400 di elo\nARGENTO: 401-650 di elo\nORO: 651-875 di elo\nPLATINO: 876-1000 di elo\nDIAMANTE: 1001-1300 di elo\nCHAMPIONE: 1301-1700\nGRANDE CAMPIONE: >1700"
first_grade_text = "RISOLVI QUESTA EQUAZIONE, RICORDA:\nn/m frazione di n fratto m\nn:m divisione di n diviso m\nn*m moltiplicazione di n per m\nn**m potenza di n alla m\n\nSe il risultato e' impossibile scrivi: 'im'\nSe il risultato e' indeterminato scrivi: 'in'\nIn ogni altro caso scrivi solo il valore dell'incognita"


api_id = 123
api_hash = '12345678'

admin_id = 0

client = TelegramClient('anon', api_id, api_hash)

async def maintenance_on(message: str):
    global maintenance
    maintenance = [True, message]
    users = c.execute("SELECT telegram_id FROM langs").fetchall()
    for user in users:
        await client.send_message(int(user[0]), message)


@client.on(NewMessage)
async def handler(e):
    global maintenance
    db = sqlite3.connect("betterelo.db")
    c = db.cursor()
    if e.sender.id == admin_id:
        await e.reply("Benvenuto nel bot.", buttons=[[Button.inline("ANNUNCIO", "announcement"), Button.inline("NUOVA STAGIONE", "new_season")], [Button.inline("ATTIVA MANUTENZIONE", "maintenance_on")]])
    else:
        if maintenance[0] == True:
            await e.reply(maintenance[1])
            return
        try:
            status = statuses[str(e.sender.id)]
        except KeyError:
            print("")
        if status:
            if status.startswith("training_first_grade"):
                end_time = time.time()
                eq_id = int(status.split(" ")[1])
                start_time = float(status.split(" ")[2])
                eq = c.execute("SELECT * FROM equations WHERE id = ?", (eq_id,)).fetchone()
                eq_solutions = eq[2]
                eq_resolves = eq[4]
                eq_resolves_sum = 0
                resolve_media = 0.00
                for sol in eq_solutions:
                    if e.text == sol:
                        for soll in eq_resolves:
                            eq_resolves_sum += int(soll)
                        resolve_media = eq_resolves_sum / len(eq_resolves)
                        lang = c.execute("SELECT lang FROM langs WHERE telegram_id = ?" (e.sender.id,)).fetchone()[0]
                        f = json.load(open(f"{lang}.json", "r"))
                        await e.reply(f"Equazione Corretta! Il tuo tempo e' stato di {end_time - start_time} secondi, il tempo medio e' di: {resolve_media} secondi", buttons=[[Button.inline(f["utility"]["back"], "user_start")]])
                        return
                await e.reply("Equazione Errata.")
            elif status.startswith("plat_first_grade"):
                end_time = time.time()
                eq_id = int(status.split(" ")[1])
                start_time = float(status.split(" ")[2])
                eq = c.execute("SELECT * FROM equations WHERE id = ?", (eq_id,))
                eq_solutions = eq[2]
                eq_resolves = eq[4]
                eq_resolves_sum = 0
                resolve_media = 0.00
                for sol in eq_solutions:
                    if e.text == sol:
                        for soll in eq_resolves:
                            eq_resolves_sum += int(soll)
                        resolver_media = eq_resolves_sum / len(eq_resolves)
                        await e.reply(f"Equazione Corretta! Il tuo tempo e' stato di {end_time - start_time} secondi, il tuo tempo e' stato di: {resolve_media} secondi")
                

        elif e.text == "/start":
            lang = c.execute("SELECT lang FROM langs WHERE telegram_id = ?" (e.sender.id,)).fetchone()[0]
            if lang:
                f = json.load(open(f"{lang}.json", "r"))
                msg = f["welcome"]
                await e.reply(msg["msg"], buttons=[[Button.inline(["msg"]["play"], "play"), Button.inline(["msg"]["leaderboards"], "leaderboards")], [Button.inline(msg["guide"], "guide"), Button.inline("📊 RANKING", "ranking")], [Button.inline(msg["training"], "training")], [Button.url(msg["channel"], "https://t.me/condonatodev")]])
            else:
                await e.reply("Choose a language\n\nWant to help the translation? [click here](https://crowdin.com/project/betterelo)", buttons=[[Button.inline("ITALIAN", "it"), Button.inline("ENGLISH", "en")]])


@client.on(CallbackQuery)
async def callback(e):
    db = sqlite3.connect("betterelo.db")
    c = db.cursor()
    if e.data == b"it":
        c.execute("INSERT INTO langs VALUES ?, ?" (e.sender.id, "it"))
        db.commit()
        f = json.load(open("it.json", "r"))
        msg = f["welcome"]
        await e.edit(msg, buttons=[[Button.inline("🎮 GIOCA", "play"), Button.inline("🏆 CLASSIFICHE", "leaderboards")], [Button.inline("⁉️ GUIDA", "guide"), Button.inline("📊 RANKING", "ranking")], [Button.inline("🎮 ALLENATI in SOLITARIA", "training")], [Button.rul("📣 CANALE", "https://t.me/condonatodev")]])
    elif e.data == b"en":
        c.execute("INSERT INTO langs VALUES?,?" (e.sender.id, "en"))
        db.commit()
        f = json.load(open("en.json", "r"))
        msg = f["welcome"]
        await e.edit(msg, buttons=[[Button.inline("🎮 PLAY", "play"), Button.inline("🏆 LEADERBOARDS", "leaderboards")], [Button.inline("⁉️ GUIDE", "guide"), Button.inline("📊 RANKING", "ranking")], [Button.inline("🎮 TRAIN YOURSELF", "training")], [Button.url("📣 CHANNEL", "https://t.me/condonatodev")]])
    elif e.data == b"user_start":
        try:
            del statuses[str(e.sender.id)]
        finally:
            lang = c.execute("SELECT lang FROM langs WHERE telegram_id = ?" (e.sender.id,)).fetchone()[0]
            f = json.load(open(f"{lang}.json", "r"))
            await e.edit(f["welcome"]["msg"], buttons=[[Button.inline(f["welcome"]["play"], "play"), Button.inline(f["welcome"]["leaderboards"], "leaderboards")], [Button.inline(f["welcome"]["guide"], "guide"), Button.inline("📊 RANKING", "ranking")], [Button.inline(f["welcome"]["train"], "training")], [Button.url(f["welcome"]["channel"], "https://t.me/condonatodev")]])
    elif e.data == b"play":
        await e.edit("SCEGLI IL TIPO DI EQUAZIONE DA RISOLVERE", buttons=[[Button.inline("🎮 PRIMO GRADO", "play_first_grade"), Button.inline("🎮 SECONDO GRADO", "play_second_grade")], [Button.inline("◀️ INDIETRO", "user_start")]])
    elif e.data == b"play_first_grade":
        pass
    elif e.data == b"play_second_grade":
        pass
    elif e.data == b"leaderboards":
        await e.edit("Scegli una Classifica", buttons=[[Button.inline("🏆 PRIMO GRADO", "leaderboard_first_grade"), Button.inline("🏆 SECONDO GRADO", "leaderboard_second_grade")], [Button.inline("◀️ INDIETRO", "user_start")]])
    elif e.data == b"leaderboard_first_grade":
        await e.edit(f"CLASSIFICA EQUAZIONI DI PRIMO GRADO:\n{leaderboard_first_grade.string()}", buttons=[[Button.inline("◀️ INDIETRO", "user_start")]])
    elif e.data == b"leaderboard_second_grade":
        await e.edit(f"CLASSIFICA EQUAZIONI DI SECONDO GRADO:\n{leaderboard_second_grade.string()}", buttons=[[Button.inline("◀️ INDIETRO", "user_start")]])
    elif e.data == b"guide":
        lang = c.execute("SELECT lang FROM langs WHERE telegram_id = ?" (e.sender.id,)).fetchone()[0]
        f = json.load(open(f"{lang}.json", "r"))
        guide_text = f["guide"]
        await e.edit(guide_text, buttons=[[Button.inline(f"◀️ {f['utility']['back']}", "user_start")]])
    elif e.data == b"ranking":
        await e.edit(ranking_text, buttons=[[Button.inline("◀️ INDIETRO", "user_start")]])
    elif e.data == b"training":
        await e.edit("SCEGLI IL TIPO DI EQUAZIONI PER LA QUALE ALLENARTI", buttons=[[Button.inline("🎮 PRIMO GRADO", "training_first_grade"), Button.inline("🎮 SECONDO GRADO", "training_second_grade")], [Button.inline("◀️ INDIETRO", "user_start")]])
    elif e.data == b"training_first_grade":
        equations = c.execute("SELECT * FROM equations WHERE grade = 1").fetchall()
        eq = random.choice(equations)
        eq_id = eq[0]
        eq_text = eq[1]
        eq_solutions = eq[2]
        resolves = eq[4]
        solutions_string = ""
        for sol in eq_solutions:
            solutions_string = solutions_string + sol + "\n"
        start_time = time.time()
        statuses[str(e.sender.id)] = f"training_first_grade {eq_id} {start_time}"
        await e.edit(f"{eq_text}\n\n{first_grade_text}", buttons=[[Button.inline("◀️ INDIETRO", "user_start")]])
    elif e.data == b"play_first_grade":
        equations = c.execute("SELECT * FROM equations WHERE grade = 1").fetchall()
        eq = random.choice(equations)
        eq_id = eq[0]
        eq_text = eq[1]
        eq_solutions = eq[2]
        resolves = eq[4]
        solutions_string = ""
        for sol in eq_solutions:
            solutions_string = solutions_string + sol + "\n"
        start_time = time.time()
        statuses[str(e.sender.id)] = f"play_first_grade {eq_id} {start_time}"
        await e.edit(f"{eq_text}\n\n{first_grade_text}")

client.start()
client.run_until_disconnected()