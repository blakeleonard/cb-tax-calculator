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
    short_term_data, long_term_data = get_data(csv_file_name)

    short_term_proceeds, short_term_cost_basis, short_term_gain, short_term_data = process_data(short_term_data)
    long_term_proceeds, long_term_cost_basis, long_term_gain, long_term_data = process_data(long_term_data)

    print("\nShort Term-")
    print(f"Proceeds: {short_term_proceeds}")
    print(f"Cost Basis: {short_term_cost_basis}")
    print(f"Gain: {short_term_gain}")
    print("Data:")
    pprint(short_term_data)

    print("\nLong Term:")
    print(f"Proceeds: {long_term_proceeds}")
    print(f"Cost Basis: {long_term_cost_basis}")
    print(f"Gain: {long_term_gain}")
    print("Data:")
    pprint(long_term_data)
    print("\n")


def get_data(csv_file_name: str) -> tuple[dict[str, AssetData], dict[str, AssetData]]:
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
            delta = end_date - start_date  # type: ignore

            if delta.days < 365:
                short_term_data[asset_name].proceeds += proceeds
                short_term_data[asset_name].cost_basis += cost_basis
            else:
                long_term_data[asset_name].proceeds += proceeds
                long_term_data[asset_name].cost_basis += cost_basis

    return short_term_data, long_term_data


def process_data(data: dict[str, AssetData]) -> tuple[float, float, float, dict[str, AssetData]]:
    total_proceeds: float = 0
    total_cost_basis: float = 0
    total_gain: float = 0

    for asset_data in data.values():
        proceeds = round(asset_data.proceeds)
        cost_basis = round(asset_data.cost_basis)

        asset_data.gain = proceeds - cost_basis

        total_proceeds += proceeds
        total_cost_basis += cost_basis
        total_gain += asset_data.gain

    return total_proceeds, total_cost_basis, total_gain, data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file_name")
    args = parser.parse_args()
    process_csv(args.csv_file_name)


if __name__ == "__main__":
    main()
