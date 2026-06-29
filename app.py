import osmnx as ox
import folium
from folium.plugins import MarkerCluster, HeatMap, Search

place = "Tashkent, Uzbekistan"

tags = {
    "amenity": ["hospital", "pharmacy"]
}

gdf = ox.features_from_place(place, tags)
hospital_count = len(gdf[gdf["amenity"] == "hospital"])
pharmacy_count = len(gdf[gdf["amenity"] == "pharmacy"])


print("Kasalxonalar:", hospital_count)
print("Dorixonalar:", pharmacy_count)

stats_html = f"""
<div style="
position: fixed;
top: 80px;
left: 50px;
width: 250px;
height: 120px;
background: linear-gradient(135deg,#0f172a,#1e293b);
color: white;
border-radius: 15px;
box-shadow: 0 4px 15px rgba(0,0,0,0.4);
z-index:9999;
padding:15px;
font-size:16px;
font-family:Arial;
">

<h4 style="margin-top:0;color:#38bdf8;">
📊 Statistika
</h4>

🏥 Kasalxonalar:
<b>{hospital_count}</b>

<br><br>

💊 Dorixonalar:
<b>{pharmacy_count}</b>

</div>
"""
m = folium.Map(
    location=[41.3111, 69.2797],
    zoom_start=11
)

m.get_root().html.add_child(folium.Element(stats_html))

legend_html = """
<div style="
position: fixed;
bottom: 50px;
left: 50px;
width: 180px;
height: 80px;
background-color: white;
border:2px solid grey;
z-index:9999;
padding:10px;
font-size:14px;
">

<b>Legenda</b><br>

<span style="color:red;">⬤</span> Kasalxona<br>

<span style="color:green;">⬤</span> Dorixona

</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))
heat_data = []
hospital_group = folium.FeatureGroup(name="Kasalxonalar")
pharmacy_group = folium.FeatureGroup(name="Dorixonalar")

m.add_child(hospital_group)
m.add_child(pharmacy_group)

search_group = folium.FeatureGroup(name="Search")
m.add_child(search_group)

for idx, row in gdf.iterrows():

    if row.geometry.geom_type == "Point":
        heat_data.append([
            row.geometry.y,
            row.geometry.x
        ])

        amenity = row.get("amenity", "")
        lat = row.geometry.y
        lon = row.geometry.x

        google_maps = f"https://www.google.com/maps?q={lat},{lon}"
        color = "blue"

        if amenity == "hospital":
            color = "red"

        elif amenity == "pharmacy":
            color = "green"
        target_group = pharmacy_group

        if amenity == "hospital":
            target_group = hospital_group
        folium.Marker(
            location=[
                row.geometry.y,
                row.geometry.x
            ],
            popup=f"""
<div style="width:220px">

<h4 style="color:#0d6efd;">
🏥 {row.get('name', 'Nomaʼlum')}
</h4>

<hr>

<b>📌 Turi:</b> {amenity}<br>

<b>📞 Telefon:</b>
{row.get('phone', 'Mavjud emas')}<br>

<b>📍 Manzil:</b><br>
{row.get('addr:street', 'Mavjud emas')}

<br><br>

<a href="{google_maps}" target="_blank"
style="
background:#0d6efd;
color:white;
padding:8px 12px;
text-decoration:none;
border-radius:8px;
font-weight:bold;
display:inline-block;
">
🗺 Google Maps
</a>

</div>
""",
            icon=folium.Icon(
    color=color,
    icon="plus-sign" if amenity == "hospital" else "shopping-cart",
    prefix="glyphicon"
)
        ).add_to(target_group)
        folium.Marker(
    location=[
        row.geometry.y,
        row.geometry.x
    ],
    popup=str(row.get("name", "Nomalum")),
    tooltip=str(row.get("name", "Nomalum"))
).add_to(search_group)
heatmap_group = folium.FeatureGroup(name="HeatMap")

HeatMap(heat_data).add_to(heatmap_group)

heatmap_group.add_to(m)
search_group.layer_name = "Search"
Search(
    layer=search_group,
    search_label="name",
    placeholder="Kasalxona yoki dorixona qidirish...",
    collapsed=False,
    position="topright"
).add_to(m)
folium.LayerControl().add_to(m)

m.save("tashkent_healthcare_map.html")

print("Xarita yaratildi!")