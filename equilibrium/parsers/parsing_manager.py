import importlib
import inspect
import json
import pathlib

from equilibrium.utils.sample import SampleHandler
from equilibrium.utils.general.shared_data_storage import get_snapshot_data_dir


class ParsingManager:
    parsers = {}

    @classmethod
    def parses(cls, parser_name):
        def decorator(obj):
            if inspect.isclass(obj):
                parser = obj().parse
            else:
                parser = obj
            cls.parsers[parser_name] = parser
            return obj

        return decorator

    @classmethod
    def invoke(cls, parser_name, data):
        data_dir_path = pathlib.Path(get_snapshot_data_dir(data))
        importlib.import_module(f"equilibrium.parsers.{parser_name}")
        return cls.parsers[parser_name](data["snapshot"], data_dir_path)


def run_parser(parser_name, raw_data):
    json_dict = json.loads(raw_data)
    data = SampleHandler.json_to_data(json_dict)
    json_dict["result"] = {parser_name: ParsingManager().invoke(parser_name, data)}
    return json.dumps(json_dict)
