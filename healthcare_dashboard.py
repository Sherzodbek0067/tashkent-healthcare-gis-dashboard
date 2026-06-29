from io import BytesIO
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import osmnx as ox

place = "Tashkent, Uzbekistan"

tags = {
    "amenity": ["hospital", "pharmacy"]
}

@st.cache_data
def load_data():
    return ox.features_from_place(place, tags)

gdf = load_data()
# st.write(gdf.columns.tolist())
# gdf = gdf[gdf["amenity"].isin(filter_type)]
hospital_count = len(gdf[gdf["amenity"] == "hospital"])
pharmacy_count = len(gdf[gdf["amenity"] == "pharmacy"])
total_count = hospital_count + pharmacy_count
st.set_page_config(
    page_title="Healthcare GIS Dashboard",
    page_icon="🏥",
    layout="wide"
)
st.sidebar.divider()
st.sidebar.subheader("🎨 Dashboard Theme")

theme = st.sidebar.radio(
    "Mavzu",
    ["🌞 Light", "🌙 Dark"]
)

if theme == "🌙 Dark":
    st.markdown("""
    <style>
    .stApp{
        background-color:#0E1117;
        color:white;
    }

    section[data-testid="stSidebar"]{
        background-color:#1B1F2A;
    }

    h1,h2,h3,h4,h5,h6{
        color:white !important;
    }

    </style>
    """, unsafe_allow_html=True)
st.title("🏥 Tashkent Healthcare GIS Dashboard")
st.sidebar.title("⚙ Dashboard")

filter_type = st.sidebar.multiselect(
    "Ko'rsatilsin:",
    ["hospital", "pharmacy"],
    default=["hospital", "pharmacy"]
)
col1, col2, col3 = st.columns(3)


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="
        background:#1E88E5;
        padding:25px;
        border-radius:15px;
        text-align:center;
        color:white;
        box-shadow:0px 4px 10px rgba(0,0,0,0.3);
    ">
        <h4>🏥 Kasalxonalar</h4>
        <h1>{hospital_count}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background:#43A047;
        padding:25px;
        border-radius:15px;
        text-align:center;
        color:white;
        box-shadow:0px 4px 10px rgba(0,0,0,0.3);
    ">
        <h4>💊 Dorixonalar</h4>
        <h1>{pharmacy_count}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background:#E53935;
        padding:25px;
        border-radius:15px;
        text-align:center;
        color:white;
        box-shadow:0px 4px 10px rgba(0,0,0,0.3);
    ">
        <h4>📍 Jami</h4>
        <h1>{total_count}</h1>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

left, right = st.columns(2)

data = pd.DataFrame({
    "Tur": ["Kasalxonalar", "Dorixonalar"],
    "Soni": [206, 978]
})
with left:
    fig = px.pie(
        data,
        values="Soni",
        names="Tur",
        hole=0.5,
        title="Healthcare Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig2 = px.bar(
        data,
        x="Tur",
        y="Soni",
        color="Tur",
        text="Soni",
        title="Healthcare Comparison"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("🗺 Tashkent Healthcare Interactive Map")

with open("tashkent_healthcare_map.html", "r", encoding="utf-8") as f:
    html = f.read()

components.html(
    html,
    height=750,
    scrolling=True
)
st.divider()


# table = gdf[["name", "amenity", "addr:street"]].copy()

# table.columns = [
#     "Nomi",
#     "Turi",
#     "Ko'chasi"
# ]
st.subheader("🔍 Healthcare Objects")

search = st.text_input(
    "Kasalxona yoki dorixona nomini kiriting:"
)

# table = gdf[
#     ["element", "id", "name", "amenity", "addr:street"]
# ].copy()

# table.columns = [
#     "Element",
#     "ID",
#     "Nomi",
#     "Turi",
#     "Ko'chasi"
# ]
table = gdf[
    ["name", "amenity", "addr:street"]
].copy()

table.columns = [
    "Nomi",
    "Turi",
    "Ko'chasi"
]
if search:
    table = table[
        table["Nomi"].astype(str).str.contains(
            search,
            case=False,
            na=False
        )
    ]
st.dataframe(
    table,
    use_container_width=True,
    height=500
)
st.divider()

excel_buffer = BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    gdf.to_excel(writer, index=False, sheet_name="Healthcare")

excel_data = excel_buffer.getvalue()
st.download_button(
    label="📥 CSV yuklab olish",
    data=gdf.to_csv(index=False).encode("utf-8"),
    file_name="tashkent_healthcare.csv",
    mime="text/csv"
)
st.download_button(
    label="📗 Excel yuklab olish",
    data=excel_data,
    file_name="tashkent_healthcare.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
st.divider()

st.markdown("""
---
### 👨‍💻 Developed by Sherzodbek Abdupattayev

🏥 **Healthcare GIS Dashboard**

📅 2026

Python • Streamlit • Folium • OSMnx • Plotly
""")