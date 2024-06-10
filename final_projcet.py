import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter,HoverTool
from math import pi
from bokeh.transform import cumsum
from bokeh.palettes import Category20c, viridis,Category20

# Load data
file_path = 'finalproject_Pizza.csv'
pizza_sales_data = pd.read_csv(file_path)

# Data preprocessing
pizza_sales_data['date'] = pd.to_datetime(pizza_sales_data['date'])
pizza_sales_data['day'] = pizza_sales_data['date'].dt.date
pizza_sales_data['month'] = pizza_sales_data['date'].dt.to_period('M')

# Aggregate sales by day
daily_sales = pizza_sales_data.groupby('day').agg({'price': 'sum'}).reset_index()

st.markdown(
        """
        <div style='background-color: #009688; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <h1 style='color: white; text-align: center;'>Pizza Sales Dashboard</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Streamlit app
def final_project():

    # Add sidebar navigation
    page = st.sidebar.radio("Navigation", ["Introduction","Daily Sales", "Pizza Sales by Name", "Sales by Category", "Sales by Pizza Size"])
    if page == "Introduction":
        st.markdown("""
        # Introduction
        ## TUGAS VISUALISASI DATA - INTERACTIVE VISUATIZATION
        """)
        st.write("Kelompok :")
        st.markdown("""
                - Andhika Rangga Dwi Guntara - 1301213179
                - Hanif Aditia Sofian - 1301213550
                - Rayhan Adrian Fadhilah - 1301210331
                - Reva Rivandi Salim - 1301213314
                - Muhammad Jilan Hilmi - 1301184514
        """)
        st.write("Dataset yang digunakan adalah dataset penjualan pizza")
        st.write("Berikut ini adalah isi dari dataset")
        
        st.write(pizza_sales_data.head(5))

    elif page == "Daily Sales":
        st.write("Pilih tanggal :")
        # Filter by date range
        start_date = st.date_input("Start date", min_value=pd.to_datetime(pizza_sales_data['date']).min(), max_value=pd.to_datetime(pizza_sales_data['date']).max())
        end_date = st.date_input("End date", min_value=pd.to_datetime(pizza_sales_data['date']).min(), max_value=pd.to_datetime(pizza_sales_data['date']).max())

        # Convert start_date and end_date to pandas datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter sales data
        filtered_sales = pizza_sales_data[(pizza_sales_data['date'] >= start_date) & (pizza_sales_data['date'] <= end_date)]

        # Daily Sales Line Chart
        st.header("Daily Sales")
        st.write("Berikut ini adalah line chart penjualan pizza:")
        # daily_sales_filtered = filtered_sales.groupby('date').agg({'price': 'sum'}).reset_index()
        # Group by date and calculate count
        daily_sales_filtered = filtered_sales.groupby('date').size().reset_index(name='count')



        source = ColumnDataSource(daily_sales_filtered)
        p = figure(x_axis_type='datetime', title="Daily Sales", height=400, width=700)
        p.line(x='date', y='count', source=source, line_width=2)

        tooltips = [("Date", "@date{%F}"), ("Count", "@count")]
        p.add_tools(HoverTool(tooltips=tooltips, formatters={"@date": "datetime"}))
        p.xaxis.formatter=DatetimeTickFormatter(months=["%b %Y"])

        # Display the chart
        st.bokeh_chart(p, use_container_width=True)

    elif page == "Pizza Sales by Name":
        st.header("Pizza Sales by Name")
        st.write("Berikut ini adalah pie chart penjualan untuk setiap menu pizza:")
        # Group data by 'name' to get the count of each pizza type
        pizza_sales_by_name = pizza_sales_data.groupby('name').size().reset_index(name='count')

        # Prepare data for pie chart
        pizza_sales_by_name['angle'] = pizza_sales_by_name['count'] / pizza_sales_by_name['count'].sum() * 2 * pi

        # Dynamically generate color palette
        num_items = len(pizza_sales_by_name)
        palette = viridis(num_items)

        pizza_sales_by_name['color'] = palette

        # Create pie chart
        p = figure(height=800,width=400, title="Pizza Sales by Name", toolbar_location=None,
                tools="hover", tooltips="@name: @count", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='name', source=pizza_sales_by_name)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None


        # Display the chart
        st.bokeh_chart(p, use_container_width=True)


    elif page == "Sales by Category":
        # Sales by Pizza Type
        st.header("Sales by Pizza Category")
        st.write("Berikut ini adalah Barplot untuk setiap category pizza:")
        sales_by_type = pizza_sales_data.groupby('type').agg({'price': 'sum'}).reset_index()
        p3 = figure(x_range=sales_by_type['type'], title="Sales by Pizza Category")
        p3.vbar(x=sales_by_type['type'], top=sales_by_type['price'], width=0.9)
        p3.xgrid.grid_line_color = None
        p3.y_range.start = 0
        

        # Display the chart
        st.bokeh_chart(p3, use_container_width=True)

    elif page == "Sales by Pizza Size":
        # Sales by Pizza Size
        st.header("Sales by Pizza Size")
        st.write("Berikut ini adalah barplot penjualan untuk setiap ukuran pizza:")
        sales_by_size = pizza_sales_data.groupby('size').agg({'price': 'sum'}).reset_index()
        p4 = figure(x_range=sales_by_size['size'], title="Sales by Pizza Size")
        p4.vbar(x=sales_by_size['size'], top=sales_by_size['price'], width=0.9)
        p4.xgrid.grid_line_color = None
        p4.y_range.start = 0

        # Display the chart
        st.bokeh_chart(p4, use_container_width=True)

        st.write("\nBerikut ini adalah pie chart penjualan untuk setiap ukuran pizza:")

        # Custom filter for each type of pizza
        selected_pizza = st.selectbox("Select Pizza Type", pizza_sales_data['name'].unique())

        # Filter sales data for the selected pizza type
        filtered_sales = pizza_sales_data[pizza_sales_data['name'] == selected_pizza]

        # Count the sales based on size
        sales_by_size = filtered_sales.groupby('size').size().reset_index(name='count')

        # Create a pie chart
        sales_by_size['angle'] = sales_by_size['count'] / sales_by_size['count'].sum() * 2 * pi
        num_sizes = len(sales_by_size)
        colors = Category20[num_sizes]
        sales_by_size['color'] = colors[:num_sizes]

        p = figure(plot_height=400, title=f"{selected_pizza} Sales by Size", toolbar_location=None,
                tools="hover", tooltips="@size: @count")

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='size', source=sales_by_size)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        # Display the chart
        st.bokeh_chart(p, use_container_width=True)


if __name__ == "__main__":
    final_project()
