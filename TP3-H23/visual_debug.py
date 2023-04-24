import numpy as np
import json


def serialize_np_array(np_array: np.array) -> str:
    formatted = {
        "kind": {"grid": True},
        "rows": [
            {
                "columns": [
                    {"content": str(value), "tag": str(value)} for value in row
                ],
            }
            for row in np_array
        ],
    }
    return json.dumps(formatted)
