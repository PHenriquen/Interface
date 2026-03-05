import re


def parse_temperature_line(text):
    text = text.strip()
    if not text:
        raise ValueError("Linha vazia")

    if "=" not in text:
        value, unit = parse_legacy_line(text)
        if value is None:
            try:
                value = float(text.replace(",", "."))
            except ValueError as err:
                raise ValueError(f"Dado invalido: {text}") from err
            unit = "C"
        return "temperatura", value, unit

    fields = {}
    for part in text.split(";"):
        if "=" in part:
            key, value = part.split("=", 1)
            fields[key.strip().upper()] = value.strip()

    if "VALOR" not in fields:
        value, unit = parse_legacy_line(text)
        if value is None:
            raise ValueError(f"Sem VALOR: {text}")
        return "temperatura", value, unit

    try:
        value = float(fields["VALOR"].replace(",", "."))
    except ValueError as err:
        raise ValueError(f"VALOR invalido: {fields['VALOR']}") from err

    return fields.get("SENSOR", "temperatura"), value, fields.get("UNIDADE", "C")


def parse_legacy_line(text):
    lowered = text.lower()

    # Match both patterns:
    # "celsius: 23.5" and "23.5 celsius"
    match_c = re.search(
        r"(?:celsius|centigrados?|centigrade|c)\s*[:=]?\s*(-?\d+(?:[.,]\d+)?)",
        lowered,
    )
    if not match_c:
        match_c = re.search(
            r"(-?\d+(?:[.,]\d+)?)\s*(?:\u00b0\s*c|celsius|centigrados?|centigrade)\b",
            lowered,
        )
    if match_c:
        try:
            return float(match_c.group(1).replace(",", ".")), "C"
        except ValueError:
            pass

    # Match both patterns:
    # "fahrenheit: 77" and "77 fahrenheit" / "77F"
    match_f = re.search(r"fahrenheit\s*[:=]?\s*(-?\d+(?:[.,]\d+)?)", lowered)
    if not match_f:
        match_f = re.search(r"(-?\d+(?:[.,]\d+)?)\s*(?:\u00b0\s*f|f)\b", lowered)
    if match_f:
        try:
            return float(match_f.group(1).replace(",", ".")), "F"
        except ValueError:
            pass

    match_temp = re.search(r"temperatura[^0-9-]*(-?\d+(?:[.,]\d+)?)", lowered)
    if match_temp:
        try:
            # If only Fahrenheit context is present, preserve unit F.
            if "fahrenheit" in lowered and "celsius" not in lowered:
                return float(match_temp.group(1).replace(",", ".")), "F"
            return float(match_temp.group(1).replace(",", ".")), "C"
        except ValueError:
            pass

    numbers = re.findall(r"-?\d+(?:[.,]\d+)?", lowered)
    if numbers:
        try:
            return float(numbers[0].replace(",", ".")), "C"
        except ValueError:
            return None, "C"

    return None, "C"


def to_celsius(value, unit):
    normalized = (unit or "").strip().upper().replace(" ", "")
    normalized = normalized.replace("\u00b0", "")
    if normalized in ("F", "FAHRENHEIT"):
        return (value - 32.0) * 5.0 / 9.0
    return value
