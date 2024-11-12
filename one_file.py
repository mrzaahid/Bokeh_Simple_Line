import pandas as pd
import re

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.plotting import figure, show

# Path to the input text file
input_file_path = 'soal_chart_bokeh.txt'
# Path to the output CSV file
output_file_path = 'output_file.csv'

# Initialize lists to store parsed data
data = []

# Read the text file
with open(input_file_path, 'r') as file:
    content = file.read()
    
    # Split the content into sections based on the separator
    sections = content.split('========================================')

    # Iterate over each section to extract data
    for section in sections:
        # Find the timestamp
        timestamp_match = re.search(r'Timestamp: (.+)', section)
        if timestamp_match:
            timestamp = timestamp_match.group(1).strip()
            
            # Find sender and receiver transfer rates
            sender_match = re.search(r'\[.*?\]\s+\S+\s+\S+\s+(\d+\.?\d*)\s+(KBytes|MBytes|Bytes)\s+(\d+\.?\d*)\s+(Kbits/sec|Mbits/sec|bits/sec)\s+.*?sender', section)
            receiver_match = re.search(r'\[.*?\]\s+\S+\s+\S+\s+(\d+\.?\d*)\s+(KBytes|MBytes|Bytes)\s+(\d+\.?\d*)\s+(Kbits/sec|Mbits/sec|bits/sec)\s+.*?receiver', section)

            # Define The Default Value
            sender_rate = None
            receiver_rate = None
            
            # Standardize The Unit
            if sender_match:
                sender_rate = float(sender_match.group(3))
                unit = sender_match.group(4)
                if unit == 'Kbits/sec':
                    sender_rate /= 1000  # Convert MBytes to KBytes

            # Standardize The Unit
            if receiver_match:
                receiver_rate = float(receiver_match.group(3))
                unit = receiver_match.group(4)
                if unit == 'Kbits/sec':
                    receiver_rate /= 1000  # Convert MBytes to KBytes
            
            # Append the data to the list
            data.append([timestamp, sender_rate, receiver_rate])

# Create a DataFrame from the parsed data
df = pd.DataFrame(data, columns=['Timestamp', 'Sender_Speed(Mbps)', 'Receiver_Speed(Mbps)'])

# Make the Timestamp data into a Datetime data
dates = pd.to_datetime(df['Timestamp'])

# Get The Main Data
source = ColumnDataSource(data=dict(date=dates, close=df['Sender_Speed(Mbps)']))

# Create a figure and axis
p = figure(title='Testing Jaringan',height=300, width=800,
           x_axis_type="datetime", x_axis_location="below",
           background_fill_color="#efefef", x_range=(dates[0], dates[195]))

# Create The Line and Label
p.line('date', 'close', source=source)
p.yaxis.axis_label = 'Speed (Mbps)'
p.xaxis.axis_label = 'Date Time'

# Create a Select Tool
select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=130, width=800, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")
range_tool = RangeTool(x_range=p.x_range, start_gesture="pan")
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2
select.line('date', 'close', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)

# Show The Line Chart And The Select Tool
show(column(p, select))


