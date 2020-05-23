from equilibrium.parsers.parsing_manager import ParsingManager


@ParsingManager.parses("feelings")
def parse_feelings(snapshot, data_dir_path):
    return {
        "hunger": snapshot.feelings.hunger,
        "thirst": snapshot.feelings.thirst,
        "exhaustion": snapshot.feelings.exhaustion,
        "happiness": snapshot.feelings.happiness,
    }
