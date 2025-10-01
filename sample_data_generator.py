"""
Sample Dataset Generator for Tricycle Fare Prediction
=====================================================
This script generates a synthetic dataset for testing the model
when you don't have real data yet.
"""

import pandas as pd
import numpy as np

def generate_sample_data(n_samples=500, output_file='tricycle_fare_data.csv'):
    """
    Generate synthetic tricycle fare data
    
    Args:
        n_samples (int): Number of samples to generate
        output_file (str): Output CSV filename
    """
    print(f"Generating {n_samples} synthetic fare records...")
    
    np.random.seed(42)
    
    # Define possible values
    fuel_prices = ["20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99", "100&up"]
    times_of_day = ["Rush Hour Morning", "Off-Peak", "Rush Hour Evening"]
    weather_conditions = ["Sunny", "Rainy"]
    vehicle_types = ["Single Motor", "Tricycle"]
    
    # Generate random data
    data = {
        'Distance_km': np.random.uniform(0.5, 15.0, n_samples).round(2),
        'Fuel_Price': np.random.choice(fuel_prices, n_samples),
        'Time_of_Day': np.random.choice(times_of_day, n_samples),
        'Weather': np.random.choice(weather_conditions, n_samples),
        'Vehicle_Type': np.random.choice(vehicle_types, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate fare using a realistic formula
    # Base fare calculation with various factors
    
    # Handle fuel price conversion (special case for "100&up")
    def convert_fuel_price(price_range):
        if price_range == "100&up":
            return 100.0
        else:
            return float(price_range.split('-')[0])
    
    df['Fuel_Price_Numeric'] = df['Fuel_Price'].apply(convert_fuel_price)
    
    df['Actual_Fare_PHP'] = (
        10.0 +                                                          # Base fare
        (df['Distance_km'] * 8.0) +                                    # Distance factor
        (df['Fuel_Price_Numeric'] * 0.1) +                             # Fuel price factor
        (df['Time_of_Day'].map({
            'Rush Hour Morning': 5.0,
            'Off-Peak': 0.0,
            'Rush Hour Evening': 7.0
        })) +
        (df['Weather'].map({
            'Sunny': 0.0,
            'Rainy': 5.0
        })) +
        (df['Vehicle_Type'].map({
            'Single Motor': 0.0,
            'Tricycle': 5.0
        }))
    )
    
    # Drop the temporary numeric column
    df = df.drop('Fuel_Price_Numeric', axis=1)
    
    # Add some random noise to make it realistic
    noise = np.random.normal(0, 2, n_samples)
    df['Actual_Fare_PHP'] = (df['Actual_Fare_PHP'] + noise).clip(lower=10.0).round(2)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    
    print(f"✅ Dataset generated successfully!")
    print(f"   File: {output_file}")
    print(f"   Samples: {len(df)}")
    print(f"\nSample records:")
    print(df.head(10))
    print(f"\nStatistics:")
    print(df.describe())
    
    return df

if __name__ == '__main__':
    generate_sample_data(n_samples=500)
