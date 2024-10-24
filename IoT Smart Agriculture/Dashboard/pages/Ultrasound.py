import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set page configuration to wide mode
st.set_page_config(page_title="Smart Agriculture Dashboard", layout="wide")


def get_file_path(filename):
    """
    Constructs the absolute path to the data file.

    Args:
        filename (str): The name of the data file (e.g., "cleaned_data.csv").

    Returns:
        str: The absolute path to the data file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)


def load_data(file_path):
    """
    Loads the data from the specified file path.

    Args:
        file_path (str): The absolute path to the data file.

    Returns:
        pandas.DataFrame: The loaded data as a pandas DataFrame.
    """
    data = pd.read_csv(file_path)
    # Add any necessary data processing steps here (e.g., handling missing values)
    # ...
    return data


def get_data_path():
    """
    This function retrieves the data path from an environment variable or a default location.

    Returns:
        str: Path to the CSV file.
    """
    data_path = os.environ.get("DATA_PATH", "./cleaned_data.csv")
    return data_path


# Load custom CSS
css_file_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
with open(css_file_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Get the data path
data_path = get_data_path()

# Load the data
data = load_data(get_file_path(data_path))
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Filter for Ultrasound (US)
us_data = data[['timestamp', 'US']]

# Page title
st.title("Ultrasound (US) Visualizations")

# Page title
st.markdown("<div class='card1'><h3>Choose a Visualizations</h3></div>", unsafe_allow_html=True)

# Initialize or get the session state to track the current chart type
if 'current_chart' not in st.session_state:
    st.session_state.current_chart = 'line'

# Arrange buttons in a single row
col1, col2, col3, col4 = st.columns(4)

# Button to show Line Chart
if col1.button("Show Line Chart"):
    st.session_state.current_chart = 'line'

# Button to show Bar Chart
if col2.button("Show Bar Chart"):
    st.session_state.current_chart = 'bar'

# Button to show Pie Chart
if col3.button("Show Pie Chart"):
    st.session_state.current_chart = 'pie'

# Button to show Scatter Plot
if col4.button("Show Scatter Plot"):
    st.session_state.current_chart = 'scatter'

# Display the corresponding chart based on the current chart type
if st.session_state.current_chart == 'line':
    st.markdown("<div class='card1'><h3>Ultrasound Over Time</h3></div>", unsafe_allow_html=True)
    st.line_chart(us_data.set_index('timestamp')['US'],color='#77b5fe')

elif st.session_state.current_chart == 'bar':
    st.markdown("<div class='card1'><h3>Ultrasound Distribution</h3></div>", unsafe_allow_html=True)
    st.bar_chart(us_data.set_index('timestamp')['US'],color='#77b5fe')

elif st.session_state.current_chart == 'pie':
    st.markdown("<div class='card1'><h3>Ultrasound Proportions</h3></div>", unsafe_allow_html=True)
    us_bins = pd.cut(us_data['US'], bins=5)
    us_pie_data = us_bins.value_counts().reset_index()
    us_pie_data.columns = ['Ultrasound Range', 'Count']
    fig, ax = plt.subplots()
    ax.pie(us_pie_data['Count'], labels=us_pie_data['Ultrasound Range'], autopct='%1.1f%%')
    st.pyplot(fig)

elif st.session_state.current_chart == 'scatter':
    st.markdown("<div class='card1'><h3>Ultrasound Scatter Plot</h3></div>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    sns.scatterplot(x='timestamp', y='US', data=us_data, ax=ax)
    st.pyplot(fig)

st.markdown("<footer>Smart Agriculture Dashboard © 2024</footer>", unsafe_allow_html=True)
