# Universal Unit Converter

A modern web application for converting between different units of measurement. Built with Python and Streamlit.

## Features

- Convert between different units in various categories:
  - Length (meters, kilometers, inches, feet, yards, miles, nautical miles, light years)
  - Weight (kilograms, grams, milligrams, pounds, ounces, metric tons, carats)
  - Temperature (Celsius, Fahrenheit, Kelvin, Rankine)
  - Volume (liters, milliliters, cubic meters, gallons, quarts, pints, cups, fluid ounces, cubic feet, cubic inches)
  - Area (square meters, square kilometers, square centimeters, square inches, square feet, square yards, acres, hectares)
  - Speed (meters per second, kilometers per hour, miles per hour, knots, feet per second)
  - Energy (joules, kilojoules, calories, kilocalories, watt hours, electron volts)
  - Power (watts, kilowatts, megawatts, horsepower, BTU per hour)
- Clean and intuitive user interface with dark mode
- Real-time conversion with visual comparison charts
- Support for decimal values and scientific notation
- Conversion history tracking
- Common conversion presets
- Keyboard shortcuts for efficiency

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run main.py
   ```
2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)
3. Select a category from the dropdown menu
4. Enter the value you want to convert
5. Choose the source unit (From Unit)
6. Choose the target unit (To Unit)
7. Click the Convert button to see the result
8. Use the Presets tab for quick access to common measurements
9. View your conversion history in the sidebar
10. Toggle scientific notation in settings if needed

## Requirements

- Python 3.7 or higher
- Streamlit 1.32.0
- Pint 0.22 (Python package for handling physical quantities)
- Plotly 5.19.0 (for visualization)
- NumPy 1.26.4 (for numerical operations) 