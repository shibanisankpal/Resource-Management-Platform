import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# Helper function to load or create the resource data
def load_resource_data():
    try:
        resource_data = pd.read_csv('resource_data.csv')
    except FileNotFoundError:
        resource_data = pd.DataFrame(columns=['Resource Name', 'Availability', 'Utilization'])
    return resource_data

# Helper function to save the resource data
def save_resource_data(resource_data):
    resource_data.to_csv('resource_data.csv', index=False)

# Load the resource data
resource_data = load_resource_data()

# Streamlit app layout
st.title("Resource Management Platform")

# Sidebar to add new resource
st.sidebar.header("Add New Resource")
resource_name = st.sidebar.text_input("Resource Name")
availability = st.sidebar.number_input("Availability", min_value=0, step=1)
utilization = st.sidebar.number_input("Utilization", min_value=0, step=1)

# Button to add the new resource
if st.sidebar.button("Add Resource"):
    resource_data = resource_data.append({
        'Resource Name': resource_name,
        'Availability': availability,
        'Utilization': utilization
    }, ignore_index=True)
    save_resource_data(resource_data)
    st.sidebar.success("Resource added successfully!")

# Remove resource
st.sidebar.header("Remove Resource")
selected_resource = st.sidebar.selectbox("Select Resource to Remove", resource_data['Resource Name'])
if st.sidebar.button("Remove Resource"):
    resource_data = resource_data[resource_data['Resource Name'] != selected_resource]
    save_resource_data(resource_data)
    st.sidebar.success("Resource removed successfully!")

# Display the current resource data
st.header("Current Resource Data")
st.dataframe(resource_data)

# Capacity planning
st.header("Capacity Planning")
total_capacity = resource_data['Availability'].sum()
total_utilization = resource_data['Utilization'].sum()
remaining_capacity = total_capacity - total_utilization

st.write(f"Total Resource Capacity: {total_capacity}")
st.write(f"Total Resource Utilization: {total_utilization}")
st.write(f"Remaining Resource Capacity: {remaining_capacity}")


from io import BytesIO
import base64

# Data export functionality
if st.button("Export Resource Data"):
    st.write("Preparing the CSV file...")
    # Save the resource data to a BytesIO buffer
    buffer = BytesIO()
    resource_data.to_csv(buffer, index=False)
    buffer.seek(0)

    # Generate a download link for the CSV file
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="resource_data.csv">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.success("Download link is ready!")
