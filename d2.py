

import pandas as pd
import streamlit as st
import requests

# Step 1: Download mutual fund NAV data from AMFI
AMFI_NAV_URL = "https://www.amfiindia.com/spages/NAVAll.txt"

def scrape_amfi_nav_data():
    # Download the NAV data
    response = requests.get( "https://www.amfiindia.com/spages/NAVAll.txt"
)
    data = response.text.splitlines()

    # Parse the text data into a structured format
    funds = []
    for line in data[1:]:  # Skip the first line (header)
        fields = line.split(";")
        if len(fields) >= 6:
            funds.append({
                "Fund Name": fields[0].strip(),
                "Category": fields[3].strip(),
                "NAV": fields[4].strip(),
                "Date": fields[5].strip(),
                "Returns": "N/A"  # AMFI doesn't provide returns in the file
            })
    return funds

# Step 2: Categorize the funds
def categorize_funds(funds):
    categories = {"Large Cap": [], "Mid Cap": [], "Small Cap": [], "Flexi Cap": []}
    for fund in funds:
        category = fund["Category"].lower()
        if "large" in category:
            categories["Large Cap"].append(fund)
        elif "mid" in category:
            categories["Mid Cap"].append(fund)
        elif "small" in category:
            categories["Small Cap"].append(fund)
        elif "flexi" in category:
            categories["Flexi Cap"].append(fund)
    return categories

# Step 3: Get and categorize the data
fund_data = scrape_amfi_nav_data()
categorized_data = categorize_funds(fund_data)

# Step 4: Build the Streamlit app
st.title("Mutual Fund Categories")

# Dropdown to select category
selected_category = st.selectbox("Select Fund Category:", ["Large Cap", "Mid Cap", "Small Cap", "Flexi Cap"])

# Display the funds under the selected category
st.subheader(f"Funds under {selected_category} category:")

if selected_category in categorized_data:
    df = pd.DataFrame(categorized_data[selected_category])
    if not df.empty:
        st.dataframe(df)
    else:
        st.write("No data available for this category.")
else:
    st.write("Invalid category selected.")

