import folium
import geopandas as gpd
import requests
import json

# Download GeoJSON data for African countries
url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
response = requests.get(url)
world_geojson = response.json()

# Financial inclusion data (account ownership %)
energy_access = {
    'Algeria': 99.8,
    'Angola': 45.6,
    'Benin': 40.3,
    'Botswana': 72.3,
    'Burkina Faso': 18.4,
    'Burundi': 11.1,
    'Cameroon': 63.3,
    'Cape Verde': 96.2,
    'Central African Republic': 14.3,
    'Chad': 8.4,
    'Comoros': 84.1,
    'Republic of Congo': 48.3,
    'Ivory Coast': 69.8,
    'Democratic Republic of the Congo': 19.1,
    'Djibouti': 61.8,
    'Egypt': 100.0,
    'Equatorial Guinea': 67.2,
    'Eritrea': 51.9,
    'Swaziland': 77.5,
    'Ethiopia': 51.1,
    'Gabon': 91.1,
    'Gambia': 62.3,
    'Ghana': 85.9,
    'Guinea': 44.7,
    'Guinea Bissau': 28.7,
    'Kenya': 71.4,
    'Lesotho': 44.6,
    'Liberia': 27.5,
    'Libya': 67.3,
    'Madagascar': 26.9,
    'Malawi': 15.0,
    'Mali': 48.4,
    'Mauritania': 47.2,
    'Mauritius': 100.0,
    'Morocco': 100.0,
    'Mozambique': 30.6,
    'Namibia': 53.9,
    'Niger': 19.2,
    'Nigeria': 55.4,
    'Rwanda': 46.6,
    'Sao Tome and Principe': 74.1,
    'Senegal': 70.4,
    'Seychelles': 100.0,
    'Sierra Leone': 26.1,
    'Somalia': 35.3,
    'South Africa': 85.0,
    'South Sudan': 6.7,
    'Sudan': 53.8,
    'United Republic of Tanzania': 39.9,
    'Togo': 52.4,
    'Tunisia': 100.0,
    'Uganda': 41.3,
    'Western Sahara': 95.0,
    'Zambia': 44.5,
    'Zimbabwe': 41.0
}

# Debug print to find Guinea-Bissau in the data
print("Looking for Guinea-Bissau in the data:")
for feature in world_geojson["features"]:
    if "Guinea" in feature["properties"]["ADMIN"]:
        print(f"Found country as: {feature['properties']['ADMIN']}")

# Filter for African countries
african_countries = [
    'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cameroon', 
    'Cape Verde', 'Central African Republic', 'Chad', 'Comoros', 'Republic of Congo', 'Ivory Coast', 
    'Democratic Republic of the Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 
    'Swaziland', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea Bissau', 'Kenya', 
    'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 
    'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe', 
    'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 
    'United Republic of Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Western Sahara', 'Zambia', 'Zimbabwe'
]

# Create GeoJSON for African countries
africa_geojson = {
    "type": "FeatureCollection",
    "features": [
        feature for feature in world_geojson["features"]
        if feature["properties"]["ADMIN"] in african_countries
    ]
}

# Debug print to check countries
print("Countries in the filtered data:")
for feature in africa_geojson["features"]:
    print(feature["properties"]["ADMIN"])

# Convert GeoJSON to string for embedding in HTML
africa_json_str = json.dumps(africa_geojson)

# Create the HTML content
html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>African Maps</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        body {{ margin: 0; padding: 0; font-family: Arial, sans-serif; }}
        #container {{ 
            display: flex; 
            width: 100%; 
            height: 100vh; 
            max-width: 1200px; 
            margin: 0 auto;
        }}
        #left-map, #right-map {{ 
            width: 50%; 
            height: 100%; 
            min-height: 500px;
        }}
        .leaflet-container {{ 
            background: white !important; 
            width: 100%;
            height: 100%;
        }}
        @media (max-width: 768px) {{
            #container {{ flex-direction: column; }}
            #left-map, #right-map {{ width: 100%; height: 50vh; }}
        }}
        .map-title {{
            position: fixed;
            top: 10px;
            width: 300px;
            z-index: 1000;
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-family: Arial, sans-serif;
        }}
        .map-title.left {{ left: 50px; }}
        .map-title.right {{ right: 50px; }}
        .source-button {{
            position: fixed;
            bottom: 10px;
            left: 50px;
            width: 300px;
            z-index: 1000;
            text-align: center;
            margin-bottom: 10px;
        }}
        .legend {{
            position: fixed;
            bottom: 20px;
            left: 50px;
            width: 300px;
            z-index: 1000;
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }}
        .legend.right {{
            left: auto;
            right: 50px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 5px 0;
            font-size: 12px;
        }}
        .legend-color {{
            width: 20px;
            height: 20px;
            margin-right: 10px;
            border: 1px solid #FFFFFF;
        }}
    </style>
