# data_loader.py
# This file loads and prepares GDP data

import pandas as pd
import json


def load_and_prepare_gdp_data():
    """
    Loads the raw GDP CSV file,
    reshapes it, cleans it,
    and returns ready-to-use data
    """

    try:
        # Load raw data
        raw_data = pd.read_csv("data/gdp_with_continent_filled.csv")

        # Find year columns (like '1960', '2020')
        year_columns = [col for col in raw_data.columns if col.isdigit()]

        # Columns to keep as they are
        id_columns = ["Country Name", "Continent"]

        # Reshape data from wide to long format
        data_long = pd.melt(
            raw_data,
            id_vars=id_columns,
            value_vars=year_columns,
            var_name="Year",
            value_name="Value"
        )

        # Remove rows with missing GDP
        data_long = data_long.dropna(subset=["Value"])

        # Fix data types
        data_long["Year"] = data_long["Year"].astype(int)
        data_long["Value"] = data_long["Value"].astype(float)

        # Rename Continent to Region
        data_long = data_long.rename(columns={"Continent": "Region"})

        return data_long

    except FileNotFoundError:
        print("❌ GDP file not found!")
        return None


def load_config():
    """
    Loads configuration from config.json
    """
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
        return config

    except FileNotFoundError:
        print("❌ config.json not found!")
        return None
