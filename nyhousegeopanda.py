import pandas as pd
import matplotlib.pyplot as plt
import panel as pn
import geopandas
import geodatasets
from geopandas import GeoDataFrame
import hvplot.pandas


pn.extension()

class DisplayAPI:
    def load_dataset(self, filename):
        self.house = pd.read_csv(filename)

    def min_max(self):
        return self.house['PRICE'].min(), self.house['PRICE'].max()
    def beds_bath(self):
       

        return self.house['BEDS'], self.house['BATH']
    def plot_map(self, filtered_df):
        

        # Create GeoDataFrame
        geometry = geopandas.points_from_xy(filtered_df['LONGITUDE'], filtered_df['LATITUDE'])
        gdf = geopandas.GeoDataFrame(filtered_df, geometry=geometry, crs="EPSG:4326")

        geometry = geopandas.points_from_xy(filtered_df['LONGITUDE'], filtered_df['LATITUDE'])
        gdf = geopandas.GeoDataFrame(filtered_df, geometry=geometry, crs="EPSG:4326")

        # Create the plot (set up the figure and axis)
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Get the borough boundaries and plot
        path_nybb = geodatasets.get_path("nybb")
        boros = GeoDataFrame.from_file(path_nybb)
        boros = boros.to_crs("EPSG:4326")

        # Plot the boroughs and house locations
        boros_plot = boros.hvplot(
            color='lightgrey', 
            edgecolor='black', 
            xlabel='Longitude', 
            ylabel='Latitude', width=600, height=600)

        house_plot = gdf.hvplot.points(
            x='LONGITUDE', 
            y='LATITUDE', 
            color='red', 
            alpha=0.3,
            hover_cols=['PRICE', 'ADDRESS', 'BEDS', 'BATH'],  
            title='NYC House Locations (Filtered by Price, Beds, and Baths)',
            xlabel = 'Longitude',
            ylabel = 'Latitude',
            tools=['pan', 'wheel_zoom', 'box_zoom', 'reset']
        )

        # Combine the plots
        combined_plot = boros_plot * house_plot

        return combined_plot
   
    def ny_table(self, min_price, max_price):

        price = self.house.sort_values('PRICE', ascending=False)
        price = price[(price['PRICE']  >= min_price) & (price['PRICE'] <= max_price)]
       
        return price
    def filter_data(self, min_price, max_price, beds=None, baths=None):
    
  
        filtered_df = self.house[
            (self.house['PRICE'] >= min_price) & 
            (self.house['PRICE'] <= max_price)
        ]
        
        # Filter by number of beds if provided
        if beds is not None:
            filtered_df = filtered_df[filtered_df['BEDS'] == beds]
        
        # Filter by number of baths if provided
        if baths is not None:
            filtered_df = filtered_df[filtered_df['BATH'] == baths]
        
        # Drop rows with missing values
        filtered_df = filtered_df.dropna()
        
        return filtered_df
def main():
    # Initialize the API
    displayapi = DisplayAPI()
    displayapi.load_dataset("NY-House-Dataset.csv")

    # Get the min and max prices from the dataset
    min_, max_ = displayapi.min_max()

    bed, bath = displayapi.beds_bath()
    # Generate the map plot and return the figure
    
    displayapi.ny_table(min_, max_)
    # Display the figure
    df = displayapi.filter_data(min_, max_, bed, bath)
    displayapi.plot_map(df)

if __name__ == '__main__':
    main()
