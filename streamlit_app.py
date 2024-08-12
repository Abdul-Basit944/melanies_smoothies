import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie")
st.write("Choose The Fruit You want in your Custom Smoothie")

# Input for name on the smoothie
name_on_order = st.text_input('Name on Smoothie:')
st.write('The Name on your Smoothie will be:', name_on_order)

# Get active Snowflake session
session = get_active_session()

# Fetch fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Convert to a list for the multi-select
fruit_options = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

# Multi-select for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 Ingredients:',
    fruit_options
)

if ingredients_list:
    # Build the ingredients string
    ingredients_string = ' '.join(ingredients_list)

    # Create the SQL insert statement
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')"""

    # Display the generated SQL statement for debugging
    st.write("Generated SQL Statement:", my_insert_stmt)

    # Display the submit button
    if st.button('Submit Order'):
        try:
            # Execute the SQL insert statement
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred: {e}")
























