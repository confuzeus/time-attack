"""Console script for time_attack."""
import argparse
import sys
from pathlib import Path

from time_attack.conf import get_config, init_config


def main():
    """Console script for time_attack."""
    parser = argparse.ArgumentParser(description="Track your time.")

    parser.add_argument(
        "action",
        type=str,
        choices=("start", "stop", "init"),
        help="The type of action to perform.",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_path",
        help="Location of the config file.",
        type=Path,
    )
    parser.add_argument("task_name", type=str, help="The name of your task.")
    args = parser.parse_args()

    # Load config here

    config = get_config(args.config_path)

    if args.action == "start":
        print(f"Starting {args.task_name}")
    elif args.action == "stop":
        print(f"Stopping {args.task_name}")
    else:
        init_config(args.config_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
