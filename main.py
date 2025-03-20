import streamlit as st
from pint import UnitRegistry
import re
import json
from datetime import datetime
import plotly.graph_objects as go
import numpy as np

ureg = UnitRegistry()

UNIT_CATEGORIES = {
    'Length': {
        'meters': 'm',
        'kilometers': 'km',
        'centimeters': 'cm',
        'millimeters': 'mm',
        'inches': 'in',
        'feet': 'ft',
        'yards': 'yd',
        'miles': 'mi',
        'nautical miles': 'nmi',
        'light years': 'ly'
    },
    'Weight': {
        'kilograms': 'kg',
        'grams': 'g',
        'milligrams': 'mg',
        'pounds': 'lb',
        'ounces': 'oz',
        'metric tons': 't',
        'carats': 'ct'
    },
    'Temperature': {
        'celsius': 'degC',
        'fahrenheit': 'degF',
        'kelvin': 'K',
        'rankine': 'degR'
    },
    'Volume': {
        'liters': 'L',
        'milliliters': 'mL',
        'cubic meters': 'm³',
        'gallons': 'gal',
        'quarts': 'qt',
        'pints': 'pt',
        'cups': 'cup',
        'fluid ounces': 'fl_oz',
        'cubic feet': 'ft³',
        'cubic inches': 'in³'
    },
    'Area': {
        'square meters': 'm²',
        'square kilometers': 'km²',
        'square centimeters': 'cm²',
        'square inches': 'in²',
        'square feet': 'ft²',
        'square yards': 'yd²',
        'acres': 'ac',
        'hectares': 'ha'
    },
    'Speed': {
        'meters per second': 'm/s',
        'kilometers per hour': 'km/h',
        'miles per hour': 'mph',
        'knots': 'knot',
        'feet per second': 'ft/s'
    },
    'Energy': {
        'joules': 'J',
        'kilojoules': 'kJ',
        'calories': 'cal',
        'kilocalories': 'kcal',
        'watt hours': 'W*h',
        'electron volts': 'eV'
    },
    'Power': {
        'watts': 'W',
        'kilowatts': 'kW',
        'megawatts': 'MW',
        'horsepower': 'hp',
        'BTU per hour': 'BTU/h'
    }
}

PRESETS = {
    'Common Lengths': {
        'Human Height (5\'10")': '1.78 m',
        'Football Field': '91.44 m',
        'Marathon': '42.195 km',
        'Earth Diameter': '12742 km'
    },
    'Common Temperatures': {
        'Room Temperature': '20 °C',
        'Body Temperature': '37 °C',
        'Water Boiling Point': '100 °C',
        'Absolute Zero': '0 K'
    },
    'Common Volumes': {
        'Water Bottle': '500 mL',
        'Soda Can': '330 mL',
        'Gallon of Milk': '3.785 L',
        'Olympic Pool': '2500000 L'
    }
}

def convert_units(value, from_unit, to_unit):
    try:
        quantity = value * ureg(from_unit)
        result = quantity.to(to_unit)
        return result.magnitude
    except Exception as e:
        return None

def create_comparison_chart(value, from_unit, to_unit, category):
    try:
        units = UNIT_CATEGORIES[category]
        
        converted_values = {}
        for unit_name, unit_symbol in units.items():
            if unit_symbol != from_unit:
                converted_value = convert_units(value, from_unit, unit_symbol)
                if converted_value is not None:
                    converted_values[unit_name] = converted_value
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=list(converted_values.keys()),
            y=list(converted_values.values()),
            text=[f"{v:.2f}" for v in converted_values.values()],
            textposition='auto',
            name=f"{value} {from_unit}"
        ))
        
        fig.update_layout(
            title=f"Comparison of {value} {from_unit} in Different Units",
            xaxis_title="Unit",
            yaxis_title="Value",
            showlegend=False,
            height=400
        )
        
        return fig
    except Exception as e:
        return None

