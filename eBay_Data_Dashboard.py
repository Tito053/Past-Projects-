import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(layout= 'wide')

st.title('Ebay Computer Sales Infomation')
st.subheader('Created By: Alberto M. Colon')
st.divider()
st.write("Data overview")

df = pd.read_csv("EbayCleanedDataSample.csv")

st.subheader("Non-aggregated and unfiltered data")

st.dataframe(df, use_container_width=True)

st.divider()

#multi select data,

st.subheader('Please select the Brand(s) you are looking for!')
st.markdown('''This widget serves as a tool to present high-level information to my manager in an organized and accessible manner. 
            It enables the manager to filter data by brand and view all details about the computers available for each selected brand. 
            The primary purpose of this widget is to provide quick and concise insights, especially when extensive filtering is not necessary. 
            Furthermore, it is designed to display comprehensive information about a single brand at a time, rather than allowing filtering across multiple categories. 
            This streamlined approach ensures efficiency and simplicity for high-level decision-making.''')
Brand_options = df['Brand'].unique()

Brand_selection = st.multiselect(
    'Please select brand(s) you would like to view:',
    options=Brand_options,
    default=Brand_options[:2]  # Set first two brands as defaults
)

# Filter the DataFrame based on selection
filtered_df_multi = df[df['Brand'].isin(Brand_selection)]

# Display the filtered DataFrame
st.dataframe(filtered_df_multi)

st.divider()

###
st.subheader('Here is a price range, please adjust as you may see fit, to find the computer that best matchs what you need and that is within your budget!')
st.markdown('''This widget is designed to help you filter through the eBay dataset based on price, enabling you to exclude any computers that fall outside your specified budget.
             By doing so, it allows you to easily identify computers that match your desired price point while providing detailed information about each item that meets your criteria. 
            Additionally, the accompanying graph visually represents the filtered results by displaying the index and position ID of each computer, alongside its price. 
            This makes it simple to assess the price distribution and locate items that align with your budget and preferences.''')
# Add slider for price range selection
min_price = int(df['Price'].min())
max_price = int(df['Price'].max())
price_range = st.slider(
    "Select Price Range:",
    min_price,
    max_price,
    (min_price, max_price)  # Default range
)


# Filter dataset based on slider
filtered_data = df[(df['Price'] >= price_range[0]) & (df['Price'] <= price_range[1])]

# Display filtered data
st.write("Filtered Dataset", filtered_data)

# Add a simple visualization
st.bar_chart(filtered_data['Price'])

st.divider()

st.subheader('Please select the type of computer that you are looking for!')
st.markdown(''' The purpose of this widget is to provide a quick and efficient way to filter for the specific type of computer you are searching for,
            offering immediate access to the desired features or functionalities. As you apply filters, the underlying dataset dynamically adjusts to display only the types of computers that match your criteria. 
            In addition, the accompanying graph below visualizes the available colors within each category, updating in real-time to reflect your selections.
            This interactive functionality ensures a seamless and intuitive experience while exploring the data and narrowing down your choices.''')

# Add radio buttons for filtering by condition
type_options = df['Type'].unique()
selected_type = st.radio(
    "Select the Laptop type:",
    options=type_options
)


# Filter the dataset based on the selected condition
filtered_data = df[df['Type'] == selected_type]

# Display filtered data
st.write(f"Filtered Data for type: {selected_type}", filtered_data)

# Add a bar chart to visualize prices for the selected condition
st.bar_chart(filtered_data['Color'])


# Strip whitespace from column names
df.columns = df.columns.str.strip()

st.divider()
st.subheader('Select as many brands, Processor, computer type you are looking for.')
st.markdown('''This widget provides a powerful and flexible tool for filtering data across multiple categories simultaneously. It allows you to refine your search based on specific criteria, such as brands, 
            processors, and computer types, ensuring that you can easily narrow down the dataset to find the most relevant information. The Sunburst chart enhances this experience by visually representing the hierarchical relationships between these categories. 
            Each segment of the chart corresponds to a specific subset of the data, starting from broader categories like brands at the center and progressing to more detailed levels such as processors and computer types as you move outward.
            Using the Sunburst chart is straightforward. The innermost circle represents the highest-level category, such as brands, and the subsequent outer layers display increasingly specific details, like processor types and computer types.
            By clicking on a segment of the chart, you can drill down into that specific subset, dynamically updating the chart to show only the data for the selected segment. For example, clicking on a particular brand will reveal the associated processors and computer types for that brand alone. 
            The size of each segment reflects its proportionate value, such as total price or quantity, offering a clear representation of the distribution within the dataset. The chart is fully interactive and updates in real time, reflecting any filters applied through the widget or interactions with the chart itself.
            This seamless integration between filtering and visualization ensures an intuitive and efficient way to explore complex data relationships and gain deeper insights.''' 
            )

##sunburt chart with mutliselect 

# Multiselect for filtering by Brand
selected_brands = st.multiselect(
    "Filter by Brand:",
    options=df['Brand'].unique(),
    default=df['Brand'].unique()  # Default selects all brands
)

# Multiselect for filtering by Processor Type
selected_processors = st.multiselect(
    "Filter by Processor Type:",
    options=df['Processor'].unique(),
    default=df['Processor'].unique()  # Default selects all processors
)

# Multiselect for filtering by color Type
selected_type = st.multiselect(
    "Filter by Processor Type:",
    options=df['Type'].unique(),
    default=df['Type'].unique()  # Default selects all processors
)

# Apply filters
filtered_df = df[
    df['Brand'].isin(selected_brands) &
    df['Processor'].isin(selected_processors)&
    df['Type'].isin(selected_type)
]

# Display filtered dataset
st.write("Filtered Dataset", filtered_df)

# Create the Sunburst Chart
fig = px.sunburst(
    filtered_df,
    path=['Brand','OS', 'Processor', 'Type'],  # Ensure these columns exist
    values='Price',
    title="Price Breakdown by Brand, Condition, and Processor Type (Filtered)",
    labels={"Price": "Total Price (USD)"},
    width=875,  #(og is 700)
    height=875  #(og is 700)
)

# Display the Sunburst Chart
st.plotly_chart(fig)