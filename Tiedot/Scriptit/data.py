import pandas as pd
import plotly.express as px

data = pd.read_csv("Sauna.csv")

data["Date"] = pd.to_datetime(data["Date"])
data = data.sort_values("Date")

data["Sauna_on"] = data["Temperature (°C)"] > 25
data["Session_change"] = data["Sauna_on"].astype(int).diff()

session_starts = data[data["Session_change"] == 1]["Date"]
session_ends = data[data["Session_change"] == -1]["Date"]

sessions = list(zip(session_starts, session_ends))

heating_times = []
cooling_times = []
humidity_averages = []

for start, end in sessions:
    session_data = data[
        (data["Date"] >= start) &
        (data["Date"] <= end)
    ]

    max_temp_time = session_data.loc[
        session_data["Temperature (°C)"].idxmax(), "Date"
    ]

    heating_time = max_temp_time - start
    cooling_time = end - max_temp_time

    heating_times.append(heating_time)
    cooling_times.append(cooling_time)

    avg_humidity = session_data["Rel. humidity (%)"].mean()
    humidity_averages.append(avg_humidity)

heating_hours = []
cooling_hours = []

for t in heating_times:
    heating_hours.append(t.total_seconds() / 3600)

for t in cooling_times:
    cooling_hours.append(t.total_seconds() / 3600)

average_heating = sum(heating_hours) / len(heating_hours)
average_cooling = sum(cooling_hours) / len(cooling_hours)
average_humidity = sum(humidity_averages) / len(humidity_averages)

print("Keskimääräinen lämpenemisaika (h):", round(average_heating, 2))
print("Keskimääräinen jäähtymisaika (h):", round(average_cooling, 2))
print("Keskimääräinen kosteus (%):", round(average_humidity, 2))

data["Month"] = data["Date"].dt.month
data["Season"] = "Muu"

data.loc[data["Month"].isin([6, 7, 8]), "Season"] = "Kesä"
data.loc[data["Month"].isin([12, 1, 2]), "Season"] = "Talvi"

summer_data = data[data["Season"] == "Kesä"]
winter_data = data[data["Season"] == "Talvi"]

summer_temp_avg = summer_data["Temperature (°C)"].mean()
winter_temp_avg = winter_data["Temperature (°C)"].mean()

summer_humidity_avg = summer_data["Rel. humidity (%)"].mean()
winter_humidity_avg = winter_data["Rel. humidity (%)"].mean()

print("Kesän keskilämpötila:", round(summer_temp_avg, 2))
print("Talven keskilämpötila:", round(winter_temp_avg, 2))
print("Kesän keskikosteus:", round(summer_humidity_avg, 2))
print("Talven keskikosteus:", round(winter_humidity_avg, 2))

example_day = data[
    data["Date"].dt.date == pd.to_datetime("2025-08-30").date()
]
