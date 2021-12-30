import os
import json
import logging
from getpass import getpass
from pathlib import Path
from typing import Optional

from .exceptions import ImproperlyConfigured, ConfigNotFound
from .utils import yes_or_no

APP_NAME = "time_attack"

CONF_FILE_NAME = "config.json"

DATA_FILE_NAME = "time-attack.json"

log = logging.getLogger(__name__)


def get_conf_file_path():
    if "APPDATA" in os.environ:
        conf_path = Path(os.environ.get("APPDATA")) / APP_NAME
    elif "XDG_CONFIG_HOME" in os.environ:
        conf_path = Path(os.environ.get("XDG_CONFIG_HOME")) / APP_NAME
    else:
        raise ImproperlyConfigured("Please specify a config directory.")

    conf_path.mkdir(parents=True, exist_ok=True)

    return conf_path / CONF_FILE_NAME


def get_config(conf_file_path: Optional[Path] = None) -> dict:
    if conf_file_path is None:
        conf_file_path = get_conf_file_path()

    if conf_file_path.exists():

        with conf_file_path.open(mode="r", encoding="utf-8") as f:
            config = json.load(f)

    else:
        config = init_config(conf_file_path)
        if config is None:
            raise ConfigNotFound()
        else:
            return get_config(conf_file_path)
    return config


def write_config(config: dict, conf_file_path: Optional[Path] = None):
    if conf_file_path is None:
        conf_file_path = get_conf_file_path()
    with conf_file_path.open("w", encoding="utf-8") as f:
        json.dump(config, f)
        log.info("Wrote new config.")


def init_config(
    config_file_path: Path = None,
) -> Optional[dict]:
    yes = yes_or_no(
        "Are you sure you want to initialize? All existing config will be overwritten."
    )

    if yes:
        data_dir = Path(input("Where would you like to save data?"))
        encrypt = yes_or_no("Would you like data to be encrypted?")

        if encrypt:
            save_password = yes_or_no("Save password?")

            if save_password:
                password = getpass()
            else:
                password = None
        else:
            save_password = False
            password = None

        data_dir.mkdir(parents=True, exist_ok=True)

        config = {
            "encrypt": encrypt,
            "data_dir": str(data_dir),
        }

        if encrypt and save_password:
            config["password"] = password
        write_config(config, config_file_path)
        return config
