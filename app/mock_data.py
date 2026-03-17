import datetime

WELLS = [
    {"id_well": "POZO-001"},
    {"id_well": "POZO-002"},
    {"id_well": "POZO-003"},
    {"id_well": "POZO-004"},
    {"id_well": "POZO-005"},
]

WELL_IDS = {w["id_well"] for w in WELLS}


def get_wells() -> list[dict]:
    return WELLS


def generate_forecast(
    id_well: str,
    date_start: datetime.date,
    date_end: datetime.date,
) -> list[dict]:
    """Generate mock forecast data with a simple linear decline.

    Starts at 150.0 bbl/day and decreases by 0.5 per day.
    """
    data = []
    current = date_start
    day_index = 0
    while current <= date_end:
        prod = round(150.0 - 0.5 * day_index, 1)
        if prod < 0:
            prod = 0.0
        data.append({"date": current.isoformat(), "prod": prod})
        current += datetime.timedelta(days=1)
        day_index += 1
    return data
