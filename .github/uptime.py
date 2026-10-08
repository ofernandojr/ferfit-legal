"""Updates status.json after the uptime check: a message for the app while the Ferfit server is down, none when it is
back. Prints "alert" when the job should fail (GitHub then e-mails the repository owner): when the server has just gone
down, and once an hour while it stays down. Usage: python3 .github/uptime.py <true|false>"""
import json, sys, datetime

ok = sys.argv[1] == "true"
now = datetime.datetime.now(datetime.timezone.utc)
path = "status.json"
status = json.load(open(path, encoding="utf-8"))

DOWN = {
    "pt": "O servidor do Ferfit está fora do ar agora. Já estamos resolvendo; seus treinos continuam salvos no aparelho.",
    "en": "The Ferfit server is down right now. We are on it; your workouts stay saved on your device.",
    "es": "El servidor de Ferfit está caído ahora. Ya lo estamos resolviendo; tus entrenamientos siguen guardados en el dispositivo.",
}

alert = False
if ok:
    status["message"] = None
    status["down_since"] = None
else:
    if not status.get("down_since"):
        status["down_since"] = now.strftime("%Y-%m-%dT%H:%MZ")
        alert = True
    elif now.minute < 5:
        alert = True
    # Keep a message written by hand (e.g. planned maintenance); else the default one.
    if not status.get("message"):
        status["message"] = DOWN

# One change a month even when all is well, so GitHub does not pause the schedule of an idle repository.
status["checked"] = now.strftime("%Y-%m")

with open(path, "w", encoding="utf-8") as f:
    json.dump(status, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("alert" if alert else "quiet")
