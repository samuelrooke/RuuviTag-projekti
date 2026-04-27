import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv("Sauna.csv")

data["Date"] = pd.to_datetime(data["Date"])
data = data.sort_values("Date")
data["Month"] = data["Date"].dt.month

# Saunomiskertojen tunnistus
data["Sauna_on"] = data["Temperature (°C)"] > 25
data["Session_change"] = data["Sauna_on"].astype(int).diff()

session_starts = data[data["Session_change"] == 1]["Date"]
session_ends = data[data["Session_change"] == -1]["Date"]

sessions = list(zip(session_starts, session_ends))

# Lämpeneminen, jäähtyminen ja kosteus
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

    heating_times.append(heating_time.total_seconds() / 3600)
    cooling_times.append(cooling_time.total_seconds() / 3600)
    humidity_averages.append(session_data["Rel. humidity (%)"].mean())

average_heating = sum(heating_times) / len(heating_times)
average_cooling = sum(cooling_times) / len(cooling_times)
average_humidity = sum(humidity_averages) / len(humidity_averages)

# Kaavio 1: saunan toiminta
fig1 = go.Figure()

fig1.add_trace(
    go.Bar(
        x=["Lämpeneminen", "Jäähtyminen"],
        y=[average_heating, average_cooling],
        name="Aika (h)",
        yaxis="y"
    )
)

fig1.add_trace(
    go.Bar(
        x=["Kosteus"],
        y=[average_humidity],
        name="Kosteus (%)",
        yaxis="y2"
    )
)

fig1.update_layout(
    title="Saunan lämpeneminen, jäähtyminen ja keskimääräinen kosteus",
    xaxis=dict(title="Mittari"),
    yaxis=dict(title="Aika (h)"),
    yaxis2=dict(
        title="Kosteus (%)",
        overlaying="y",
        side="right"
    )
)

fig1.show()

# Kaavio 2: yksi saunomiskerta
example_day = data[
    data["Date"].dt.date == pd.to_datetime("2025-08-30").date()
]

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=example_day["Date"],
        y=example_day["Temperature (°C)"],
        name="Lämpötila (°C)",
        yaxis="y"
    )
)

fig2.add_trace(
    go.Scatter(
        x=example_day["Date"],
        y=example_day["Rel. humidity (%)"],
        name="Kosteus (%)",
        yaxis="y2"
    )
)

fig2.update_layout(
    title="Saunomiskerta 30.8.2025 – lämpötila ja kosteus",
    xaxis=dict(title="Aika"),
    yaxis=dict(title="Lämpötila (°C)"),
    yaxis2=dict(
        title="Kosteus (%)",
        overlaying="y",
        side="right"
    )
)

fig2.write_html("saunomiskerta.html")
fig2.show()

# Kaavio 3: kesä ja talvi samassa aikasarjassa
summer_data = data[data["Month"].isin([6, 7, 8])]
winter_data = data[data["Month"].isin([12, 1, 2])]

fig3 = go.Figure()

# Kesä lämpötila
fig3.add_trace(
    go.Scatter(
        x=summer_data["Date"],
        y=summer_data["Temperature (°C)"],
        name="Kesä lämpötila",
        line=dict(color="blue", width=2),
        yaxis="y"
    )
)

# Talvi lämpötila
fig3.add_trace(
    go.Scatter(
        x=winter_data["Date"],
        y=winter_data["Temperature (°C)"],
        name="Talvi lämpötila",
        line=dict(color="red", width=2),
        yaxis="y"
    )
)

# Kesä kosteus
fig3.add_trace(
    go.Scatter(
        x=summer_data["Date"],
        y=summer_data["Rel. humidity (%)"],
        name="Kesä kosteus",
        line=dict(color="green", width=2),
        yaxis="y2"
    )
)

# Talvi kosteus
fig3.add_trace(
    go.Scatter(
        x=winter_data["Date"],
        y=winter_data["Rel. humidity (%)"],
        name="Talvi kosteus",
        line=dict(color="purple", width=2),
        yaxis="y2"
    )
)

fig3.update_layout(
    title="Kesä ja talvi – lämpötila ja kosteus ajan mukaan",
    xaxis=dict(
        title="Aika",
        rangebreaks=[
            dict(bounds=["2025-09-01", "2025-12-01"])
        ]
    ),
    yaxis=dict(title="Lämpötila (°C)"),
    yaxis2=dict(
        title="Kosteus (%)",
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0.01, y=0.99)
)

fig3.write_html("kesa_talvi.html")
fig3.show()
