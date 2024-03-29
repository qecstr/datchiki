import serial
import requests

# Establish serial connection
ser = serial.Serial('COM3', 9600)  # Adjust the port as per your Arduino

# Read data from Arduino
while True:
    if ser.in_waiting > 0:
        data = ser.readline().strip()
        print("Received data from Arduino:", data)

        # Send data to FastAPI backend
        # Make sure to adjust the URL and data format as per your API
        response = requests.post("http://localhost:8000/data", json={"sensor_value": str(data)})
        print(response.json())