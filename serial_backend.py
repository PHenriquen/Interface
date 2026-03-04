import random
import time

try:
    import serial
    import serial.tools.list_ports

    HAS_PYSERIAL = True
except Exception:
    HAS_PYSERIAL = False

ARDUINO_VIDS = {0x2341, 0x2A03, 0x1A86, 0x10C4, 0x0403, 0x239A}
ARDUINO_HINTS = ("arduino", "ch340", "cp210", "ftdi", "usb serial", "ttyacm", "wch")


def list_serial_ports():
    if not HAS_PYSERIAL:
        return []
    return list(serial.tools.list_ports.comports())


def _is_arduino_like(port_info):
    text = " ".join(
        [
            getattr(port_info, "device", "") or "",
            getattr(port_info, "description", "") or "",
            getattr(port_info, "manufacturer", "") or "",
            getattr(port_info, "product", "") or "",
            getattr(port_info, "hwid", "") or "",
        ]
    ).lower()
    vid = getattr(port_info, "vid", None)
    return (vid in ARDUINO_VIDS) or any(hint in text for hint in ARDUINO_HINTS)


def detect_arduino_ports():
    return [p.device for p in list_serial_ports() if _is_arduino_like(p)]


def list_ports_with_simulation():
    ports = [p.device for p in list_serial_ports()]
    if "SIMULACAO" not in ports:
        ports.append("SIMULACAO")
    return ports


def open_serial_connection(port, baudrate):
    if not HAS_PYSERIAL:
        raise RuntimeError("pyserial nao instalado")
    return serial.Serial(port=port, baudrate=baudrate, timeout=1)


def serial_read_loop(stop_event, connection, output_queue, parse_fn):
    while not stop_event.is_set():
        if connection is None:
            break

        try:
            line = connection.readline().decode("utf-8", errors="ignore").strip()
        except Exception as err:
            output_queue.put(("erro", f"Serial desconectada: {err}"))
            break

        if not line:
            continue

        output_queue.put(("linha", line))
        try:
            output_queue.put(("dado", *parse_fn(line)))
        except ValueError as err:
            output_queue.put(("invalido", str(err)))

    output_queue.put(("fim",))


def simulation_loop(stop_event, output_queue, parse_fn, sensor_name="LM35", interval_s=1.0):
    while not stop_event.is_set():
        value = round(random.uniform(23.0, 30.0), 2)
        line = f"SENSOR={sensor_name};VALOR={value:.2f};UNIDADE=C"
        output_queue.put(("linha", line))
        output_queue.put(("dado", *parse_fn(line)))
        time.sleep(interval_s)

    output_queue.put(("fim",))
