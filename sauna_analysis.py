#!/usr/bin/env python3
"""
Sauna Performance Analysis
Analyzes temperature and humidity data from Sauna.csv to:
1. Compute baseline (room) temperature
2. Measure heating rate and time
3. Measure cooling rate and time
4. Analyze humidity changes during the cycle
5. Compute variance statistics

Outputs: saunastats.png with comprehensive analysis plots
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from datetime import datetime
import os

# Configuration
CSV_FILE = "/home/lab/projects/rouvi/Sauna.csv"
OUTPUT_DIR = "/home/lab/projects/rouvi/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "saunastats.png")

# Temperature thresholds for cycle detection
HEATING_THRESHOLD = 2.0  # °C above baseline to detect heating phase
COOLING_THRESHOLD = 1.5  # °C above baseline to detect cooling phase


def load_sauna_data(csv_path):
    """Load sauna data from CSV file."""
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    return df


def compute_baseline_temperature(temperature, method='lowest_10pct'):
    """
    Compute baseline (room) temperature.
    
    Args:
        temperature: Array of temperature values
        method: Method to compute baseline
                'lowest_10pct': Average of lowest 10% of temperatures
                'median': Median temperature
                'mode': Most frequent temperature (for step changes)
    
    Returns:
        baseline_temp: Baseline temperature in °C
    """
    if method == 'lowest_10pct':
        # Use lowest 10% of temperatures as baseline
        threshold = np.percentile(temperature, 10)
        baseline_temp = np.mean(temperature[temperature <= threshold])
    elif method == 'median':
        baseline_temp = np.median(temperature)
    else:
        # Use mode (most frequent value)
        from scipy import stats
        baseline_temp = stats.mode(temperature).mode[0]
    
    return baseline_temp


def detect_cycle_transitions(temperature, baseline, heating_threshold, cooling_threshold):
    """
    Detect heating and cooling transitions in temperature data.
    A heating cycle starts when temp rises above baseline+threshold and ends when it cools back down.
    
    Args:
        temperature: Temperature array
        baseline: Baseline temperature
        heating_threshold: Threshold above baseline to detect heating start
        cooling_threshold: Threshold above baseline to detect cooling end
    
    Returns:
        cycles: List of dicts with start, peak, end indices and durations
    """
    cycles = []
    i = 0
    n = len(temperature)
    
    while i < n:
        # Look for the start of a heating phase
        if temperature[i] > baseline + heating_threshold:
            start_idx = i
            
            # Find the peak temperature (hottest point)
            peak_idx = start_idx
            peak_temp = temperature[start_idx]
            
            # Keep going while temperature is rising or still above cooling threshold
            while i < n and temperature[i] > baseline + cooling_threshold:
                if temperature[i] > peak_temp:
                    peak_idx = i
                    peak_temp = temperature[i]
                i += 1
            
            end_idx = i - 1  # Last point above cooling threshold
            
            if end_idx > start_idx and peak_idx > start_idx:
                cycles.append({
                    'start': start_idx,
                    'peak': peak_idx,
                    'end': end_idx,
                    'peak_temp': peak_temp,
                    'heating_duration': None,
                    'cooling_duration': None,
                    'heating_rate': None,
                    'cooling_rate': None,
                    'humidity_start': None,
                    'humidity_peak': None,
                    'humidity_end': None
                })
        else:
            i += 1
    
    return cycles


def calculate_cycle_metrics(cycles, temperature, humidity, sample_rate=1.0):
    """
    Calculate heating and cooling rates for each cycle.
    
    Args:
        cycles: List of cycle dictionaries
        temperature: Temperature array
        humidity: Humidity array
        sample_rate: Sample rate in Hz
    
    Returns:
        Updated cycles list with metrics
    """
    for cycle in cycles:
        start = cycle['start']
        peak = cycle['peak']
        end = cycle['end']
        
        # Calculate heating duration and rate
        if peak > start:
            cycle['heating_duration'] = (peak - start) / sample_rate
            heating_data = temperature[start:peak+1]
            if len(heating_data) > 1:
                # Linear regression for heating rate
                x = np.arange(len(heating_data))
                coeffs = np.polyfit(x, heating_data, 1)
                cycle['heating_rate'] = coeffs[0] * sample_rate  # °C per second
            else:
                cycle['heating_rate'] = 0
        
        # Calculate cooling duration and rate
        if end > peak:
            cycle['cooling_duration'] = (end - peak) / sample_rate
            cooling_data = temperature[peak:end+1]
            if len(cooling_data) > 1:
                # Exponential decay fitting for cooling
                x = np.arange(len(cooling_data))
                # Simple linear approximation for cooling rate
                coeffs = np.polyfit(x, cooling_data, 1)
                cycle['cooling_rate'] = coeffs[0] * sample_rate  # °C per second
            else:
                cycle['cooling_rate'] = 0
        
        # Get humidity values
        cycle['humidity_start'] = humidity[start]
        cycle['humidity_peak'] = humidity[peak]
        cycle['humidity_end'] = humidity[end]
    
    return cycles


def compute_statistics(values):
    """Compute statistical measures."""
    if len(values) == 0:
        return {'mean': 0, 'std': 0, 'min': 0, 'max': 0, 'cv': 0}
    
    mean_val = np.mean(values)
    std_val = np.std(values)
    
    return {
        'mean': mean_val,
        'std': std_val,
        'min': np.min(values),
        'max': np.max(values),
        'cv': std_val / mean_val if mean_val != 0 else 0  # Coefficient of variation
    }


def create_analysis_plots(df, cycles, output_path):
    """
    Create comprehensive analysis visualization.
    
    Args:
        df: DataFrame with sauna data
        cycles: List of cycle dictionaries
        output_path: Path to save the plot
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Extract data
    timestamps = df['Date'].values
    temperature = df['Temperature (°C)'].values
    humidity = df['Rel. humidity (%)'].values
    time_numeric = (timestamps - timestamps[0]).astype('timedelta64[s]').astype(float)
    
    # Compute baseline
    baseline_temp = compute_baseline_temperature(temperature)
    
    # Compute statistics
    heating_rates = [c['heating_rate'] for c in cycles if c['heating_rate'] is not None]
    cooling_rates = [c['cooling_rate'] for c in cycles if c['cooling_rate'] is not None]
    heating_durations = [c['heating_duration'] for c in cycles if c['heating_duration'] is not None]
    cooling_durations = [c['cooling_duration'] for c in cycles if c['cooling_duration'] is not None]
    humidity_peaks = [c['humidity_peak'] for c in cycles]
    
    stats = {
        'heating_rate': compute_statistics(heating_rates),
        'cooling_rate': compute_statistics(cooling_rates),
        'heating_duration': compute_statistics(heating_durations),
        'cooling_duration': compute_statistics(cooling_durations),
        'humidity_peak': compute_statistics(humidity_peaks)
    }
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Temperature and Humidity over Time with cycle markers
    ax1 = fig.add_subplot(3, 2, 1)
    
    # Plot temperature
    ax1.plot(time_numeric, temperature, linewidth=0.8, color='red', label='Temperature (°C)')
    ax1.axhline(y=baseline_temp, color='gray', linestyle='--', alpha=0.5, label=f'Baseline: {baseline_temp:.2f}°C')
    
    # Mark cycles
    colors = plt.cm.rainbow(np.linspace(0, 1, len(cycles)))
    for i, cycle in enumerate(cycles):
        ax1.axvspan(time_numeric[cycle['start']], time_numeric[cycle['end']], 
                   alpha=0.1, color=colors[i], label=f'Cycle {i+1}' if i < 5 else None)
        ax1.plot(time_numeric[cycle['peak']], cycle['peak_temp'], 'ro', markersize=6)
    
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Temperature (°C)')
    ax1.set_title('Sauna Temperature Cycles')
    ax1.legend(loc='upper right', fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # Plot humidity on secondary axis
    ax1_twin = ax1.twinx()
    ax1_twin.plot(time_numeric, humidity, linewidth=0.8, color='blue', alpha=0.6, label='Humidity (%)')
    ax1_twin.set_ylabel('Humidity (%)', color='blue')
    ax1_twin.tick_params(axis='y', labelcolor='blue')
    ax1_twin.legend(loc='upper left', fontsize=8)
    
    # 2. Heating Rate Analysis
    ax2 = fig.add_subplot(3, 2, 2)
    if len(heating_rates) > 0:
        # Plot heating rates over cycles
        ax2.plot(range(1, len(heating_rates)+1), heating_rates, 'ro-', markersize=6, label='Heating Rate')
        ax2.axhline(y=stats['heating_rate']['mean'], color='red', linestyle='--', 
                   label=f'Mean: {stats["heating_rate"]["mean"]:.4f} °C/s')
        # Only add shaded region if we have more than 1 data point
        if len(heating_rates) > 1:
            ax2.fill_between(range(1, len(heating_rates)+1),
                            [stats['heating_rate']['mean'] - stats['heating_rate']['std']] * len(heating_rates),
                            [stats['heating_rate']['mean'] + stats['heating_rate']['std']] * len(heating_rates),
                            alpha=0.2, color='red', label='±1σ')
        ax2.set_xlabel('Cycle Number')
        ax2.set_ylabel('Heating Rate (°C/s)')
        ax2.set_title('Heating Rate Analysis')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'No heating cycles detected', ha='center', va='center', transform=ax2.transAxes)
    
    # 3. Cooling Rate Analysis
    ax3 = fig.add_subplot(3, 2, 3)
    if len(cooling_rates) > 0:
        # Plot cooling rates over cycles
        ax3.plot(range(1, len(cooling_rates)+1), cooling_rates, 'bo-', markersize=6, label='Cooling Rate')
        ax3.axhline(y=stats['cooling_rate']['mean'], color='blue', linestyle='--',
                   label=f'Mean: {stats["cooling_rate"]["mean"]:.4f} °C/s')
        # Only add shaded region if we have more than 1 data point
        if len(cooling_rates) > 1:
            ax3.fill_between(range(1, len(cooling_rates)+1),
                            [stats['cooling_rate']['mean'] - stats['cooling_rate']['std']] * len(cooling_rates),
                            [stats['cooling_rate']['mean'] + stats['cooling_rate']['std']] * len(cooling_rates),
                            alpha=0.2, color='blue', label='±1σ')
        ax3.set_xlabel('Cycle Number')
        ax3.set_ylabel('Cooling Rate (°C/s)')
        ax3.set_title('Cooling Rate Analysis')
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)
    else:
        ax3.text(0.5, 0.5, 'No cooling cycles detected', ha='center', va='center', transform=ax3.transAxes)
    
    # 4. Duration Analysis (Heating vs Cooling)
    ax4 = fig.add_subplot(3, 2, 4)
    if len(heating_durations) > 0 and len(cooling_durations) > 0:
        # Use the minimum length since they may differ slightly
        min_len = min(len(heating_durations), len(cooling_durations))
        width = 0.35
        x = np.arange(min_len)
        
        p1 = ax4.bar(x - width/2, heating_durations[:min_len], width, label='Heating (s)', color='red', alpha=0.7)
        p2 = ax4.bar(x + width/2, cooling_durations[:min_len], width, label='Cooling (s)', color='blue', alpha=0.7)
        
        ax4.set_xlabel('Cycle Number')
        ax4.set_ylabel('Duration (seconds)')
        ax4.set_title(f'Heating vs Cooling Duration per Cycle ({min_len} cycles)')
        ax4.legend(fontsize=8)
        ax4.grid(True, alpha=0.3, axis='y')
    else:
        ax4.text(0.5, 0.5, 'Insufficient data for duration analysis', ha='center', va='center', transform=ax4.transAxes)
    
    # 5. Humidity Analysis
    ax5 = fig.add_subplot(3, 2, 5)
    if len(humidity_peaks) > 0:
        ax5.plot(range(1, len(humidity_peaks)+1), humidity_peaks, 'go-', markersize=6, label='Peak Humidity (%)')
        ax5.axhline(y=stats['humidity_peak']['mean'], color='green', linestyle='--',
                   label=f'Mean: {stats["humidity_peak"]["mean"]:.2f}%')
        # Only add shaded region if we have more than 1 data point
        if len(humidity_peaks) > 1:
            ax5.fill_between(range(1, len(humidity_peaks)+1),
                            [stats['humidity_peak']['mean'] - stats['humidity_peak']['std']] * len(humidity_peaks),
                            [stats['humidity_peak']['mean'] + stats['humidity_peak']['std']] * len(humidity_peaks),
                            alpha=0.2, color='green', label='±1σ')
        ax5.set_xlabel('Cycle Number')
        ax5.set_ylabel('Humidity (%)')
        ax5.set_title('Humidity During Heating Phase')
        ax5.legend(fontsize=8)
        ax5.grid(True, alpha=0.3)
    else:
        ax5.text(0.5, 0.5, 'No humidity data available', ha='center', va='center', transform=ax5.transAxes)
    
    # 6. Scientific Variance Analysis (Coefficient of Variation)
    ax6 = fig.add_subplot(3, 2, 6)
    metrics = ['Heating Rate', 'Cooling Rate', 'Heating Duration', 'Cooling Duration', 'Humidity']
    cv_values = [
        stats['heating_rate']['cv'] * 100 if stats['heating_rate']['cv'] > 0 else 0,
        stats['cooling_rate']['cv'] * 100 if stats['cooling_rate']['cv'] > 0 else 0,
        stats['heating_duration']['cv'] * 100 if stats['heating_duration']['cv'] > 0 else 0,
        stats['cooling_duration']['cv'] * 100 if stats['cooling_duration']['cv'] > 0 else 0,
        stats['humidity_peak']['cv'] * 100 if stats['humidity_peak']['cv'] > 0 else 0
    ]
    colors = ['red', 'blue', 'red', 'blue', 'green']
    
    bars = ax6.bar(metrics, cv_values, color=colors, alpha=0.7, edgecolor='black')
    ax6.set_ylabel('Coefficient of Variation (%)')
    ax6.set_title('Scientific Variance Analysis (CV%)')
    ax6.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, cv in zip(bars, cv_values):
        ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{cv:.2f}%', ha='center', va='bottom', fontsize=9)
    
    # Adjust top bar for proper visibility
    max_cv = max(cv_values) if cv_values else 10
    ax6.set_ylim(0, max_cv * 1.3)
    
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Analysis plot saved to: {output_path}")
    
    return {
        'baseline_temp': baseline_temp,
        'num_cycles': len(cycles),
        'stats': stats
    }


