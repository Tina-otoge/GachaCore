import importlib
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("command", choices=["import"])
parser.add_argument("module", type=str)
parser.add_argument(
    "--clean",
    action="store_true",
    help="Wipe the database before importing data",
)
parser.add_argument("--max", type=int, help="Stop after this many entries")

args = parser.parse_args()


def run_import_for_module(module):
    print(f"Running {module} import")
    module = importlib.import_module(f"plugins.{module}.parser")
    if args.clean:
        module.db.drop_database()
    module.db.create_database()
    if args.max:
        module.main(stop_at=args.max)
    else:
        module.main()


if args.command == "import":
    run_import_for_module(args.module)