def main():
    st.set_page_config(
        page_title="Universal Unit Converter",
        page_icon="📏",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    if 'conversion_history' not in st.session_state:
        st.session_state.conversion_history = []
    
    st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #1F77B4;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #2C8AC0;
        }
        .stSelectbox>div>div>select {
            background-color: #1F1F1F;
            color: white;
            border: 1px solid #2C2C2C;
        }
        .stNumberInput>div>div>input {
            background-color: #1F1F1F;
            color: white;
            border: 1px solid #2C2C2C;
        }
        .stSidebar {
            background-color: #0E1117;
        }
        .stMarkdown {
            color: #FFFFFF;
        }
        .stSuccess {
            background-color: #1F1F1F;
            color: #4CAF50;
        }
        .stError {
            background-color: #1F1F1F;
            color: #f44336;
        }
        .stInfo {
            background-color: #1F1F1F;
            color: #2196F3;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #0E1117;
        }
        .stTabs [data-baseweb="tab"] {
            color: #FFFFFF;
        }
        
        </style>
    """, unsafe_allow_html=True)
    
   
    with st.sidebar:
        st.title("⚙️ Settings")
        use_scientific = st.checkbox("Use Scientific Notation", value=False)
        
        st.title("📜 History")
        for i, conv in enumerate(st.session_state.conversion_history[-5:]):
            st.write(f"{conv['from_value']} {conv['from_unit']} → {conv['to_value']:.4f} {conv['to_unit']}")
            st.write(f"*{conv['timestamp']}*")
            st.write("---")
        
        if st.button("Clear History"):
            st.session_state.conversion_history = []
            st.experimental_rerun()
    
    st.title("📏 Universal Unit Converter")
    st.write("Convert between different units of measurement easily!")
    
    tab1, tab2 = st.tabs(["Converter", "Presets"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Select Category", list(UNIT_CATEGORIES.keys()))
            
            units = UNIT_CATEGORIES[category]
            
            value = st.number_input(
                "Enter Value",
                min_value=0.0,
                value=1.0,
                step=0.1,
                format="%.10f" if use_scientific else "%.2f"
            )
            
            from_unit = st.selectbox("From Unit", list(units.keys()))
        
        with col2:
            to_unit = st.selectbox("To Unit", list(units.keys()))
            
            if st.button("Convert", key="convert_btn"):
                if from_unit != to_unit:
                    result = convert_units(value, units[from_unit], units[to_unit])
                    if result is not None:
                        formatted_result = f"{result:.10e}" if use_scientific else f"{result:.4f}"
                        st.success(f"{value} {from_unit} = {formatted_result} {to_unit}")
                        
                        st.session_state.conversion_history.append({
                            'from_value': value,
                            'from_unit': from_unit,
                            'to_value': result,
                            'to_unit': to_unit,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        chart = create_comparison_chart(value, units[from_unit], units[to_unit], category)
                        if chart:
                            st.plotly_chart(chart, use_container_width=True)
                    else:
                        st.error("Conversion failed. Please check the units and try again.")
                else:
                    st.info("Please select different units for conversion.")
    
    with tab2:
        st.title("Common Conversion Presets")
        preset_category = st.selectbox("Select Preset Category", list(PRESETS.keys()))
        
        presets = PRESETS[preset_category]
        cols = st.columns(2)
        
        for i, (name, value) in enumerate(presets.items()):
            with cols[i % 2]:
                if st.button(name):
                    match = re.match(r"([\d.]+)\s*([^\s]+)", value)
                    if match:
                        preset_value, preset_unit = match.groups()
                        st.session_state.preset_value = float(preset_value)
                        st.session_state.preset_unit = preset_unit
                        st.experimental_rerun()
    
    st.markdown("---")
    st.markdown("""
    ### Keyboard Shortcuts
    - `Ctrl/Cmd + Enter`: Convert
    - `Ctrl/Cmd + R`: Reset
    - `Ctrl/Cmd + H`: Toggle History
    """)
    
    st.markdown("""
    ### Tips:
    - Select a category from the dropdown menu
    - Enter the value you want to convert
    - Choose the source unit (From Unit)
    - Choose the target unit (To Unit)
    - Click Convert to see the result
    - Use presets for common conversions
    - Toggle scientific notation in settings
    - View conversion history in the sidebar
    """)

if __name__ == "__main__":
    main() 