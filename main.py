import requests
import pandas as pd
import time

base = "https://api.openf1.org/v1"

sessions = requests.get(
    f"{base}/sessions",
    params={
        "year": 2025,
        "country_name": "Bahrain",
        "session_name": "Race"
    },
    timeout=30
)
sessions.raise_for_status()

session_key = sessions.json()[0]["session_key"]


def fetch_data(endpoint):
    response = requests.get(
        f"{base}/{endpoint}",
        params={"session_key": session_key},
        timeout=120
    )
    response.raise_for_status()
    time.sleep(1)  
    return pd.DataFrame(response.json())


stints = fetch_data("stints")
weather = fetch_data("weather")
pit_stops = fetch_data("pit")
laps=fetch_data("laps")
stints.to_csv("bahrain_2025_stints.csv", index=False)
weather.to_csv("bahrain_2025_weather.csv", index=False)
pit_stops.to_csv("bahrain_2025_pit_stops.csv", index=False)
laps.to_csv("bahrain_2025_laps.csv", index=False)

for name, df in [
    ("Laps", laps),
    ("Stints", stints),
    ("Weather", weather),
    ("Pit Stops", pit_stops)
]:
    print(f"\n{name}: {df.shape}")
    print(df.columns.tolist())
    print(df.head(3).to_string(index=False))

