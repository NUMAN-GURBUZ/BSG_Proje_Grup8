import tkinter as tk
import threading
import time
from datetime import datetime
import random
import os
import csv
import json
from ml_runtime import MLDetector   

energy_value   = 0.0
step           = 0
force_anomaly  = False
ocpp_connected = True
replay_enabled = False 
stop_event = threading.Event()
sim_thread = None

LOG_FILE = "log.txt"
REPLAY_FILE = os.path.join("data", "ocpp_log.json")

btn_ocpp = None
btn_replay = None


class SimpleReplay:
    def __init__(self, path):
        self.events = []
        self.idx = 0
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.events = json.load(f)
            except Exception:
                self.events = []
        # Normalize
        if not isinstance(self.events, list):
            self.events = []
    def reset(self):
        self.idx = 0
    def has_next(self):
        return self.idx < len(self.events)
    def next(self):
        if not self.has_next():
            return None
        ev = self.events[self.idx]
        self.idx += 1
        return ev

replay = SimpleReplay(REPLAY_FILE)


def gui_log(msg: str, tag="info"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} | {msg}\n"

    # GUI
    log_box.configure(state="normal")
    log_box.insert(tk.END, line, tag)
    log_box.see(tk.END)
    log_box.configure(state="disabled")

    # FILE
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except:
        pass


def update_energy_label():
    energy_label.config(text=f"Enerji: {energy_value:.2f} kWh")

def update_step_label():
    step_label.config(text=f"Adım: {step}")

def update_status(text, color="black"):
    status_label.config(text=text, fg=color)

def ensure_dirs():
    os.makedirs("data", exist_ok=True)


