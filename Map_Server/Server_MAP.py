from flask import Flask
import folium
import pandas as pd
import geopandas as gpd
import rtree
import pygeos

app = Flask(__name__)

df = pd.read_csv('../AnalysisData.csv')

#  define the 2 coordinates and zip together
df["WellHeadCoordinates"] = list(zip(df.SurfaceLongitude, df.SurfaceLatitude))
from shapely.geometry import Point #get method to create points on shapefiles
# create points on shapefile
df["WellHeadCoordinates"] = df["WellHeadCoordinates"].apply(Point) # 
# create geopandas datafarame with weel coordinates as geolocation geometry
gdf = gpd.GeoDataFrame(df, geometry="WellHeadCoordinates")

gdf.crs = "EPSG:4269"
#create folium map with gdf
m = gdf.drop('CompletionDate', axis=1).explore()
#get fips for texas
fips_tx = 48
# load county bond. from latest CENSUS data
county_df = gpd.read_file("https://datascience.quantecon.org/assets/data/cb_2016_us_county_5m.zip")
# Load all TEXAS counties
county_df = county_df.query("STATEFP == '48'") #Texas State
# creating the counties outline gdf intersecting with the well data
from geopandas.tools import sjoin
county_df = sjoin(county_df, gdf, how='inner')
#add counties to folium map
county_df.explore(m=m)

folium.TileLayer('Stamen Toner', control=True).add_to(m)  # use folium to add alternative tiles
folium.LayerControl().add_to(m)  # use folium to add layer control



#@app.route('/')
#def index():
#	folium_map = m
#    return folium_map._repr_html_()


#if __name__ == '__main__':
#    app.run(port=5000,debug=True)
	

@app.route('/')
def index():
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
