# Africa Maps Visualization

Interactive maps showing financial inclusion data and project coverage across African countries. Built with Python, Folium, and Leaflet.js. Data source: World Bank Global Findex Database 2021.

## Features
- Interactive map of Africa
- Color-coded countries based on energy access levels
- Hover tooltips showing exact percentages
- Source link to World Bank data
- Clean, modern design with white background

## Data Source
Data is sourced from the World Bank's Energy Access indicator (EG.ELC.ACCS.ZS) for the year 2020.

## Technologies Used
- Python
- Folium
- GeoPandas
- Pandas
- World Bank API

## How to Run
1. Install required packages:
```bash
pip install folium geopandas pandas requests
```

2. Run the script:
```bash
python africa_map.py
```

3. Open the generated `africa_map.html` in your web browser to view the map. 