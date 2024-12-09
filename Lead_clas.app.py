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

import streamlit as st
import folium
from streamlit_folium import st_folium
import pgeocode

# Function to get latitude and longitude from pincode
def geocode_pincode(pincode, nomi):
    location = nomi.query_postal_code(pincode)
    if location is not None:
        return location.latitude, location.longitude
    return None, None

import streamlit as st
import pandas as pd
import folium
from pgeocode import GeoDistance
from streamlit.components.v1 import iframe

# Initialize GeoDistance for India
nomi = GeoDistance('IN')

# Function to clean and validate pincode
def clean_pincode(pincode):
    if pincode:
        pincode = pincode.replace(',', '')  # Remove commas
        if len(pincode) == 6 and pincode.isdigit():
            return pincode
    return None

# Function to get latitude and longitude from pincode
def get_lat_lon(pincode):
    location = nomi.query_postal_code(pincode)
    if location.empty:
        return None
    return location.iloc[0]['latitude'], location.iloc[0]['longitude']

# Function to assign color based on status
def status_color(status):
    if status == 'hot':
        return 'red'
    elif status == 'warm':
        return 'yellow'
    elif status == 'cold':
        return 'blue'
    return 'gray'

# # Sample DataFrame (replace with your actual dataframe)
# df_clean = pd.DataFrame({
#     'pincode': ['110001', '1234,56', '400001', None, '500001'],
#     'status': ['hot', 'warm', 'cold', 'warm', 'hot']
# })
df_clean = df
# Clean and process the pincode data
df_clean['pincode'] = df_clean['pincode'].apply(clean_pincode)
df_clean = df_clean.dropna(subset=['pincode'])  # Drop rows with missing or invalid pincodes

# Create a base map centered around India
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Add markers for each valid pincode on the map
for _, row in df_clean.iterrows():
    pincode = row['pincode']
    status = row['status']
    lat_lon = get_lat_lon(pincode)
    
    if lat_lon:
        lat, lon = lat_lon
        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            color=status_color(status),
            fill=True,
            fill_color=status_color(status),
            fill_opacity=0.7,
            popup=f"Pincode: {pincode}\nStatus: {status}"
        ).add_to(m)

# Save the map to an HTML file
map_file = "india_pincode_map.html"
m.save(map_file)

# Display the map in Streamlit
st.title('Pincode Status Visualization on India Map')

# Display the map using Streamlit iframe component
iframe_html = f'<iframe src="{map_file}" width="100%" height="600"></iframe>'
st.markdown(iframe_html, unsafe_allow_html=True)




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
