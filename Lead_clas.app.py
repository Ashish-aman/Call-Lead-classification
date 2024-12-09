import streamlit as st
import pandas as pd

# Load CSV data
df = pd.read_csv('results_poc_modified_prompt.csv')

# Show the first few rows of the dataset
st.write("Call Data Overview", df.head())



# Calculate KPIs
total_calls = len(df)
hot_calls = len(df[df['status'] == 'Hot'])
warm_calls = len(df[df['status'] == 'Warm'])
cold_calls = len(df[df['status'] == 'Cold'])

# Display KPIs in the app
st.title("Lead Classification Dashboard")

st.metric(label="Total Calls", value=total_calls)
st.metric(label="HOT Calls", value=hot_calls)
st.metric(label="Warm Calls", value=warm_calls)
st.metric(label="Cold Calls", value=cold_calls)



import plotly.express as px

# Pie chart for status breakdown
status_count = df['status'].value_counts().reset_index()
status_count.columns = ['Status', 'Count']

fig = px.pie(status_count, names='Status', values='Count', title="Call Status Breakdown")
st.plotly_chart(fig)


# Bar chart for reasons
reason_count = df.groupby('reason').size().reset_index(name='Count')
fig = px.bar(reason_count, x='reason', y='Count', title="Top Reasons for Call Classification")
st.plotly_chart(fig)


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import pgeocode

# Function to get latitude and longitude from pincode
def geocode_pincode(pincode, nomi):
    location = nomi.query_postal_code(pincode)
    return location.latitude, location.longitude

# Title
st.title("India Pincode Status Map")

# # File upload
# uploaded_file = st.file_uploader("Upload Pincode Data CSV", type=["csv"])

# if uploaded_file is not None:
# Load data
data = pd.read_csv('results_poc_modified_prompt.csv')


nomi = pgeocode.Nominatim('IN')  # For India

# Map Initialization
m = folium.Map(location=[22.5937, 78.9629], zoom_start=5)

# Define status colors
status_colors = {"hot": "red", "warm": "orange", "cold": "blue"}

# Plot points based on pincode and status
for _, row in data.iterrows():
  # Geocode pincode
  latitude, longitude = geocode_pincode(row['pincode'], nomi)
  
  # Check if latitude and longitude are valid
  if latitude and longitude:
      folium.CircleMarker(
          location=[latitude, longitude],
          radius=5,
          color=status_colors.get(row['status'].lower(), "gray"),
          fill=True,
          fill_color=status_colors.get(row['status'].lower(), "gray"),
          fill_opacity=0.7,
          popup=f"Pincode: {row['pincode']}<br>Status: {row['status']}",
      ).add_to(m)

# Display map in Streamlit
st_data = st_folium(m, width=700, height=500)

# else:
#     st.info("Please upload a CSV file to visualize the map.")



# Stacked bar chart for model vs status
model_status_count = pd.crosstab(df['model'], df['status']).reset_index()
fig = px.bar(model_status_count, x='model', y=model_status_count.columns[1:], 
             title="Car Model vs Call Status", barmode='stack')
st.plotly_chart(fig)



# Status filter
status_filter = st.selectbox("Select Call Status", df['status'].unique())
filtered_df = df[df['status'] == status_filter]

# Display filtered dataframe
st.write(f"Filtered Calls - Status: {status_filter}", filtered_df)

# Filter by model
model_filter = st.selectbox("Select Vehicle Model", df['model'].unique())
filtered_df_by_model = filtered_df[filtered_df['model'] == model_filter]

st.write(f"Filtered Calls - Model: {model_filter}", filtered_df_by_model)



# Lookup by file name
call_id = st.selectbox("Select Call", df['file_name'].unique())
call_details = df[df['file_name'] == call_id]
st.write(f"Call Details - {call_id}", call_details)



# Expander to show call details
with st.expander(f"Click to view details for {call_id}"):
    st.write(call_details)



# Assigning colors for different statuses
status_colors = {'Hot': 'red', 'Warm': 'yellow', 'Cold': 'blue'}

# Apply color to the charts
fig.update_traces(marker=dict(color=df['status'].map(status_colors)))
st.plotly_chart(fig)