def run_simulation():
    global energy_value, step, force_anomaly

    ensure_dirs()

    update_status("Simülasyon başladı ✅", "blue")
    gui_log("=== Yeni simülasyon başladı ===", "general")

    energy_value = 0.0
    step         = 0
    update_energy_label()
    update_step_label()

    NORMAL_CSV = os.path.join("data", "normal_data.csv")
    if not os.path.exists(NORMAL_CSV):
        with open(NORMAL_CSV, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["step", "energy", "delta"])

    RULE_CSV = os.path.join("data", "rule_data.csv")
    if not os.path.exists(RULE_CSV):
        with open(RULE_CSV, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["step", "energy", "delta", "reason"])

    detector   = MLDetector()
    prevEnergy = 0.0

    if replay_enabled:
        replay.reset()
        gui_log("▶️ OCPP Replay açık (ocpp_log.json kullanılacak)", "general")

    for i in range(50):
        if stop_event.is_set():
            update_status("Durduruldu ⏹", "orange")
            return

        step = i
        update_step_label()

        used_replay = False
        if replay_enabled and replay.has_next():
            ev = replay.next()
            if ev:
                action = ev.get("action")
                if action == "Disconnect":
                    if ocpp_connected:
                        toggle_ocpp_internal(set_to=False)
                    gui_log("⛔ Replay: Disconnect", "rule")
                    used_replay = True
                elif action == "MeterValues":
                    payload = ev.get("payload", {})
                    mv = payload.get("meterValue", None)
                    if mv is not None:
                        energy_value = float(mv) / 1000.0
                        used_replay = True

        if not used_replay:
            energy_value += random.uniform(0.3, 1.2)

        if force_anomaly:
            energy_value += random.uniform(10.0, 20.0)
            gui_log("⚠️ Zorla anomali eklendi!", "anomaly")
            force_anomaly = False

        update_energy_label()

        delta = energy_value - prevEnergy
        prevEnergy = energy_value

        if ocpp_connected:
            is_anom, score = detector.predict_anomaly(energy_value, delta, 1)
            if is_anom:
                update_status("⚠️ ML Anomali", "red")
                gui_log(
                    f"ML ⚠️ANOMALİ | adım={step} | e={energy_value:.2f} | Δ={delta:.2f} | skor={score:.3f}",
                    "anomaly"
                )
            else:
                update_status("Simülasyon çalışıyor ✅", "green")
                gui_log(
                    f"ML NORMAL | adım={step} | e={energy_value:.2f} | Δ={delta:.2f} | skor={score:.3f}",
                    "normal"
                )
        else:
            if delta > 0:
                update_status("⚠️ RULE Anomali", "orange")
                gui_log(
                    f"RULE ⚠️ANOMALİ | adım={step} | e={energy_value:.2f} | Δ={delta:.2f}",
                    "rule"
                )
                with open(RULE_CSV, "a", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerow([step, f"{energy_value:.4f}", f"{delta:.4f}", "OCPP_DISCONNECTED"])

        with open(NORMAL_CSV, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([step, f"{energy_value:.4f}", f"{delta:.4f}"])

        time.sleep(0.5)

    update_status("Simülasyon bitti ✅", "green")
    gui_log("Simülasyon bitti ✅", "general")



def on_start():
    global sim_thread, force_anomaly
    force_anomaly = False
    stop_event.clear()

    if sim_thread and sim_thread.is_alive():
        return

    sim_thread = threading.Thread(target=run_simulation, daemon=True)
    sim_thread.start()

def on_stop():
    stop_event.set()
    update_status("Durdurma istendi ⏹", "orange")

def clear_logs():
    log_box.configure(state="normal")
    log_box.delete("1.0", tk.END)
    log_box.configure(state="disabled")
    update_status("Loglar temizlendi", "black")

def inject_anomaly():
    global force_anomaly
    force_anomaly = True
    gui_log("⚠️ Kullanıcı anomalisi tetiklendi", "anomaly")

def toggle_ocpp_internal(set_to=None):
    global ocpp_connected
    if set_to is None:
        ocpp_connected = not ocpp_connected
    else:
        ocpp_connected = bool(set_to)

    # ✅ تغيير لون الزر
    if ocpp_connected:
        btn_ocpp.config(bg="green")
    else:
        btn_ocpp.config(bg=tk.Button().cget("bg"))

    if ocpp_connected:
        gui_log("✅ OCPP Bağlandı",   "normal")
        update_status("OCPP bağlı ✅", "green")
    else:
        gui_log("❌ OCPP Kesildi", "rule")
        update_status("OCPP kesildi ❌", "orange")

def toggle_ocpp_button():
    toggle_ocpp_internal(set_to=None)

def toggle_replay():
    global replay_enabled
    replay_enabled = not replay_enabled

    # ✅ تغيير لون الزر
    if replay_enabled:
        btn_replay.config(bg="green")
        gui_log("▶️ OCPP Replay AÇIK (dosya: data/ocpp_log.json)", "general")
    else:
        btn_replay.config(bg=tk.Button().cget("bg"))
        gui_log("⏹ OCPP Replay KAPALI", "general")



window = tk.Tk()
window.title("EV Charger — ML + RULE (+Replay)")
window.geometry("980x620")

title = tk.Label(window, text="EV Charger — ML + RULE (+Replay)", font=("Arial", 18))
title.pack(pady=10)

row1 = tk.Frame(window)
row1.pack()

energy_label = tk.Label(row1, text="Enerji: 0 kWh", font=("Arial", 14))
energy_label.pack(side=tk.LEFT, padx=6)

step_label = tk.Label(row1, text="Adım: 0", font=("Arial", 14))
step_label.pack(side=tk.LEFT, padx=6)

status_label = tk.Label(window, text="Hazır", font=("Arial", 14))
status_label.pack(pady=6)

# ---------- Controls ----------
controls = tk.Frame(window)
controls.pack(pady=6)

tk.Button(controls, text="Başlat", font=("Arial",12), width=12, command=on_start).pack(side=tk.LEFT, padx=6)
tk.Button(controls, text="Durdur", font=("Arial",12), width=12, command=on_stop).pack(side=tk.LEFT, padx=6)
tk.Button(controls, text="ML Anomali", font=("Arial",12), width=12, command=inject_anomaly).pack(side=tk.LEFT, padx=6)

# ✅ زر OCPP مع متغير
btn_ocpp = tk.Button(controls, text="OCPP Aç/Kapa", font=("Arial",12), width=12, command=toggle_ocpp_button)
btn_ocpp.pack(side=tk.LEFT, padx=6)

# ✅ زر Replay مع متغير
btn_replay = tk.Button(controls, text="Replay Aç/Kapa", font=("Arial",12), width=14, command=toggle_replay)
btn_replay.pack(side=tk.LEFT, padx=6)

tk.Button(controls, text="Log Temizle", font=("Arial",12), width=12, command=clear_logs).pack(side=tk.LEFT, padx=6)

# ---------- LOG View ----------
log_box = tk.Text(window, width=120, height=25, font=("Courier New", 10), state="disabled")
log_box.pack(padx=10, pady=4)

# color tags
log_box.tag_config("normal",  foreground="green")
log_box.tag_config("anomaly", foreground="red")
log_box.tag_config("rule",    foreground="orange")
log_box.tag_config("general", foreground="blue")

window.mainloop()
