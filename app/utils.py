import json
from collections.abc import Iterator


class ExtendedEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Iterator):
            return list(o)
        return json.JSONEncoder.default(self, o)
