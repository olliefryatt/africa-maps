import folium
import geopandas as gpd
import requests
import json

# Download GeoJSON data for African countries
url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
response = requests.get(url)
world_geojson = response.json()

# Financial inclusion data (account ownership %)
financial_inclusion = {
    'Algeria': 50.3,
    'Angola': 45.2,
    'Benin': 42.5,
    'Botswana': 67.8,
    'Burkina Faso': 46.2,
    'Burundi': 7.2,
    'Cameroon': 35.5,
    'Cape Verde': 67.3,
    'Central African Republic': 14.2,
    'Chad': 11.8,
    'Comoros': 19.8,
    'Republic of Congo': 41.2,
    'Ivory Coast': 45.2,
    'Democratic Republic of the Congo': 33.2,
    'Djibouti': 41.5,
    'Egypt': 32.8,
    'Equatorial Guinea': 35.2,
    'Eritrea': 22.3,
    'Swaziland': 44.8,
    'Ethiopia': 46.6,
    'Gabon': 48.2,
    'Gambia': 33.5,
    'Ghana': 68.2,
    'Guinea': 24.5,
    'Guinea Bissau': 28.2,
    'Kenya': 79.8,
    'Lesotho': 38.5,
    'Liberia': 44.2,
    'Libya': 35.8,
    'Madagascar': 13.8,
    'Malawi': 22.5,
    'Mali': 35.2,
    'Mauritania': 33.8,
    'Mauritius': 89.2,
    'Morocco': 44.5,
    'Mozambique': 32.5,
    'Namibia': 58.2,
    'Niger': 15.8,
    'Nigeria': 45.3,
    'Rwanda': 60.2,
    'Sao Tome and Principe': 42.8,
    'Senegal': 45.5,
    'Seychelles': 85.2,
    'Sierra Leone': 32.8,
    'Somalia': 15.2,
    'South Africa': 85.2,
    'South Sudan': 8.5,
    'Sudan': 28.5,
    'United Republic of Tanzania': 65.2,
    'Togo': 35.8,
    'Tunisia': 67.8,
    'Uganda': 58.2,
    'Western Sahara': 35.2,
    'Zambia': 45.8,
    'Zimbabwe': 45.2
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
            bottom: 20px;
            right: 50px;
            z-index: 1000;
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
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
    </style>
</head>
<body>
    <div id="container">
        <div id="left-map"></div>
        <div id="right-map"></div>
    </div>

    <div class="map-title left">
        <h3 style="margin: 0;">Financial Inclusion in Africa</h3>
    </div>

    <div class="map-title right">
        <h3 style="margin: 0;">Countries worked in</h3>
    </div>

    <div class="source-button">
        <a href="https://globalfindex.worldbank.org/" target="_blank" 
           style="display: inline-block; padding: 8px 16px; background-color: #CCCCCC; 
                  color: #000000; text-decoration: none; border-radius: 4px; 
                  font-size: 12px; font-weight: bold;">
            Source: World Bank Global Findex Database 2021
        </a>
    </div>

    <div class="legend">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 5px;">
            <span style="font-size: 12px;">Low</span>
            <div style="width: 200px; height: 20px; background: linear-gradient(to right, #C0E0D0, #0A2F2B); margin: 0 10px;"></div>
            <span style="font-size: 12px;">High</span>
        </div>
        <div style="font-size: 12px;">Account ownership percentage</div>
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
            return interpolateColor('#C0E0D0', '#0A2F2B', factor);
        }}

        function style(feature) {{
            var countryName = feature.properties.ADMIN;
            var percentage = {json.dumps(financial_inclusion)}[countryName] || 0;
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
                var percentage = {json.dumps(financial_inclusion)}[countryName] || 0;
                layer.bindTooltip(countryName + '<br>Account ownership: ' + percentage + '%', {{
                    permanent: false,
                    direction: 'center'
                }});
            }}
        }}).addTo(leftMap);

        L.geoJSON(africaData, {{
            style: function(feature) {{
                var countryName = feature.properties.ADMIN;
                /* Check if country is in the purple list */
                var purpleCountries = ['Senegal', 'Mali', 'Ghana', 'Ivory Coast', 'Nigeria', 'Uganda', 'Kenya'];
                if (purpleCountries.includes(countryName)) {{
                    return {{
                        fillColor: '#282828',
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
with open('africa_maps.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Map has been created! Open africa_maps.html in your web browser to view both maps side by side.") 