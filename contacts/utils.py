from rich import print_json
from rich.console import Console
from rich.table import Table

console = Console()


def print(message, level="INFO"):
    pass


def print_table(data):
    if not data:
        console.print("Not Found", style="red")
        return None

    table = Table(title="Contacts")

    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("First Name", style="blue", width=20)
    table.add_column("Last Name", style="blue", width=20)
    table.add_column("Sex", style="magenta", justify="right", width=8)
    table.add_column("Address", justify="right", style="green", width=20)

    if isinstance(data, list):
        for item in data:
            table.add_row(
                str(item["id"]),
                item["first_name"],
                item["last_name"],
                item["sex"],
                item["address"],
            )
    else:
        table.add_row(
            str(data["id"]),
            data["first_name"],
            data["last_name"],
            data["sex"],
            data["address"],
        )

    console.print(table)


def print_raw(data):
    if not data:
        console.print("Not Found", style="red")
        return None

    console.print_json(data=data)


def get_print_func(output="table"):
    if output == "raw":
        return print_raw
    return print_table
