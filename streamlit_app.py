import streamlit as st
import pandas as pd
from pathlib import Path

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)


# Caching the data loading function
@st.cache_data
def get_complaint_data():
    """Load complaint data from a CSV file and return it as a DataFrame.
    
    This uses caching to avoid reading the file every time. If you were
    reading from an HTTP endpoint, you could set a TTL argument for the cache.
    """
    # Use the absolute path to the data file
    DATA_FILENAME = Path('/Users/huiluan/Desktop/ComplaintApp/Data/dashboard_test.csv')
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(DATA_FILENAME)

    # Convert '接件日期' to datetime (assuming it's in this format)
    df['接件日期'] = pd.to_datetime(df['接件日期'], errors='coerce')
    
    # Return the DataFrame
    return df

# Load the data into df_use
df_use = get_complaint_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :hospital: Hospital Complaint Dashboard

Browse complaint data from the hospital. You can filter by date range and department (ward).
'''

# Sidebar: Filter by date range (years)
st.sidebar.header('Filter by Date Range')
min_year = df_use['接件日期'].dt.year.min()
max_year = df_use['接件日期'].dt.year.max()

# Slider to select the year range
from_year, to_year = st.sidebar.slider(
    'Which years are you interested in?',
    min_value=int(min_year),
    max_value=int(max_year),
    value=[int(min_year), int(max_year)]
)

# Filter the data based on the selected year range
df_filtered = df_use[(df_use['接件日期'].dt.year >= from_year) & (df_use['接件日期'].dt.year <= to_year)]

# Sidebar: Filter by departments/wards (涉及科室/病区)
st.sidebar.header('Filter by Department/Ward')
departments = df_use['涉及科室/病区'].unique()

# Multiselect for departments/wards
selected_departments = st.sidebar.multiselect(
    'Which departments/wards would you like to view?',
    departments,
    default=departments  # Select all by default
)

# Filter data based on selected departments
if selected_departments:
    df_filtered = df_filtered[df_filtered['涉及科室/病区'].isin(selected_departments)]
else:
    st.warning("Please select at least one department/ward.")

# Main Content: Display filtered complaint information
st.header('Filtered Complaint Information')

# Display the filtered data in a table format
st.dataframe(df_filtered)

# Optionally, add more visualizations like charts, summaries, etc.
# Example: Count of complaints per department/ward
st.subheader('Complaint Count by Department/Ward')
complaint_count = df_filtered['涉及科室/病区'].value_counts()
st.bar_chart(complaint_count)

# Display the counts of complaints by year via line bar graph
st.subheader('Complaint Count by Year')
complaint_count_by_year = filtered_df['Year'].value_counts().sort_index()
st.line_chart(complaint_count_by_year)

''
''

# Display the counts of complaints by department/ward
st.subheader('Complaint Count by Department/Ward')
complaint_count_by_department = filtered_df['涉及科室/病区'].value_counts()
st.bar_chart(complaint_count_by_department)

''
''

# Display the counts of complaints for the first and last year
first_year_df = filtered_df[filtered_df['Year'] == from_year]
last_year_df = filtered_df[filtered_df['Year'] == to_year]

st.header(f'Complaint Count in {to_year}', divider='gray')

''

cols = st.columns(4)

for i, department in enumerate(selected_departments):
    col = cols[i % len(cols)]

    with col:
        first_count = first_year_df[first_year_df['涉及科室/病区'] == department]['Year'].count()
        last_count = last_year_df[last_year_df['涉及科室/病区'] == department]['Year'].count()

        if first_count == 0:
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_count / first_count:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{department} Complaint Count',
            value=f'{last_count}',
            delta=growth,
            delta_color=delta_color
        )
