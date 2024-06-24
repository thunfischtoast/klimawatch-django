"""Parse actions from the raw data"""

import pandas as pd
import json
from pathlib import Path

if __name__ == "__main__":
    for path in Path("data/").glob("**/actions_raw.xlsx"):
        site = path.parent.name

        df = pd.read_excel(path)

        output = {}

        for field, group in df.groupby("Field"):
            # convert group to json and add to output
            output[field] = group.drop(columns=["Field"]).to_dict(orient="records")

        with open(f"data/{site}/actions.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)