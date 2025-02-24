import streamlit as st
import pandas as pd
df_sku_search = pd.read_excel("Master.xlsx")
# Load your Excel files (replace with your paths)
supplier_brands_df = pd.read_excel("supplier_brands.xlsx")
tire_brands_df = pd.read_excel("tire_brands.xlsx")
df = pd.read_excel("brand_segmant.xlsx")
discount_df = pd.read_excel("supplier_discount.xlsx")
supplier_discounts = {
    (row["supplier"], row["brand"]): row["discount"] for _, row in discount_df.iterrows()
}
brand_to_category = dict(zip(tire_brands_df["Brand"], tire_brands_df["Category"]))

# Function for price calculation
def calculate_price(df):
    st.header("Final Price Calculator")
    unique_suppliers = supplier_brands_df["Supplier"].unique()
    selected_supplier = st.selectbox("Choose a Supplier:", unique_suppliers)
    if selected_supplier=="Tamco":
        associated_brands=supplier_brands_df["Brand"].unique()
        if len(associated_brands) == 0:
            st.warning(f"No brands found for the selected supplier: {selected_supplier}")
            return
    else:
        associated_brands = supplier_brands_df[supplier_brands_df["Supplier"] == selected_supplier]["Brand"].unique()
        if len(associated_brands) == 0:
            st.warning(f"No brands found for the selected supplier: {selected_supplier}")
            return

    selected_brand = st.selectbox("Choose a tire brand:", associated_brands)
    category = brand_to_category.get(selected_brand, None)
    size = st.selectbox("Select Size:", df["Size"].unique())
    cost_value = st.number_input("Enter Cost:")

    if st.button("Calculate Price"):
        discount = supplier_discounts.get((selected_supplier, selected_brand),
                                          supplier_discounts.get((selected_supplier, "all"), 0))
        result = df[(df["Category"] == category) & (df["Size"] == size)]
        if not result.empty:
            profit_value = result["Value"].values[0]
            discounted_cost = cost_value * (1 - discount / 100)
            discounted_cost = discounted_cost * 100 / 114
            total_value = ((discounted_cost * profit_value) + 102 + 150) * 1.14 + (((discounted_cost * profit_value) + 102 + 150) * 1.14) * .04

            st.title(f"Total Price: {round(total_value + 2)} INC VAT")
        else:
            st.warning("No matching data found for the selected category and size.")

# Another function (PO Calc)
def show_PO_Calc():
    st.header("purchase order")
    unique_suppliers2 = supplier_brands_df["Supplier"].unique()
    selected_supplier = st.selectbox("Choose  Supplier :", unique_suppliers2)
    associated_brands2 = supplier_brands_df[supplier_brands_df["Supplier"] == selected_supplier]["Brand"].unique()

    if len(associated_brands2) == 0:
        st.warning(f"No brands found for the selected supplier: {selected_supplier}")
        return
    selected_brand = st.selectbox("Choose tire brand:", associated_brands2)    
    cost_value = st.number_input("Enter Cost")
    
    if st.button("Calculate purchase order Price"):
        discount = supplier_discounts.get((selected_supplier, selected_brand),
                                          supplier_discounts.get((selected_supplier, "all"), 0))


        discounted_cost = cost_value * (1 - discount / 100)


        st.title(f"Total purchase order: {round(discounted_cost)} INC VAT")


def sku_search(df):
# Streamlit App Title
    st.title("SKU Search")

    # Define the columns to display
    columns_to_display = ["Supplier", "sku", "Brand", "Size"]

    # Search Bar and Button
    search_sku = st.text_input("Enter SKU to search:", "")
    search_button = st.button("Search")

    # Perform the search only when the button is clicked
    if search_button and search_sku:
        # Filter for Live SKUs
        live_df = df[
        (df["sku"].str.contains(search_sku, case=False, na=False)) &
        (df["Sku Status on The Website"] == "Live")
    ]
    
        # Filter for Not Live SKUs
        not_live_df = df[
        (df["sku"].str.contains(search_sku, case=False, na=False)) &
        (df["Sku Status on The Website"] != "Live")
        ]
    
        # Display results for Live SKUs
        if not live_df.empty:
            st.write(f"**Results for Live SKUs matching '{search_sku}':**")
            # Extract unique suppliers for Live SKUs
            live_suppliers = live_df["Supplier"].unique()
            live_suppliers_text = ", ".join(live_suppliers)
            st.write(f"The live SKU on the website is  from : **{live_suppliers_text}** Supplier")
            st.dataframe(live_df[columns_to_display])  # Display only selected columns
        else:
            st.write(f"No live SKUs found for '{search_sku}'")

        # Display results for Not Live SKUs
        if not not_live_df.empty:
            # Extract unique suppliers for Not Live SKUs
            not_live_suppliers = not_live_df["Supplier"].unique()
            not_live_suppliers_text = ", ".join(not_live_suppliers)
            st.write(f"Same sku But From other Supplier: **{not_live_suppliers_text}** Supplier")
            st.dataframe(not_live_df[columns_to_display])  # Display only selected columns




def Supplier_Brand_Search(df):
    st.header("Brand Search")

    # Ensure the DataFrame contains the expected columns
    if "Brand" in df.columns and "Supplier" in df.columns:
        unique_brands = df["Brand"].unique()
        selected_brand = st.selectbox("Choose a Brand:", unique_brands)

        # Filter suppliers based on the selected brand
        filtered_suppliers = df[df["Brand"] == selected_brand]["Supplier"].unique()


        st.subheader("Suppliers offering this brand:")
        for supplier in filtered_suppliers:
            st.markdown(f"<h3 style='color:blue;'>{supplier}</h3>", unsafe_allow_html=True)


        return selected_brand, filtered_suppliers
    else:
        st.error("The DataFrame does not contain the required 'Brand' or 'Supplier' columns.")
        return None, None

    



# Tabs interface
tabs = st.tabs(["Price Calculator", "purchase order","Sku Search","Supplier Brand Search"])
with tabs[0]:
    calculate_price(df)

with tabs[1]:
    show_PO_Calc()

with tabs[2]:
    sku_search(df_sku_search)

with tabs[3]:
    Supplier_Brand_Search(df_sku_search)

