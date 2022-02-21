import click
from contacts.core import (
    JsonDB,
)
from contacts.utils import console, get_print_func

print(__name__)


DB = JsonDB()


@click.group()
def cli():
    pass


@click.command()
def init():
    res = DB.init()
    if res is None:
        console.print("Database already initialized", style="orange1")
    else:
        console.print("Database initialized successfully", style="green")


@click.command()
@click.argument("action", type=click.STRING)
def db(action):
    match action:
        case "reset":
            DB.reset()
        case _:
            print("Unknown option")


@click.command()
@click.option("--first-name", "first_name", prompt="First name")
@click.option("--last-name", "last_name", prompt="Last name")
@click.option("--sex", "sex", prompt="Sex")
@click.option("--address", "address", prompt="Address")
@click.option(
    "--output",
    default="table",
    type=click.Choice(["table", "raw"], case_sensitive=False),
)
def add(first_name, last_name, sex, address, output):
    contact = DB.add(
        first_name=first_name, last_name=last_name, sex=sex, address=address
    )

    print = get_print_func(output)
    print(contact)


@click.command()
@click.argument("id", type=click.INT, required=False)
@click.option(
    "--output",
    default="table",
    type=click.Choice(["table", "raw"], case_sensitive=False),
)
def get(id=None, output="table"):
    contact = DB.get(id)

    print = get_print_func(output)
    print(data=contact)


@click.command()
@click.argument("id", type=click.INT)
@click.option("--first-name", "first_name", required=False)
@click.option("--last-name", "last_name", required=False)
@click.option("--sex", "sex", required=False)
@click.option("--address", "address", required=False)
@click.option(
    "--output",
    default="table",
)
def update(id, output, **kwargs):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}
    contact = DB.update(id, **kwargs)

    print = get_print_func(output)
    print(contact)


@click.command()
@click.argument("id", type=click.INT)
@click.option(
    "--output",
    default="table",
)
def remove(id=None, output="table"):
    contact = DB.remove(id)

    print = get_print_func(output)
    print(contact)


@click.command()
@click.argument("keyword", type=click.STRING)
@click.option(
    "--output",
    default="table",
)
def find(keyword, output="table"):
    if keyword.isnumeric():
        keyword = int(keyword)

    contact = DB.find(keyword=keyword)

    print = get_print_func(output)
    print(contact)


cli.add_command(init)
cli.add_command(db)
cli.add_command(add)
cli.add_command(get)
cli.add_command(update)
cli.add_command(remove)
cli.add_command(find)
