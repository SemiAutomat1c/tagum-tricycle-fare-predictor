"""
API Testing Script for Tricycle Fare Optimizer
==============================================
Simple script to test the backend API endpoints
"""

import requests
import json
import sys

# Configuration
BASE_URL = 'http://localhost:5000'

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    print(f"GET {BASE_URL}/")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Health check passed\n")
            return True
        else:
            print("❌ Health check failed\n")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        print("   Run: cd backend && python app.py\n")
        return False
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


def test_prediction(data):
    """Test the prediction endpoint"""
    print("Testing prediction endpoint...")
    print(f"POST {BASE_URL}/predict")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            if 'predicted_fare' in result:
                print(f"✅ Prediction successful: ₱{result['predicted_fare']:.2f}\n")
                return True
            else:
                print("❌ Invalid response format\n")
                return False
        else:
            print("❌ Prediction failed\n")
            return False
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


def run_all_tests():
    """Run all API tests"""
    print("="*50)
    print("Tricycle Fare Optimizer - API Tests")
    print("="*50)
    print()
    
    # Test 1: Health check
    health_ok = test_health_check()
    if not health_ok:
        print("Cannot proceed with further tests. Please start the backend server.")
        sys.exit(1)
    
    # Test 2: Valid prediction
    print("-" * 50)
    print("Test 2: Valid Prediction")
    print("-" * 50)
    valid_data = {
        "Distance_km": 5.5,
        "Fuel_Price": "60-69",
        "Time_of_Day": "Rush Hour Morning",
        "Weather": "Sunny",
        "Vehicle_Type": "Tricycle"
    }
    test_prediction(valid_data)
    
    # Test 3: Different scenario
    print("-" * 50)
    print("Test 3: Off-Peak, Rainy, Single Motor")
    print("-" * 50)
    scenario_2 = {
        "Distance_km": 3.2,
        "Fuel_Price": "40-49",
        "Time_of_Day": "Off-Peak",
        "Weather": "Rainy",
        "Vehicle_Type": "Single Motor"
    }
    test_prediction(scenario_2)
    
    # Test 4: Long distance
    print("-" * 50)
    print("Test 4: Long Distance")
    print("-" * 50)
    scenario_3 = {
        "Distance_km": 12.8,
        "Fuel_Price": "80-89",
        "Time_of_Day": "Rush Hour Evening",
        "Weather": "Rainy",
        "Vehicle_Type": "Tricycle"
    }
    test_prediction(scenario_3)
    
    # Test 5: Invalid data (missing field)
    print("-" * 50)
    print("Test 5: Invalid Data (Missing Field)")
    print("-" * 50)
    invalid_data = {
        "Distance_km": 5.0,
        "Fuel_Price": "60-69",
        # Missing Time_of_Day
        "Weather": "Sunny",
        "Vehicle_Type": "Tricycle"
    }
    test_prediction(invalid_data)
    
    # Test 6: Invalid fuel price
    print("-" * 50)
    print("Test 6: Invalid Fuel Price")
    print("-" * 50)
    invalid_fuel = {
        "Distance_km": 5.0,
        "Fuel_Price": "invalid-price",
        "Time_of_Day": "Off-Peak",
        "Weather": "Sunny",
        "Vehicle_Type": "Tricycle"
    }
    test_prediction(invalid_fuel)
    
    print("="*50)
    print("All Tests Complete!")
    print("="*50)


if __name__ == '__main__':
    # Check if requests library is installed
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library not found")
        print("Install it with: pip install requests")
        sys.exit(1)
    
    # Allow custom base URL via command line
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
        print(f"Using custom base URL: {BASE_URL}\n")
    
    run_all_tests()
