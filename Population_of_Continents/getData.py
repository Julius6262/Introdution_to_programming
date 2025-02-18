import pandas as pd
import os

url = 'https://en.wikipedia.org/wiki/List_of_continents_and_continental_subregions_by_population'

html_tables = pd.read_html(url, header=0)

list_table_names= ["Eastern Africa","Middle Africa","Northern Africa","Southern Africa","Western Africa","Total Africa",
                   "Total Americas","Caribbean","Central America","Northern America","Total North America","Total South America",
                   "Central Asia","Eastern Asia","South-eastern Asia","Southern Asia","Western Asia","Total Asia",
                   "Eastern Europe","Northern Europe","Southern Europe","Western Europe","Total Europe",
                   "Total Oceania","Total World"]


directory = "data/"

if not os.path.exists(directory):
    os.makedirs(directory)

for i in range(0,25):
    html_tables[i+3].to_csv(f"data/{list_table_names[i]}.csv", index=False)