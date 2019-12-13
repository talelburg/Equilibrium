from equilibrium.sample import v1, v2


class SampleReader:
    adapters = {1: v1.Adapter, 2: v2.Adapter}

    def __init__(self, version: int):
        self.adapter = self.adapters[version]()

    def parse(self, path: str):
        return self.adapter.parse(path)

    def build(self, obj):
        return self.adapter.build(obj)
