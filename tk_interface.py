import queue, threading, tkinter as tk
from datetime import datetime
from tkinter import ttk
from serial_backend import HAS_PYSERIAL, detect_arduino_ports, list_serial_ports, open_serial_connection, serial_read_loop, simulation_loop
from temperature_parser import parse_temperature_line, to_celsius


class AppSerial:
    def __init__(self, root):
        self.root = root
        root.title("Monitor Serial"); root.geometry("860x540"); root.minsize(760, 460)
        self.queue, self.stop_event = queue.Queue(), threading.Event()
        self.conn, self.mode, self.errors, self.history = None, "", 0, []
        self.build_ui(); self.refresh_ports(); self.poll_queue(); root.protocol("WM_DELETE_WINDOW", self.close)

    def build_ui(self):
        r = self.root; r.grid_columnconfigure(0, weight=1); r.grid_rowconfigure(1, weight=1)
        tk.Label(r, text="Interface Tkinter + Serial", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(12, 6))

        left = tk.LabelFrame(r, text="Leitura e Historico", padx=10, pady=8)
        left.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=(0, 12)); left.grid_columnconfigure(0, weight=1); left.grid_rowconfigure(6, weight=1)
        self.temp_label = tk.Label(left, text="-- C", font=("Segoe UI", 30, "bold")); self.temp_label.grid(row=0, column=0, sticky="w")
        self.sensor_label = tk.Label(left, text="Sensor: --"); self.sensor_label.grid(row=1, column=0, sticky="w")
        self.quality_label = tk.Label(left, text="Qualidade: --"); self.quality_label.grid(row=2, column=0, sticky="w")
        self.status_label = tk.Label(left, text="Status: aguardando"); self.status_label.grid(row=3, column=0, sticky="w", pady=(0, 6))
        self.last_line = tk.Label(left, text="Ultima linha: --"); self.last_line.grid(row=4, column=0, sticky="w", pady=(0, 6))
        actions = tk.Frame(left); actions.grid(row=5, column=0, sticky="ew", pady=(0, 6)); actions.grid_columnconfigure(0, weight=1); actions.grid_columnconfigure(1, weight=1)
        ttk.Button(actions, text="Limpar", command=self.clear_history).grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(actions, text="Atualizar portas", command=self.refresh_ports).grid(row=0, column=1, sticky="ew", padx=(4, 0))
        self.listbox = tk.Listbox(left, font=("Consolas", 10), height=10); self.listbox.grid(row=6, column=0, sticky="nsew")

        side = tk.Frame(r); side.grid(row=1, column=1, sticky="nsew", padx=(6, 12), pady=(0, 12)); side.grid_rowconfigure(1, weight=1)
        serial = tk.LabelFrame(side, text="Conexao USB (Arduino)", padx=10, pady=8)
        serial.grid(row=0, column=0, sticky="new"); serial.grid_columnconfigure(0, weight=1)
        tk.Label(serial, text="Porta").grid(row=0, column=0, sticky="w")
        self.port_combo = ttk.Combobox(serial, state="readonly", width=24); self.port_combo.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        tk.Label(serial, text="Baudrate").grid(row=2, column=0, sticky="w")
        self.baud_combo = ttk.Combobox(serial, state="readonly", values=["9600", "19200", "38400", "57600", "115200"], width=24)
        self.baud_combo.set("9600"); self.baud_combo.grid(row=3, column=0, sticky="ew", pady=(0, 6))
        self.detect_label = tk.Label(serial, text="Arduino: procurando..."); self.detect_label.grid(row=4, column=0, sticky="w", pady=(0, 6))
        sbtn = tk.Frame(serial); sbtn.grid(row=5, column=0, sticky="ew"); sbtn.grid_columnconfigure(0, weight=1); sbtn.grid_columnconfigure(1, weight=1)
        self.connect_btn = ttk.Button(sbtn, text="Conectar", command=lambda: self.start("serial")); self.connect_btn.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(sbtn, text="Desconectar", command=self.disconnect).grid(row=0, column=1, sticky="ew", padx=(4, 0))

        sim = tk.LabelFrame(side, text="Simulacao", padx=10, pady=8)
        sim.grid(row=2, column=0, sticky="sew", pady=(8, 0))
        tk.Label(sim, text="Intervalo (s)").grid(row=0, column=0, sticky="w")
        self.sim_interval = ttk.Combobox(sim, state="readonly", values=["0.2", "0.5", "1.0", "2.0"], width=10)
        self.sim_interval.set("1.0"); self.sim_interval.grid(row=1, column=0, sticky="w", pady=(0, 6))
        sim_btn = tk.Frame(sim); sim_btn.grid(row=2, column=0, sticky="ew"); sim_btn.grid_columnconfigure(0, weight=1); sim_btn.grid_columnconfigure(1, weight=1)
        ttk.Button(sim_btn, text="Iniciar", command=lambda: self.start("sim")).grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(sim_btn, text="Parar", command=self.disconnect).grid(row=0, column=1, sticky="ew", padx=(4, 0))

    def refresh_ports(self):
        usb, arduino = [p.device for p in list_serial_ports()], (detect_arduino_ports() if HAS_PYSERIAL else [])
        ports = arduino or usb; self.port_combo["values"] = ports; self.port_combo.set(ports[0] if ports else "")
        txt = "Arduino: pyserial nao instalado" if not HAS_PYSERIAL else f"Arduino: {', '.join(arduino)}" if arduino else "Arduino: nenhum identificado (usando USB encontrado)" if usb else "Arduino: nenhum dispositivo USB"
        self.detect_label.configure(text=txt)

    def set_running(self, running):
        st = "disabled" if running else "readonly"
        self.port_combo.configure(state=st); self.baud_combo.configure(state=st); self.connect_btn.configure(state="disabled" if running else "normal")

    def start(self, mode):
        if self.mode: return
        if mode == "serial":
            if not HAS_PYSERIAL: self.status_label.configure(text="Status: pyserial nao instalado"); return
            port = self.port_combo.get().strip()
            if not port: self.status_label.configure(text="Status: conecte um Arduino USB"); return
            try: self.conn = open_serial_connection(port, int(self.baud_combo.get()))
            except Exception as err: self.status_label.configure(text=f"Status: erro ao conectar ({err})"); return
            target, args, status = serial_read_loop, (self.stop_event, self.conn, self.queue, parse_temperature_line), f"Status: conectado em {port}"
        else:
            self.conn = None
            target, args, status = simulation_loop, (self.stop_event, self.queue, parse_temperature_line, "LM35", float(self.sim_interval.get())), "Status: simulacao ativa"
            self.sensor_label.configure(text="Sensor: LM35 (sim)")
        self.mode = mode; self.stop_event.clear(); threading.Thread(target=target, args=args, daemon=True).start(); self.set_running(True); self.status_label.configure(text=status)

    def disconnect(self):
        self.stop_event.set()
        if self.conn:
            try: self.conn.close()
            except Exception: pass
        self.conn, self.mode = None, ""; self.set_running(False); self.status_label.configure(text="Status: desconectado")

    def poll_queue(self):
        while not self.queue.empty():
            kind, *data = self.queue.get_nowait()
            if kind == "linha": self.last_line.configure(text=f"Ultima linha: {data[0]}")
            elif kind == "dado":
                s, v, u = data
                self.history.insert(0, f"{datetime.now().strftime('%H:%M:%S')} | {s:<12} | {v:>7.2f} {u}"); del self.history[20:]
                self.temp_label.configure(text=f"{to_celsius(v, u):.1f} C"); self.sensor_label.configure(text=f"Sensor: {s}"); self.quality_label.configure(text="Qualidade: valido")
                self.listbox.delete(0, tk.END)
                for row in self.history: self.listbox.insert(tk.END, row)
            elif kind == "invalido": self.errors += 1; self.quality_label.configure(text=f"Qualidade: invalido ({self.errors})")
            elif kind == "erro": self.status_label.configure(text=f"Status: {data[0]}"); self.disconnect()
            elif kind == "fim" and not self.stop_event.is_set(): self.disconnect()
        self.root.after(120, self.poll_queue)

    def clear_history(self):
        self.history.clear(); self.errors = 0; self.listbox.delete(0, tk.END)
        self.last_line.configure(text="Ultima linha: --"); self.quality_label.configure(text="Qualidade: --")

    def close(self): self.disconnect(); self.root.destroy()


def main():
    root = tk.Tk(); AppSerial(root); root.mainloop()


if __name__ == "__main__":
    main()