def print_analysis_summary(results):
    """Print summary of the analysis."""
    stats = results['stats']
    
    print("\n" + "="*60)
    print("SAUNA PERFORMANCE ANALYSIS SUMMARY")
    print("="*60)
    print(f"\nBaseline Temperature: {results['baseline_temp']:.2f} °C")
    print(f"Cycles Detected: {results['num_cycles']}")
    
    print("\n--- Heating Analysis ---")
    print(f"  Mean Heating Rate: {stats['heating_rate']['mean']:.6f} °C/s")
    print(f"  Std Dev: {stats['heating_rate']['std']:.6f} °C/s")
    print(f"  CV: {stats['heating_rate']['cv']*100:.2f}%")
    print(f"  Mean Heating Duration: {stats['heating_duration']['mean']:.2f} seconds")
    print(f"  Std Dev: {stats['heating_duration']['std']:.2f} seconds")
    
    print("\n--- Cooling Analysis ---")
    print(f"  Mean Cooling Rate: {stats['cooling_rate']['mean']:.6f} °C/s")
    print(f"  Std Dev: {stats['cooling_rate']['std']:.6f} °C/s")
    print(f"  CV: {stats['cooling_rate']['cv']*100:.2f}%")
    print(f"  Mean Cooling Duration: {stats['cooling_duration']['mean']:.2f} seconds")
    print(f"  Std Dev: {stats['cooling_duration']['std']:.2f} seconds")
    
    print("\n--- Humidity Analysis ---")
    print(f"  Mean Peak Humidity: {stats['humidity_peak']['mean']:.2f}%")
    print(f"  Std Dev: {stats['humidity_peak']['std']:.2f}%")
    print(f"  CV: {stats['humidity_peak']['cv']*100:.2f}%")
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60)


