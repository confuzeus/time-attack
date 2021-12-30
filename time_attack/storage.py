import json
import logging
from pathlib import Path
from typing import Optional

from time_attack.crypto import decrypt, encrypt

log = logging.getLogger(__name__)


def load_data(
    data_file_path: Path, encrypted: bool, password: Optional[str] = None
) -> dict:
    data = {}
    if data_file_path.exists():

        if encrypted:

            if not password:
                raise ValueError("Password must be supplied.")

            with data_file_path.open("rb") as f:
                decrypted = decrypt(password, f.read())
                data.update(json.loads(str(decrypted)))
        else:

            with data_file_path.open(mode="r", encoding="utf-8") as f:
                data.update(json.load(f))
    return data


def write_data(
    data: dict, data_file_path: Path, encrypted: bool, password: Optional[str] = None
):

    if encrypted:
        if not password:
            raise ValueError("Password must be supplied.")
        json_str = json.dumps(data)
        encrypted_data = encrypt(password, json_str)

        with data_file_path.open("wb") as f:
            f.write(encrypted_data)
    else:

        with data_file_path.open(mode="w", encoding="utf-8") as f:
            json.dump(data, f)
    log.info("Wrote data.")
