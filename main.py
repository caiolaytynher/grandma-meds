import datetime
import sys
import json

DATA = "/home/caio/Documents/python/grandma-meds/data.json"


def load_data(filepath: str) -> dict:
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def dump_data(filepath: str, data: dict) -> None:
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def validate_int(prompt: str) -> int:
    while True:
        string = input(prompt)
        if not string.isdigit():
            print("Please provide a valid number.")
        else:
            break

    return int(string)


def add_med(data: dict) -> None:
    name = input("Name: ").lower()
    if name in data:
        print("Medicine already added, continuing will update the system data.")

    doses = validate_int("Total amount of doses: ")
    daily_intake = validate_int("Daily intake: ")
    remaining_doses = validate_int("Remaining Doses: ")
    date = datetime.datetime.now()

    data[name] = {
        "last modification": str(date),
        "total doses": doses,
        "daily intake": daily_intake,
        "remaining doses": remaining_doses,
    }


def remove_med(data: dict) -> None:
    name = input("Name: ")
    if name in data:
        del data[name]
    else:
        print("Medication does not exist in the system.")


def list_meds(data: dict) -> None:
    for name in data:
        print(f"{name.capitalize()}:")
        for key, value in data[name].items():
            print(f"  {key.capitalize()}: {value}")


def show_med_status(name: str, data: dict) -> None:
    medication = data[name]
    previous_date = datetime.datetime.strptime(
        medication["last modification"][:10], "%Y-%m-%d"
    )
    days_passed = (datetime.datetime.now() - previous_date).days
    remaining_doses = (
        medication["remaining doses"] - days_passed * medication["daily intake"]
    )
    remaining_days = remaining_doses / medication["daily intake"]
    run_out_date = datetime.datetime.now() + datetime.timedelta(remaining_days)

    print(f"{name.capitalize()}:")
    print(f"  Remaining doses: {remaining_doses}")
    print(f"  Remaining days: {remaining_days:.0f}")
    print(f"  Run out date: {run_out_date:%d/%m/%Y}")


def get_status(data: dict):
    name = input("Name: ")
    if name == "" or name.lower() == "all":
        for medicine in data:
            show_med_status(medicine, data)
    elif name not in data:
        print("Medicine does not exist in the system.")
    else:
        show_med_status(name, data)


def main(argument: str) -> None:
    data: dict = load_data(DATA)
    commands = {
        "list": list_meds,
        "add": add_med,
        "remove": remove_med,
        "status": get_status,
    }

    if argument in commands:
        commands[argument](data)
        dump_data(DATA, data)
    else:
        print("Command does not exist.")


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        main(args[1])
    elif len(args) == 1:
        print('Please provide a command.')
    else:
        print("Please provide only one command at a time.")
