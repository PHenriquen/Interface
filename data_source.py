import os
import random
import time

from serial_backend import HAS_PYSERIAL, detect_arduino_ports, list_serial_ports, open_serial_connection
from temperature_parser import parse_temperature_line, to_celsius


def simulate_temperature():
    return round(random.uniform(20.0, 30.0), 2)


def _detect_port():
    if not HAS_PYSERIAL:
        return None

    forced = os.getenv("ARDUINO_PORT", "").strip()
    if forced:
        return forced

    arduino_ports = detect_arduino_ports()
    if arduino_ports:
        return arduino_ports[0]

    ports = [p.device for p in list_serial_ports()]
    return ports[0] if ports else None


def _read_from_serial():
    if not HAS_PYSERIAL:
        raise RuntimeError("pyserial nao instalado")

    port = _detect_port()
    if not port:
        raise RuntimeError("nenhuma porta serial detectada")

    baud = int(os.getenv("ARDUINO_BAUD", "9600"))
    timeout = float(os.getenv("ARDUINO_TIMEOUT", "1.0"))
    end_time = time.time() + float(os.getenv("ARDUINO_READ_WINDOW_S", "3.0"))

    with open_serial_connection(port=port, baudrate=baud) as conn:
        conn.timeout = timeout
        while time.time() < end_time:
            raw = conn.readline().decode("utf-8", errors="ignore").strip()
            if not raw:
                continue
            try:
                _, value, unit = parse_temperature_line(raw)
            except ValueError:
                continue
            return round(to_celsius(value, unit), 2), port

    raise RuntimeError("sem leitura valida dentro da janela de tempo")


def read_temperature_with_meta():
    mode = os.getenv("TEMP_SOURCE_MODE", "auto").strip().lower()
    if mode == "sim":
        return simulate_temperature(), "sim", "simulacao forcada"
    if mode not in ("auto", "serial"):
        mode = "auto"

    try:
        temp, port = _read_from_serial()
        return temp, "serial", f"porta {port}"
    except RuntimeError as err:
        if mode == "serial":
            raise
        return simulate_temperature(), "sim", f"fallback auto ({err})"


def read_temperature():
    return read_temperature_with_meta()[0]
