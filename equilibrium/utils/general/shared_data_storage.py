import datetime
import pathlib

import equilibrium

DATA_DIR_PATH = f"{equilibrium.__path__[0]}/../data/"


def get_snapshot_data_dir(data):
    user_info = data["user_information"]
    snapshot = data["snapshot"]

    timestamp = datetime.datetime.fromtimestamp(snapshot.datetime / 1000)
    return (pathlib.Path(DATA_DIR_PATH) / str(user_info.user_id) / f"{timestamp:%Y-%m-%d_%H-%M-%S-%f}").resolve()
