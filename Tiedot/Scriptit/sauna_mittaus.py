import pandas as pd
import matplotlib.pyplot as plt

# --- SÄÄDÄ NÄMÄ ARVOT TESTIAJON PERUSTEELLA ---
REKISTERÖITY_ALALAUDE = 45.0  # Mitä Ruuvi näytti
TODELLINEN_YLALAUDE = 80.0    # Mitä seinämittari näytti samaan aikaan
KERROIN = TODELLINEN_YLALAUDE / REKISTERÖITY_ALALAUDE

def main():
    # 1. Ladataan data
    df = pd.read_csv('Sauna.csv')
    df['Date'] = pd.to_datetime(df['Date'])

    # 2. Lasketaan ennuste ylälauteelle
    # Kaava: Mitattu lämpö * kerroin + pieni löylylisä kosteudesta
    df['Ennuste'] = df.apply(lambda r: round((r['Temperature (°C)'] * KERROIN) + (r['Rel. humidity (%)'] * 0.1), 1) 
                             if r['Temperature (°C)'] > 25 else r['Temperature (°C)'], axis=1)

    # 3. Otetaan tarkasteluun vain viimeisin saunomiskerta
    viimeisin_sessio = df[df['Temperature (°C)'] > 30].tail(50) # Viimeiset 50 riviä kun sauna kuuma

    # 4. Tehdään kuvaaja luokalle näytettäväksi
    plt.figure(figsize=(10, 5))
    plt.plot(viimeisin_sessio['Date'], viimeisin_sessio['Temperature (°C)'], label='Alalaude (Ruuvi)', color='blue')
    plt.plot(viimeisin_sessio['Date'], viimeisin_sessio['Ennuste'], label='Ylälaude (Ennuste)', color='red', linestyle='--')
    
    plt.title('Saunaprojekti: Lämpötilaennuste')
    plt.legend()
    plt.savefig('saunakuva.png')
    
    print(f"Valmis! Korkein ennustettu lämpö: {viimeisin_sessio['Ennuste'].max()}°C")
    print("Kuvaaja tallennettu: saunakuva.png")

if __name__ == "__main__":
    main()