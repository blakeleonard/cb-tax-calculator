import argparse
from collections import defaultdict
from csv import DictReader
from pprint import pprint

from dateparser import parse as parse_date
from pydantic import BaseModel


class AssetData(BaseModel):
    proceeds: float = 0
    cost_basis: float = 0
    gain: float = 0


def process_csv(csv_file_name: str) -> None:

    short_term_data: dict[str, AssetData] = defaultdict(AssetData)
    long_term_data: dict[str, AssetData] = defaultdict(AssetData)

    with open(csv_file_name) as csv_file:
        rows = DictReader(csv_file)

        for row in rows:
            asset_name = row["Asset name"]
            proceeds = float(row["Proceeds (USD)"])
            cost_basis = float(row["Cost basis (USD)"])

            start_date = parse_date(row["Date Acquired"])
            end_date = parse_date(row["Date of Disposition"])
            delta = end_date - start_date

            if delta.days < 365:
                short_term_data[asset_name].proceeds += proceeds
                short_term_data[asset_name].cost_basis += cost_basis
            else:
                long_term_data[asset_name].proceeds += proceeds
                long_term_data[asset_name].cost_basis += cost_basis

    for asset_data in short_term_data.values():
        asset_data.gain = round(asset_data.proceeds) - round(asset_data.cost_basis)

    for asset_data in long_term_data.values():
        asset_data.gain = round(asset_data.proceeds) - round(asset_data.cost_basis)

    print("\nShort Term:")
    pprint(short_term_data)

    print("\nLong Term:")
    pprint(long_term_data)
    print("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file_name")
    args = parser.parse_args()
    process_csv(args.csv_file_name)


if __name__ == "__main__":
    main()
