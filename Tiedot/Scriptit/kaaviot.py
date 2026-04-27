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

# Kaavio 1: saunan lämpeneminen (sauna2.csv)
sauna2 = pd.read_csv("sauna2.csv")
sauna2["Date"] = pd.to_datetime(sauna2["Date"])
sauna2 = sauna2.sort_values("Date")

session_start_s2 = sauna2[sauna2["Temperature (°C)"] > 25].iloc[0]["Date"]
sauna2["minutes"] = (sauna2["Date"] - session_start_s2).dt.total_seconds() / 60
sauna2 = sauna2[sauna2["minutes"] >= 0]

peak_idx = sauna2["Temperature (°C)"].idxmax()
peak_temp = sauna2.loc[peak_idx, "Temperature (°C)"]
peak_min = sauna2.loc[peak_idx, "minutes"]

fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=sauna2["minutes"],
    y=sauna2["Temperature (°C)"],
    name="Lämpötila (°C)",
    line=dict(color="tomato", width=2),
    hovertemplate="%{x:.0f} min<br>%{y:.1f} °C<extra></extra>"
))

fig1.add_annotation(
    x=peak_min, y=peak_temp,
    text=f"Huippu: {peak_temp:.1f} °C<br>{peak_min:.0f} min",
    showarrow=True, arrowhead=2, ay=-40
)

fig1.update_layout(
    title="Saunan lämpeneminen, kuinka kauan kuumeneminen kestää",
    autosize=True,
    xaxis=dict(title="Minuuttia istunnon alusta"),
    yaxis=dict(title="Lämpötila (°C)")
)
fig1.write_html("sauna6342.html", config={"responsive": True})
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

# Kaavio 4: saunatunnit kuukausittain
import calendar

data["above30"] = (data["Temperature (°C)"] > 30).astype(int)
data["session_id"] = (data["above30"].diff().fillna(0) != 0).cumsum()

monthly_hours = {}
for _, group in data[data["above30"] == 1].groupby("session_id"):
    duration_h = (group["Date"].max() - group["Date"].min()).total_seconds() / 3600
    if duration_h < 0.25:
        continue
    month = group["Date"].iloc[0].month
    monthly_hours[month] = monthly_hours.get(month, 0) + duration_h

months_sorted = sorted(monthly_hours.keys())
month_names = [calendar.month_abbr[m] for m in months_sorted]
hours_values = [monthly_hours[m] for m in months_sorted]

fig4 = go.Figure()
season_colors = {
    12: "#4fc3f7", 1: "#0288d1", 2: "#81d4fa",   # talvi - sininen
    3: "#a5d6a7", 4: "#66bb6a", 5: "#2e7d32",     # kevät - vihreä
    6: "#fff176", 7: "#ffd600", 8: "#ffb300",     # kesä - keltainen
    9: "#ffb74d", 10: "#e64a19", 11: "#795548",   # syksy - oranssi/ruskea
}

bar_colors = [season_colors[m] for m in months_sorted]

fig4.add_trace(go.Bar(
    x=month_names,
    y=hours_values,
    marker_color=bar_colors,
    hovertemplate="%{x}<br>%{y:.1f} h<extra></extra>"
))
fig4.update_layout(
    title=dict(
        text="Saunatunnit kuukausittain<br><sup>Data: 1.4.2025 – 3.3.2026</sup>",
    ),
    autosize=True,
    xaxis=dict(title="Kuukausi"),
    yaxis=dict(title="Tunnit (h)", rangemode="tozero")
)
fig4.write_html("sauna_per_month.html", config={"responsive": True})
fig4.show()
