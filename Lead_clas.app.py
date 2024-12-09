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



# Step 2: Drop rows where Pincode is null or empty
df_clean = df[df['pincode'].notna()]  # Removes rows where Pincode is NaN
# df_clean = df_clean[df_clean['pincode'].str.strip() != '']  # Removes rows where Pincode is an empty string

# Step 3: Clean the Pincode column
# Remove any commas and ensure the pincode is a 6-digit number
# df_clean['pincode'] = df_clean['pincode'].str.replace(',', '')  # Remove commas
# df_clean['pincode'] = df_clean['pincode'].apply(lambda x: str(x).zfill(6))  # Pad to 6 digits
df_clean['pincode'] = df_clean['pincode'].astype(int)

# Step 4: Check the results
# print(df_clean[['pincode']].head())
import pandas as pd
import folium
import streamlit as st

# Step 1: Load your datasets
# Replace these paths with the actual paths to your CSV files
df_models = df_clean   # Contains models status and pincodes
df_latitudes_longitudes = pd.read_csv('pincode_with_lat-long.csv')  # Contains pincode, lat, long
# Remove invalid rows
df_latitudes_longitudes['Latitude'] = pd.to_numeric(df_latitudes_longitudes['Latitude'], errors='coerce')
df_latitudes_longitudes['Longitude'] = pd.to_numeric(df_latitudes_longitudes['Longitude'], errors='coerce')
# Merge DataFrames by specifying column names
merged_df = pd.merge(df_models, df_latitudes_longitudes, left_on='pincode', right_on='Pincode', how='inner')

# Step 3: Drop rows where Latitude or Longitude is missing (if necessary)
merged_df = merged_df.dropna(subset=['Latitude', 'Longitude'])

# Step 4: Create a base map centered on India
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  # India center

# Step 5: Plot each pincode on the map
for _, row in merged_df.iterrows():
    lat, lon = row['Latitude'], row['Longitude']
    pincode = row['Pincode']
    model_status = row['status']  # Assuming 'Status' column contains model status (hot, warm, cold)
    
    # Set the color based on the status (can adjust the color as per your logic)
    if model_status == 'Hot':
        color = 'red'
    elif model_status == 'Warm':
        color = 'orange'
    else:
        color = 'green'

    # Add a CircleMarker for each pincode
    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"Pincode: {pincode}\nStatus: {model_status}",
    ).add_to(m)

# Step 6: Save the map and display it in Streamlit
map_file = "india_pincode_map.html"
m.save(map_file)

# Display the map in Streamlit
st.title('Pincode Locations with Model Status on India Map')

# Display map using iframe in Streamlit
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
