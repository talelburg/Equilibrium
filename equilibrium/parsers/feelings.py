import json

from equilibrium.parsers.parsing_manager import ParsingManager


@ParsingManager.parses("feelings")
def parse_feelings(snapshot, data_dir_path):
    data = {
        "hunger": snapshot.feelings.hunger,
        "thirst": snapshot.feelings.thirst,
        "exhaustion": snapshot.feelings.exhaustion,
        "happiness": snapshot.feelings.happiness,
    }
    result_path = data_dir_path / "feelings.json"
    with open(result_path, 'w') as f:
        json.dump(data, f, indent=4)
    return result_path
