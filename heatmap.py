import panel as pn
import folium
import geopandas as gpd
import pandas as pd
from folium.plugins import HeatMap


# Load dataset
class HeatmapAPI():
    def load_dataset(self, filename):
        
        self.df = pd.read_csv(filename)
        

    def min_max(self):
            return self.df['PRICE'].min(), self.df['PRICE'].max()
    # Function to generate heatmap
    def generate_heatmap(self, min_price, max_price):
        
        filtered_df = self.df[(self.df['PRICE'] >= min_price) & (self.df['PRICE'] <= max_price)]
        filtered_df["PRICE_PER_SQFT"] = filtered_df["PRICE"] / filtered_df["PROPERTYSQFT"]
        m = folium.Map(location=[40.7128, -74.0060], zoom_start=12, tiles="CartoDB Positron")

        heat_data = list(zip(filtered_df['LATITUDE'], filtered_df['LONGITUDE'], filtered_df['PRICE_PER_SQFT']))
        HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(m)

        return m
    
    def update_heatmap(price_range):
        min_price, max_price = price_range
        

def main():
    heatapi = HeatmapAPI()
    heatapi.load_dataset("NY-House-Dataset.csv")
    minimum, maximum = heatapi.min_max()
    plot = heatapi.generate_heatmap(minimum, maximum)

if __name__ == '__main__':
    main()


