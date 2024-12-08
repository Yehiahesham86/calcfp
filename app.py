import streamlit as st
import pandas as pd

# Load the supplier-to-brands mapping
supplier_brands_df = pd.read_excel("supplier_brands.xlsx")  # Renamed for clarity

# Load the tire brands data and map each brand to its category
tire_brands_df = pd.read_excel("tire_brands.xlsx")
brand_to_category = dict(zip(tire_brands_df["Brand"], tire_brands_df["Category"]))

# Load the main DataFrame with categories, sizes, and values
df = pd.read_excel("brand_segmant.xlsx")

# Load the supplier discount data from Excel and create a dictionary
discount_df = pd.read_excel("supplier_discount.xlsx")
supplier_discounts = {
    (row["supplier"], row["brand"]): row["discount"] for _, row in discount_df.iterrows()
}

# Title of the app
st.title("Final Price Calculator")

# Function to calculate and display the profit value with supplier and brand discount
def calculate_profit_value(df):
    # Create a list of unique suppliers from the discount DataFrame
    unique_suppliers = supplier_brands_df["Supplier"].unique()
    selected_supplier = st.selectbox("Choose a Supplier:", unique_suppliers)

    # Filter the supplier_brands DataFrame to get brands associated with the selected supplier
    associated_brands = supplier_brands_df[supplier_brands_df["Supplier"] == selected_supplier]["Brand"].unique()

    # Check if there are any associated brands
    if len(associated_brands) == 0:
        st.warning(f"No brands found for the selected supplier: {selected_supplier}")
        return

    # Dropdown input for Brand (only show brands associated with the selected supplier)
    selected_brand = st.selectbox("Choose a tire brand:", associated_brands)

    # Get the category for the selected brand
    category = brand_to_category.get(selected_brand, None)

    # Dropdown input for Size
    size = st.selectbox("Select Size:", df["Size"].unique())

    # Numeric input field for cost value
    cost_value = st.number_input("Enter Cost:", min_value=1, step=1)

    # Button to calculate price
    if st.button("Calculate Price"):
        # Get the discount for the selected supplier and brand
        discount = supplier_discounts.get((selected_supplier, selected_brand),
                                          supplier_discounts.get((selected_supplier, "all"), 0))

        # Filter the DataFrame based on selected category and size
        result = df[(df["Category"] == category) & (df["Size"] == size)]

        # Check if result exists and display total price
        if not result.empty:
            profit_value = result["Value"].values[0]

            # Calculate the discounted cost after applying supplier and brand discount
            discounted_cost = cost_value * (1 - discount / 100)
            discounted_cost=discounted_cost * 100/114
            # Calculate the final price based on discounted cost
            if (size<=16):
                fitment_cost=50
                total_value = ( (discounted_cost * profit_value) +((discounted_cost *0.06) + fitment_cost) )* 1.14
            else:
                total_value = ( (discounted_cost * profit_value) +((discounted_cost *0.06) + 100) )* 1.14
            st.title(f"Total Price for ({cost_value}) after {discount}% discount: {round(total_value + 2)} INC VAT")
        else:
            st.warning("No matching data found for the selected category and size.")

# Call the function
calculate_profit_value(df)
