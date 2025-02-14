from nyhousegeopanda import DisplayAPI
import panel as pn
import pandas as pd
from heatmap import HeatmapAPI

pn.extension()
# Call API functions and load in data from previous classes
api = DisplayAPI()
heatapi = HeatmapAPI()

api.load_dataset("NY-House-Dataset.csv")
heatapi.load_dataset("NY-House-Dataset.csv")

min_price, max_price = api.min_max()
beds, baths = api.beds_bath()

# Beds is a dataframe we only need 1 values to initialize so this is what that does
beds = pd.to_numeric(beds).dropna().unique()
baths = pd.to_numeric(baths).dropna().unique()
bed_default = int(beds[0])
bath_default = float(baths[0]) 

# Adding text inputs to add interactiveness to plots
min_price_input = pn.widgets.TextInput(name='Min Price ($)', value=str(min_price))
max_price_input = pn.widgets.TextInput(name='Max Price ($)', value=str(max_price))

bed_input = pn.widgets.TextInput(name='Number of beds', value=str(bed_default))
bath_input = pn.widgets.TextInput(name='Number of baths', value=str(bath_default))



def update_plot(min_price, max_price, bed_default, bath_default):
    '''
    Updates the plot based on the input of a user on the frontend
    min_price - tells you the lowest price value
    max_price - tells you highest price value
    bed_default - initialized bed variable
    bath_default - initialized bath variable
    '''

    min_price = int(min_price)
    max_price = int(max_price)
    bed_default = int(bed_default)
    bath_default = float(bath_default)

    # Filter the data
    filtered_data = api.filter_data(min_price, max_price, bed_default, bath_default)
    
    # Generate the interactive plot using hvplot
    plot = api.plot_map(filtered_data)
    
    return plot

def get_catalog_price_bed_bath(min_price, max_price, beds, baths):
    '''
    Make a table that is interactive based on the price the user inputs on the frontend
    paramers work the same as update_plot
    '''
    min_price = int(min_price)
    max_price = int(max_price)
    beds = int(beds)
    baths = float(baths)

    # Filter the dataset using price, beds, and baths
    local = api.filter_data(min_price, max_price, beds, baths)
    
    # Create the table widget
    table = pn.widgets.Tabulator(local, selectable=False)
    return table

def update_heatmap(price_range):
    '''
    Creates a slider on the frontend which can be used by the user to filter by a range on the heatmap
    '''
    min_price, max_price = price_range
    filtered_data = api.filter_data(min_price, max_price)

    heatmap = heatapi.generate_heatmap(min_price, max_price)
    return pn.pane.HTML(heatmap._repr_html_(), width=800, height=600)

# Make the plot and table interactive, binding the widgets to values
plot = pn.bind(update_plot, min_price_input, max_price_input, bed_input, bath_input)
catalog_price_bed_bath = pn.bind(get_catalog_price_bed_bath, min_price_input, max_price_input, bed_input, bath_input)

# Creates the slider widget on the frontend
price_range = pn.widgets.RangeSlider(
    name='Price Range', 
    start=min_price, 
    end=max_price, 
    step=5000,
    value=(min_price, max_price)
)
# Binds the slider to a heatmap that will be updated
heatmap_pane = pn.bind(update_heatmap, price_range)

# Creates the input text box in the frontend
plot_card = pn.Card(
    pn.Column(
        min_price_input,
        max_price_input,
        bed_input,
        bath_input
    ),
    title="Price Distribution Plot", width=350, collapsed=False
)


# Create a container for the plot
plot_container = pn.Column(
    plot,
)

# Create container for heatmap plot
heat_container = pn.Column(
    price_range,
    heatmap_pane
)

# Make table header
catalog_card = pn.Card(
    catalog_price_bed_bath, 
    title="House Listings by Price, Bed & Bath", width=1200, collapsed=False
)


# Create the final layout with adjustments
layout = pn.template.FastListTemplate(
    title='NYC Housing Plot',
    sidebar=[
        plot_card,
        pn.Column(catalog_card)
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Price plot", plot_container),
            ("Heatmap", heat_container),
            active=1
        )
        
    ]
).servable()

layout.show()