</head>
<body>
    <div id="container">
        <div id="left-map"></div>
        <div id="right-map"></div>
    </div>

    <div class="map-title left">
        <h3 style="margin: 0;">Access to Energy in Africa</h3>
    </div>

    <div class="map-title right">
        <h3 style="margin: 0;">Lendable's portfolio</h3>
    </div>

    <div class="legend">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 5px;">
            <span style="font-size: 12px;">Low</span>
            <div style="width: 200px; height: 20px; background: linear-gradient(to right, #fff2da, #FFB800); margin: 0 10px;"></div>
            <span style="font-size: 12px;">High</span>
        </div>
        <div style="font-size: 12px; margin-bottom: 40px;">Access to electricity (%)</div>
    </div>

    <div class="source-button">
        <a href="https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS" target="_blank" 
           style="display: inline-block; padding: 8px 16px; background-color: white; 
                  color: #000000; text-decoration: none; border-radius: 4px; 
                  font-size: 12px;">
            Source: World Bank Energy Access Data 2021
        </a>
    </div>

    <div class="legend right">
        <div class="legend-item">
            <div class="legend-color" style="background-color: #155B54;"></div>
            <span>Data available in Lendable's PAYGO benchmark</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #36c187;"></div>
            <span>Markets we have experience in</span>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        // Embedded GeoJSON data
        var africaData = {africa_json_str};

        // Initialize maps
        var leftMap = L.map('left-map', {{
            center: [0, 20],
            zoom: 3,
            zoomControl: false,
            attributionControl: false,
            scrollWheelZoom: false,
            doubleClickZoom: false,
            touchZoom: false,
            boxZoom: false,
            keyboard: false,
            dragging: false,
            minZoom: 3,
            maxZoom: 3,
            maxBounds: [[-40, -20], [40, 60]]
        }});

        var rightMap = L.map('right-map', {{
            center: [0, 20],
            zoom: 3,
            zoomControl: false,
            attributionControl: false,
            scrollWheelZoom: false,
            doubleClickZoom: false,
            touchZoom: false,
            boxZoom: false,
            keyboard: false,
            dragging: false,
            minZoom: 3,
            maxZoom: 3,
            maxBounds: [[-40, -20], [40, 60]]
        }});

        // Style for the countries
        function interpolateColor(color1, color2, factor) {{
            /* Convert hex to RGB */
            var r1 = parseInt(color1.slice(1,3), 16);
            var g1 = parseInt(color1.slice(3,5), 16);
            var b1 = parseInt(color1.slice(5,7), 16);
            var r2 = parseInt(color2.slice(1,3), 16);
            var g2 = parseInt(color2.slice(3,5), 16);
            var b2 = parseInt(color2.slice(5,7), 16);
            
            /* Interpolate */
            var r = Math.round(r1 + (r2 - r1) * factor);
            var g = Math.round(g1 + (g2 - g1) * factor);
            var b = Math.round(b1 + (b2 - b1) * factor);
            
            /* Convert back to hex */
            return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
        }}

        function getColor(d) {{
            /* Normalize the percentage to a value between 0 and 1 */
            var factor = Math.min(Math.max(d / 100, 0), 1);
            return interpolateColor('#fff2da', '#FFB800', factor);
        }}

        function style(feature) {{
            var countryName = feature.properties.ADMIN;
            var percentage = {json.dumps(energy_access)}[countryName] || 0;
            return {{
                fillColor: getColor(percentage),
                color: '#FFFFFF',
                weight: 2,
                fillOpacity: 1.0,
                opacity: 1.0,
                dashArray: ''
            }};
        }}

        // Add GeoJSON to both maps
        L.geoJSON(africaData, {{
            style: style,
            onEachFeature: function(feature, layer) {{
                var countryName = feature.properties.ADMIN;
                var percentage = {json.dumps(energy_access)}[countryName] || 0;
                layer.bindTooltip(countryName + '<br>Energy access: ' + percentage + '%', {{
                    permanent: false,
                    direction: 'center'
                }});
            }}
        }}).addTo(leftMap);

        L.geoJSON(africaData, {{
            style: function(feature) {{
                var countryName = feature.properties.ADMIN;
                /* Check if country is in the dark green list */
                var darkGreenCountries = ['Benin', 'Nigeria', 'Kenya', 'United Republic of Tanzania', 'Zambia', 'Mozambique'];
                /* Check if country is in the light green list */
                var lightGreenCountries = ['Senegal', 'Mali', 'Ghana', 'Ivory Coast', 'Uganda'];
                
                if (darkGreenCountries.includes(countryName)) {{
                    return {{
                        fillColor: '#155B54',
                        color: '#FFFFFF',
                        weight: 2,
                        fillOpacity: 1.0,
                        opacity: 1.0,
                        dashArray: ''
                    }};
                }}
                if (lightGreenCountries.includes(countryName)) {{
                    return {{
                        fillColor: '#36c187',
                        color: '#FFFFFF',
                        weight: 2,
                        fillOpacity: 1.0,
                        opacity: 1.0,
                        dashArray: ''
                    }};
                }}
                return {{
                    fillColor: '#CCCCCC',
                    color: '#FFFFFF',
                    weight: 2,
                    fillOpacity: 1.0,
                    opacity: 1.0,
                    dashArray: ''
                }};
            }},
            onEachFeature: function(feature, layer) {{
                layer.bindTooltip(feature.properties.ADMIN, {{
                    permanent: false,
                    direction: 'center'
                }});
            }}
        }}).addTo(rightMap);
    </script>
</body>
</html>
'''

# Save the HTML file
with open('paygo_benchmark.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Map has been created! Open paygo_benchmark.html in your web browser to view both maps side by side.") 