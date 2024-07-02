from typing import Sequence
import argparse
import os
from collections import defaultdict
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

checked_names = {
    "access",
    "auth",
    "key",
    "loging",
    "pass",
    "passwd",
    "password",
    "path",
    "pwd",
    "secret",
    "token",
    "uri",
    "url",
}

checked_values = {
    "AppData",
    "home",
    "http://",
    "https://",
    "ssh://",
    "Program Files",
    "Users",
}

ignored_values = {
    "",
    "false",
    "no",
    "none",
    "null",
    "off",
    "on",
    "true",
    "yes",
    "default",
    "0",
    "1",
    "2",
}

expected: dict[str, set[str]] = defaultdict(set)
expected["CI_SERVER_URL".lower()].update("pyproject.toml", "cruft.json")
expected["CI_PROJECT_PATH".lower()].update("pyproject.toml", "cruft.json")
expected["CI_PROJECT_URL".lower()].update("pyproject.toml", "cruft.json")
expected["CI_API_V4_URL".lower()].update("pyproject.toml", "cruft.json")

def check_env_leakage(contents: str, name: str, ignored: list[str]) -> bool:
    retv = 0
    for key, value in os.environ.items():
        if key.lower() in ignored or value.lower() in ignored_values or any(name.lower().endswith(fname.lower()) for fname in expected[key.lower()]):
            continue
        if any(name in key.lower() for name in checked_names) or any(
            val in value.lower() for val in checked_values
        ):
            for i, line in enumerate(contents):
                if value in line:
                    print(
                        f"Environment variable {key} leaked in file {name}:{i + 1}"
                    )
                    retv = 1
                    break
    return retv


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    parser.add_argument("--ignore", type=str, default="")
    args = parser.parse_args(argv)

    retv = 0

    ignore_list = (
        [ignore.lower() for ignore in args.ignore.split(",")] if args.ignore else []
    )

    for filename in args.filenames:
        with open(filename, "rt") as f:
            contents = f.read()
        retv |= check_env_leakage(contents.split("\n"), filename, ignore_list)

    return retv


if __name__ == "__main__":
    raise SystemExit(main())
