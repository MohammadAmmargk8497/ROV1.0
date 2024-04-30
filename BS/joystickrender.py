import json
from rich.live import Live
from rich.table import Table
from joysticksocket import s


def generate_table() -> Table:
    x = s.recvfrom(1000000)
    client_ip = x[1][0]
    data = x[0]
    data_final = json.loads(data.decode())
    # print(data_final)

    table = Table(title="Joystick Control Values")

    table.add_column("Control", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="yellow")

    table.add_row("Move", str(data_final['move']))
    table.add_row("Turn", str(data_final['turn']))
    table.add_row("Depth", str(data_final['depth']))

    return table


with Live(generate_table(), refresh_per_second=40) as live:
    while True:
        live.update(generate_table())
