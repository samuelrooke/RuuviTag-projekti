import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def analyze_sauna_session(input_file):
    if not os.path.exists(input_file):
        print(f"Virhe: Tiedostoa '{input_file}' ei löydy.")
        return

    df = pd.read_csv(input_file)
    columns = ['Date', 'Temperature (°C)', 'Rel. humidity (%)', 'Abs. humidity (g/m³)']
    df = df[columns].copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)

    active_mask = df['Temperature (°C)'] > 28.0
    if not active_mask.any():
        print("Saunomissessiota ei löytynyt.")
        return
    
    df_s = df.iloc[max(0, active_mask.idxmax()-15) : min(len(df), active_mask[::-1].idxmax()+45)].copy()

    df_s['Abs_Change'] = df_s['Abs. humidity (g/m³)'].diff()
    loyly_indices = []
    last_time = None
    
    for idx, row in df_s.iterrows():
        if row['Abs_Change'] > 0.8 and row['Temperature (°C)'] > 55:
            if last_time is None or (row['Date'] - last_time).total_seconds() > 180:
                loyly_indices.append(idx)
                last_time = row['Date']

    df_loylyt = df_s.loc[loyly_indices]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df_s['Date'], y=df_s['Temperature (°C)'], 
                             name="Lämpötila (°C)", 
                             line=dict(color='red', width=3)), 
                  secondary_y=False)

    fig.add_trace(go.Scatter(x=df_s['Date'], y=df_s['Abs. humidity (g/m³)'], 
                             name="Abs. kosteus (g/m³)", 
                             line=dict(color='blue', width=2, dash='dot')), 
                  secondary_y=True)

    fig.add_trace(go.Scatter(x=df_s['Date'], y=df_s['Rel. humidity (%)'], 
                             name="Suht. kosteus (%)", 
                             line=dict(color='rgba(0, 150, 255, 0.6)', width=2)), 
                  secondary_y=True)

    if not df_loylyt.empty:
        fig.add_trace(go.Scatter(x=df_loylyt['Date'], y=df_loylyt['Abs. humidity (g/m³)'],
                                 mode='markers+text', 
                                 name=f'Löylyt ({len(df_loylyt)} kpl)',
                                 text=[f"Löyly {i+1}" for i in range(len(df_loylyt))],
                                 textposition="top center",
                                 marker=dict(color='orange', size=14, symbol='star', 
                                            line=dict(width=1, color='black'))), 
                      secondary_y=True)

    fig.update_layout(
        title="Sauna-analyysi: yksi saunakerta, Lämpötila ja kosteussuhteet", 
        template="plotly_white", 
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_yaxes(title_text="Lämpötila (°C)", secondary_y=False)
    fig.update_yaxes(title_text="Kosteus ($g/m^3$ ja %)", secondary_y=True)
    fig.update_xaxes(tickformat="%H:%M")
    
    fig.write_html('sauna.html')

if __name__ == "__main__":
    analyze_sauna_session("sauna_full.csv")