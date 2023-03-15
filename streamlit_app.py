import streamlit
import pandas
import requests
import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.header("Fruit List")
streamlit.dataframe(my_data_row)


new_fruit = streamlit.text_input('which fruit would you like to add')
streamlit.write('Thanks for adding ', new_fruit)

#my_cur.execute("INSERT INTO FRUIT_LOAD_LIST(FRUITNAME) VALUES ("+new_fruit+")")


streamlit.title('My parents Healthy Diner')


streamlit.header('🥣  Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 🐔  Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')


streamlit.text('Onzin')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
 

streamlit.dataframe(my_fruit_list)




# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected] 

streamlit.dataframe(fruits_to_show)

#streamlit json/api call


# streamlit api call section

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#display results  
streamlit.header("Fruityvice Fruit Advice!")  
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("please select a fruit for info")
    else:
       back_from_function = get_fruityvice_data(fruit_choice)
    # displays the dataframe on the webpage
       streamlit.dataframe(back_from_function)
     
except URLError as e:
    streamlit.error()