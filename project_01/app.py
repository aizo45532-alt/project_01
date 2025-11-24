import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------
# TITLE & DESCRIPTION
# -------------------------------------------
st.set_page_config(page_title="COVID-19 Global Trends Dashboard", layout="wide")

st.title("🌍 COVID-19 Global Trends Dashboard")
st.write(
    """
    This interactive dashboard visualizes global COVID-19 trends including  
    **total cases**, **total deaths**, and **total vaccinations** for selected countries.

    Data Source: *Our World in Data (OWID)* – updated automatically via live URL.
    """
)

# -------------------------------------------
# LOAD & CACHE DATA
# -------------------------------------------
@st.cache_data
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# -------------------------------------------
# CLEANING
# -------------------------------------------
df = df.dropna(subset=["continent"])
df["date"] = pd.to_datetime(df["date"])

# -------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------
st.sidebar.header("🔧 Filters")

countries = df["location"].unique()
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=countries,
    default=["India", "United States", "Brazil"]
)

metric = st.sidebar.selectbox(
    "Select Metric:",
    ["total_cases", "total_deaths", "total_vaccinations"]
)

st.sidebar.info("You can choose multiple countries and any COVID-19 metric.")

# -------------------------------------------
# FILTER DATA
# -------------------------------------------
filtered_df = df[df["location"].isin(selected_countries)]

# -------------------------------------------
# CHART
# -------------------------------------------
st.subheader(f"📈 Trend of {metric.replace('_', ' ').title()}")

plt.figure(figsize=(12, 5))

for country in selected_countries:
    country_data = filtered_df[filtered_df["location"] == country]
    plt.plot(country_data["date"], country_data[metric], label=country)

plt.xlabel("Date")
plt.ylabel(metric.replace("_", " ").title())
plt.legend()
plt.tight_layout()
st.pyplot(plt)

# -------------------------------------------
# SUMMARY TABLE
# -------------------------------------------
st.subheader("📊 Latest Data Summary")

latest = (
    filtered_df.sort_values("date")
    .groupby("location")
    [["total_cases", "total_deaths", "total_vaccinations"]]
    .last()
)

st.dataframe(latest.style.format("{:,.0f}"))

st.success("Dashboard Loaded Successfully ✔️")
