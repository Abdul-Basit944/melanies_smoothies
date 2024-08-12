import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd 

st.title(":cup_with_straw: Customize Your Smoothie")
st.write("Choose the Fruit You Want in Your Custom Smoothie")

# Input for name on the smoothie
name_on_order = st.text_input('Name on Smoothie:')
st.write('The Name on your Smoothie will be:', name_on_order)

# Create a connection to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON')).to_pandas()

# Convert to a list for the multi-select
fruit_options = my_dataframe['FRUIT_NAME'].tolist()

# Multi-select for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 Ingredients:',
    fruit_options
)

if ingredients_list:
    # Build the ingredients string
    ingredients_string = ' '.join(ingredients_list)

    for fruit_chosen in ingredients_list:
        # Find the corresponding SEARCH_ON value
        search_on = my_dataframe.loc[my_dataframe['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write(f'The search value for {fruit_chosen} is {search_on}.')

        # Display nutrition information
        st.subheader(f'{fruit_chosen} Nutrition Information')
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        fruityvice_data = fruityvice_response.json()
        st.dataframe(pd.DataFrame(fruiyvice_data), use_container_width=True)

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

