def main():
    """Main function to run the sauna analysis."""
    print("Loading sauna data...")
    df = load_sauna_data(CSV_FILE)
    print(f"Loaded {len(df)} samples from {df['Date'].min()} to {df['Date'].max()}")
    
    # Detect cycles
    print("\nDetecting sauna cycles...")
    baseline_temp = compute_baseline_temperature(df['Temperature (°C)'].values)
    print(f"Baseline temperature: {baseline_temp:.2f} °C")
    
    cycles = detect_cycle_transitions(
        df['Temperature (°C)'].values,
        baseline_temp,
        HEATING_THRESHOLD,
        COOLING_THRESHOLD
    )
    print(f"Detected {len(cycles)} sauna cycles")
    
    if len(cycles) == 0:
        print("No cycles detected. Adjust thresholds or check data.")
        return
    
    # Calculate metrics
    print("\nCalculating cycle metrics...")
    # Estimate sample rate from time differences
    time_numeric = (df['Date'].values - df['Date'].values[0]).astype('timedelta64[s]').astype(float)
    time_diffs = np.diff(time_numeric)
    sample_rate = 1.0 / np.median(time_diffs) if np.median(time_diffs) > 0 else 0.1
    
    cycles = calculate_cycle_metrics(cycles, df['Temperature (°C)'].values, 
                                     df['Rel. humidity (%)'].values, sample_rate)
    
    # Create plots
    print("\nGenerating analysis plots...")
    results = create_analysis_plots(df, cycles, OUTPUT_FILE)
    
    print_analysis_summary(results)


if __name__ == "__main__":
    main()