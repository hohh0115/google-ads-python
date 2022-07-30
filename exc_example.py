import argparse
from importlib import import_module

from examples.misc.get_pmax_campaign_assets_info import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Execute files in "examples/" folder from project root directory.'
    )
    parser.add_argument(
        "-p",
        "--example_file_path",
        type=str,
        required=True,
        help="The path of the example file to execute"
    )
    args = parser.parse_args()

    module_path = args.example_file_path.replace('.py', '').replace('/', '.')
    module = import_module(module_path)
    module.main()
