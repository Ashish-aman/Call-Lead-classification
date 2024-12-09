# import streamlit as st
# import pandas as pd

# # Load CSV data
# df = pd.read_csv('results_poc_modified_prompt.csv')

# # Show the first few rows of the dataset
# # st.write("Call Data Overview", df.head())


# # Calculate KPIs
# total_calls = len(df)
# hot_calls = len(df[df['status'] == 'Hot'])
# warm_calls = len(df[df['status'] == 'Warm'])
# cold_calls = len(df[df['status'] == 'Cold'])

# # Display KPIs in the app
# st.title("Lead Classification Dashboard")

# st.metric(label="Total Calls", value=total_calls)
# st.metric(label="HOT Calls", value=hot_calls)
# st.metric(label="Warm Calls", value=warm_calls)
# st.metric(label="Cold Calls", value=cold_calls)



# import plotly.express as px

# # Pie chart for status breakdown
# status_count = df['status'].value_counts().reset_index()
# status_count.columns = ['Status', 'Count']

# fig = px.pie(status_count, names='Status', values='Count', title="Call Status Breakdown")
# st.plotly_chart(fig)



# # Bar chart for reasons
# reason_count = df.groupby('reason').size().reset_index(name='Count')
# fig = px.bar(reason_count, x='reason', y='Count', title="Top Reasons for Call Classification")
# st.plotly_chart(fig)



# # Map of HOT calls by Pincode
# hot_leads_by_pincode = df[df['status'] == 'Hot']['pincode'].value_counts().reset_index()
# hot_leads_by_pincode.columns = ['pincode', 'Count']

# fig = px.choropleth(hot_leads_by_pincode, locations='pincode', color='Count', 
#                     color_continuous_scale='Viridis', title="HOT Calls by Pincode")
# st.plotly_chart(fig)



# # Stacked bar chart for model vs status
# model_status_count = pd.crosstab(df['model'], df['status']).reset_index()
# fig = px.bar(model_status_count, x='model', y=model_status_count.columns[1:], 
#              title="Car Model vs Call Status", barmode='stack')
# st.plotly_chart(fig)



# # Status filter
# status_filter = st.selectbox("Select Call Status", df['status'].unique())
# filtered_df = df[df['status'] == status_filter]

# # Display filtered dataframe
# st.write(f"Filtered Calls - Status: {status_filter}", filtered_df)

# # Filter by model
# model_filter = st.selectbox("Select Vehicle Model", df['model'].unique())
# filtered_df_by_model = filtered_df[filtered_df['model'] == model_filter]

# st.write(f"Filtered Calls - Model: {model_filter}", filtered_df_by_model)



# # Lookup by file name
# call_id = st.selectbox("Select Call", df['file_name'].unique())
# call_details = df[df['file_name'] == call_id]
# st.write(f"Call Details - {call_id}", call_details)



# # Expander to show call details
# with st.expander(f"Click to view details for {call_id}"):
#     st.write(call_details)



# # # Assigning colors for different statuses
# # status_colors = {'Hot': 'red', 'Warm': 'yellow', 'Cold': 'blue'}

# # # Apply color to the charts
# # fig.update_traces(marker=dict(color=df['status'].map(status_colors)))
# # st.plotly_chart(fig)






import streamlit as st
import pandas as pd
import plotly.express as px

# Custom CSS for background color and other styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5dc;  /* Light brown-cream color */
        font-family: Arial, sans-serif;
    }
    .css-1v3fvcr {
        background-color: #f5f5dc;  /* Adjust for content background */
    }
    .stSelectbox label {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load CSV data
df = pd.read_csv('results_poc_modified_prompt.csv')

# Title and Description
st.title("Lead Classification Dashboard")
st.markdown("**Analyze call data and understand lead classifications.**")

# KPIs - Arrange in Two Columns
kpi_col1, kpi_col2 = st.columns(2)
with kpi_col1:
    st.metric(label="Total Calls", value=len(df))
    st.metric(label="HOT Calls", value=len(df[df['status'] == 'Hot']))
with kpi_col2:
    st.metric(label="Warm Calls", value=len(df[df['status'] == 'Warm']))
    st.metric(label="Cold Calls", value=len(df[df['status'] == 'Cold']))

# Pie chart for status breakdown
st.markdown("### Call Status Breakdown")
status_count = df['status'].value_counts().reset_index()
status_count.columns = ['Status', 'Count']
fig = px.pie(status_count, names='Status', values='Count', title="Call Status Breakdown")
st.plotly_chart(fig)

# Bar chart for reasons
st.markdown("### Top Reasons for Call Classification")
reason_count = df.groupby('reason').size().reset_index(name='Count')
fig = px.bar(reason_count, x='reason', y='Count', title="Top Reasons for Call Classification")
st.plotly_chart(fig)

# Map of HOT calls by Pincode
st.markdown("### HOT Calls by Pincode")
hot_leads_by_pincode = df[df['status'] == 'Hot']['pincode'].value_counts().reset_index()
hot_leads_by_pincode.columns = ['pincode', 'Count']
fig = px.choropleth(
    hot_leads_by_pincode,
    locations='pincode',
    color='Count',
    color_continuous_scale='Viridis',
    title="HOT Calls by Pincode",
)
st.plotly_chart(fig)

# Stacked bar chart for model vs status
st.markdown("### Car Model vs Call Status")
model_status_count = pd.crosstab(df['model'], df['status']).reset_index()
fig = px.bar(
    model_status_count,
    x='model',
    y=model_status_count.columns[1:],
    title="Car Model vs Call Status",
    barmode='stack',
)
st.plotly_chart(fig)

# Filters Section - Arrange in Two Columns
st.markdown("### Filters")
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    status_filter = st.selectbox("Select Call Status", df['status'].unique())
with filter_col2:
    model_filter = st.selectbox("Select Vehicle Model", df['model'].unique())

# Apply Filters
filtered_df = df[df['status'] == status_filter]
st.write(f"Filtered Calls - Status: {status_filter}", filtered_df)

filtered_df_by_model = filtered_df[filtered_df['model'] == model_filter]
st.write(f"Filtered Calls - Model: {model_filter}", filtered_df_by_model)

# Lookup by file name
st.markdown("### Call Lookup")
call_id = st.selectbox("Select Call", df['file_name'].unique())
call_details = df[df['file_name'] == call_id]

with st.expander(f"Click to view details for {call_id}"):
    st.write(call_details)

