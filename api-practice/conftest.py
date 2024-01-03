import os
from typing import Any


def pytest_generate_tests(metafunc: Any) -> None:
    env_properties = {}

    with open("env/test.properties", "r") as f:
        for line in f:
            line = line.rstrip()  # removes trailing whitespace and '\n' chars

            if "=" not in line:
                continue  # skips blanks and comments w/o =
            if line.startswith("#"):
                continue  # skips comments which contain =

            k, v = line.split("=", 1)
            env_properties[k] = v

    for key, value in env_properties.items():
        os.environ[str(key)] = str(value)
