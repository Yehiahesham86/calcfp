import streamlit as st
import pandas as pd

tire_brands = {
    "Premium": [
        "Bridgestone", "Continental", "Goodyear", "Michelin", "Pirelli"
    ],
    "Quality": [
        "Cooper", "Dunlop", "Falken", "Firestone", "Fulda", "General",
        "General Tire", "General Tyre", "Hankook", "Kumho", "Maxxis",
        "Mickey", "Mickey Thompson", "Nexen", "Sumitomo", "Toyo",
        "Toyo Tires", "Yokohama"
    ],
    "Budget 1": [
        "BF GOODRICH", "CooperTires", "Double Coin", "Federal", "JK",
        "Lassa", "Matrax", "Otani", "PETLAS", "Roadx", "Roadstone",
        "SAILUN", "Sava", "Starmax", "Tarazano", "TRAZANO", "Vredestein",
        "Zeetex"
    ],
    "Budget 2": [
        "Accelera", "Achilles", "Altenzo", "Annaite", "APLUS", "APTANY",
        "Arivo", "Armstrong", "Arroyo", "Atlas", "Atturo", "Bearway",
        "Berlin", "BLACK ARROW", "Blackarrow", "Blacklion", "BOTO",
        "Centara", "CHARMHOO", "Charmo", "Comoro", "compasal", "Davanti",
        "Dayton", "Deestone", "Doublestar", "Durun", "ETERNITY", "Fortune",
        "Frztrac", "Galaxia", "Getwin", "GoForm", "Goodride", "Gopro",
        "GREENLANDER", "Greenmax", "Greentrac", "GRIPMAX", "Groundspeed",
        "Habilead", "Headway", "HEDOVIC", "HILLO", "HILO", "Honour",
        "Horizon", "Ilink", "Infinity", "Joyroad", "KAPSEN", "Kenda",
        "KINFOREST", "LALBIGATOR", "Lancaster", "Landsail", "Landspider",
        "LANVIGATOR", "Laufenn", "LEAO", "Lexani", "Lexxis", "Longway",
        "LUISTONE", "Malone", "Marshal", "Massimo", "Maxtrek", "Mileking",
        "Miletrip", "Minnell", "Montreal", "Mosimo", "NAMA", "NANKANG",
        "NAVIGATOR", "Neupar", "Opals", "PALLY KING", "PALLYKING", "Pearly",
        "Prinx", "RIKEN", "Road March", "Roadboss", "Roadcruza", "Roadking",
        "ROADMARCH", "Roadwing", "Rotalla", "Rovelo", "ROYAL BLAK", "Rydanz",
        "SAILWIN", "Seam", "Shaheen", "Sonar", "SPORTRAK", "SunFull",
        "SUNNY", "TBB", "Teraflex", "Tesche", "Thunderer", "TRACKMAX",
        "TRACMAX", "Transmate", "Vitour", "VIZZONI", "Wanli", "WANLY",
        "West Lake", "WINDA", "Windforce", "WINRUN", "Zeta", "Zetum",
        "ZEXTOUR", "Zmax"
    ]
}

# Flatten the dictionary to map each brand to its category
brand_to_category = {brand: category for category, brands in tire_brands.items() for brand in brands}


# Show the category for the selected brand

# Create a DataFrame with the given data
data = {
    "Category": ["Premium", "Premium", "Premium", "Premium", "Premium", "Premium", "Premium", "Premium", "Premium", "Premium", "Premium", "Premium",
                 "Quality", "Quality", "Quality", "Quality", "Quality", "Quality", "Quality", "Quality", "Quality", "Quality", "Quality", "Quality",
                 "Budget 1", "Budget 1", "Budget 1", "Budget 1", "Budget 1", "Budget 1", "Budget 1", "Budget 1", "Budget 1", "Budget 1", "Budget 1", "Budget 1",
                 "Budget 2", "Budget 2", "Budget 2", "Budget 2", "Budget 2", "Budget 2", "Budget 2", "Budget 2", "Budget 2", "Budget 2", "Budget 2", "Budget 2"],
    "helper": ["Premium12", "Premium13", "Premium14", "Premium15", "Premium16", "Premium17", "Premium18", "Premium19", "Premium20", "Premium21", "Premium22", "Premium23",
               "Quality12", "Quality13", "Quality14", "Quality15", "Quality16", "Quality17", "Quality18", "Quality19", "Quality20", "Quality21", "Quality22", "Quality23",
               "Budget 112", "Budget 113", "Budget 114", "Budget 115", "Budget 116", "Budget 117", "Budget 118", "Budget 119", "Budget 120", "Budget 121", "Budget 122", "Budget 123",
               "Budget 212", "Budget 213", "Budget 214", "Budget 215", "Budget 216", "Budget 217", "Budget 218", "Budget 219", "Budget 220", "Budget 221", "Budget 222", "Budget 223"],
    "Size": [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
             12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
             12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
             12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    "Value": [1.15, 1.15, 1.15, 1.15, 1.15, 1.14, 1.14, 1.14, 1.12, 1.1, 1.1, 1.1,
              1.2, 1.2, 1.2, 1.2, 1.15, 1.16, 1.18, 1.18, 1.18, 1.15, 1.15, 1.15,
              1.18, 1.18, 1.18, 1.18, 1.15, 1.15, 1.15, 1.15, 1.15, 1.15, 1.15, 1.15,
              1.23, 1.23, 1.23, 1.23, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2]
}

df = pd.DataFrame(data)

# Title of the app
st.title("Final Price Calculator")

# Dropdown input for Category



def calculate_profit_value(df):
    # Create a dropdown list for brands
    selected_brand = st.selectbox("Choose a tire brand:", list(brand_to_category.keys()))

    # Dropdown input for Category
    category = brand_to_category[selected_brand]

    # Dropdown input for Size
    size = st.selectbox("Select Size:", df["Size"].unique())

    # Numeric input field for quantity (multiplier)
    cost_value = st.number_input("Enter Cost :", min_value=1, step=1)

    # Button to calculate profit value
    if st.button("Calculate Price"):
        # Filter the DataFrame based on selected inputs
        result = df[(df["Category"] == category) & (df["Size"] == size)]
        
        # Check if result exists and display profit value
        if not result.empty:
            profit_value = result["Value"].values[0]
            total_value = (cost_value+((cost_value*.165)+(cost_value*0.02)+150))*profit_value
            st.title(f"Total Price For ({cost_value}): {round(total_value+2)}")
        else:
            st.title("No matching data found.")

# Call the function
calculate_profit_value(df)