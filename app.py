import streamlit as st
import pandas as pd

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
            if size <= 16:
                fitment_cost = 150
                total_value = (((discounted_cost * profit_value) +  fitment_cost + 150 ))  + (((((discounted_cost * profit_value) +  fitment_cost + 150)) * 1.14) * 0.04)* 1.14
            else:
                total_value = (((discounted_cost * profit_value) +  fitment_cost + 150 ))  + (((((discounted_cost * profit_value) +  fitment_cost + 150)) * 1.14) * 0.04)* 1.14
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


# Tabs interface
tabs = st.tabs(["Price Calculator", "purchase order"])
with tabs[0]:
    calculate_price(df)

with tabs[1]:
    show_PO_Calc()
