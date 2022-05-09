"""
Name:       Soleil Maldonado
CS230:      Section 2
Data:       UFO Sightings Data Set
URL:        Link to your web application online

Description:

In this program, I created a sidebar to allow the user to navigate and learn about Australia, Great Britain, Canada, and
the United States and the different UFO sightings that were reported in each country. In each country section, I included
a slider that allows the user to pick a year and see how many sightings were reported and where in the country they were
reported by including a map underneath the slider. The map updates every time the user chooses a new year. Underneath the
map, each country section has a different chart that depicts a specific aspect of the data (Example: 'Top 10 States with
the most reported sightings'). After the user looks through each of the sections, there's one final section that tests
the user's knowledge about the information from the app. I included 5 questions.

"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import streamlit_book as stb


df_ufo = pd.read_csv('ufo_sightings_8000_sample.csv')  # dataframe
df_ufo.rename(columns={"latitude": "lat", "longitude": "lon"}, inplace=True)


# To print the entire dataframe using pd.set_option()
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'max_colwidth', None)

# index: default index
# columns: datetime, city, state, country, shape, 'duration (seconds)', duration (hours/min), comments, 'date posted', lat, lon

# Original dataframe, will be used to analyze data for countries that might have empty values
df_ufo['datetime'] = pd.to_datetime(df_ufo['datetime'])
df_ufo['country'] = df_ufo['country'].str.upper()
sorted_ufo = df_ufo.sort_values(by=['datetime'], ascending=True)
new_df = sorted_ufo.dropna()

# Updated dataframe, has no empty values
new_df['datetime'] = pd.to_datetime(sorted_ufo['datetime'])
new_df['country'] = new_df['country'].str.upper()

# US States Dataframe
us_df = sorted_ufo.loc[sorted_ufo['country'] == 'US'][['datetime', 'state', 'city', 'country', 'lat', 'lon']]
us_df['datetime'] = pd.to_datetime(sorted_ufo['datetime'])

# Great Britain Dataframe
uk_df = sorted_ufo.loc[sorted_ufo['country'] == 'GB'][['datetime', 'duration (seconds)', 'city', 'country', 'comments', 'lat', 'lon']]
uk_df['datetime'] = pd.to_datetime(sorted_ufo['datetime'])

# Canada Dataframe
ca_df = sorted_ufo.loc[sorted_ufo['country'] == 'CA'][['datetime', 'city', 'country', 'lat', 'lon']]
ca_df['datetime'] = pd.to_datetime(sorted_ufo['datetime'])

# Australia Dataframe
au_df = sorted_ufo.loc[sorted_ufo['country'] == 'AU'][['datetime', 'city', 'country', 'lat', 'lon']]
au_df['datetime'] = pd.to_datetime(sorted_ufo['datetime'])


def year_sightings(year, country):  # Function that returns the total number of reports from the inputted country for the specified year

    # Check if the inputted year is in the dataframe
    if sorted_ufo['datetime'].__contains__(year):

        # Capitalizes the first letter each city name
        sorted_ufo['city'] = sorted_ufo['city'].str.title()

        # Creates a new dataframe that is filtered by the specified year and country that was inputted by the user
        user_year = sorted_ufo.loc[(sorted_ufo['year'] == year) & (sorted_ufo['country'] == country.upper()), ['datetime', 'city', 'country']]
        year_sightings = len(user_year)

        # Checks which country was inputted by the user and outputs the number of sightings
        if country.upper() == 'AU':
            msg = f"In {year}, Australia had a total of {year_sightings} reported sightings!"
            return msg
        elif country.upper() == 'GB':
            msg = f"In {year}, Great Britain had a total of {year_sightings} reported sightings!"
            return msg
        elif country.upper() == 'CA':
            msg = f"In {year}, Canada had a total of {year_sightings} reported sightings!"
            return msg
        elif country.upper() == 'US':
            msg = f"In {year}, the United States had a total of {year_sightings} reported sightings!"
            return msg
        else:
            msg = 'Please enter one of the suggested countries above.'
            return msg

    # Returns the message below if the country does not have any reported sightings for the specified year
    else:
        return f"{country.upper()} were no reported sightings in {year}"


def main():  # Main function where the user interaction will be displayed
    sorted_ufo['year'] = pd.DatetimeIndex(sorted_ufo['datetime']).year
    years = list(sorted_ufo['year'])
    years.sort()
    choose_country = st.text_input('Choose a country (US, AU, GB, or CA) to view the number of sightings for the specified year:')
    choose_year = st.select_slider('Choose a year to view the number of sightings: ', years)

    if len(choose_country) > 0:
        st.write(year_sightings(choose_year, choose_country))
        user_year = sorted_ufo.loc[(sorted_ufo['year'] == choose_year) & (sorted_ufo['country'] == choose_country.upper()), ['datetime', 'city', 'country']]
        st.write(user_year)
    else:
        st.write('Please choose a country to view its reported sightings for the selected year')


# Sets the layout of the app as wide
st.set_page_config(layout="wide")

# Sidebar: user will be able to choose between seeing worldwide stats, US stats, AU stats, GB stats, or CA stats
st.sidebar.title("UFO Sightings")
where = ['Worldwide', 'United States', 'Great Britain', 'Australia', 'Canada', 'Test Your Knowledge']
selected_where = st.sidebar.selectbox('Please select where in the world you are interested in looking at: ', where)

# Sidebar expander gives a brief explanation of the purpose of this app
with st.sidebar.expander('About This Project'):
    st.write('The purpose of this project is to show how the number of UFO sightings worldwide differentiate.')

# Sidebar image of a UFO
st.sidebar.image(r'https://www.gannett-cdn.com/media/2019/04/05/USATODAY/usatsports/gettyimages-501124314.jpg')


# First option is worldwide (default)
if selected_where == 'Worldwide':

    # Created columns to display a cover image at the top of this section
    col1, col2, col3 = st.columns([1,8,1])
    with col1:
        st.write("")
    with col2:
        image = r'https://fbcoverstreet.com/thumbnail/QoSgRxnqSWGf3HlAY9gZSY9fgQsFdrd6mQMlJbl5DRCPApDQBSF9VUZ1pw9AFiMj.webp'
        st.image(image, width=800)
    with col3:
        st.write("")

    st.title("UFO Sightings Around the World")

    # Calls the main function
    main()

    # Displays a simple map of the world to show the most active UFO areas
    st.map(df_ufo)

    # Store number of sightings per country
    # usa, au, gb, and ca
    countries_dict = {}
    countries_list = list(sorted_ufo['country'])
    freq = 0
    freq1 = 0
    freq2 = 0
    freq3 = 0

    for j in range(len(countries_list)):
        country = countries_list[j]
        if country == 'US':
            if country not in countries_dict:
                countries_dict[country] = freq + 0
            elif country in countries_dict:
                countries_dict[country] = freq
                freq += 1
        elif country == 'AU':
            if country not in countries_dict:
                countries_dict[country] = freq1 + 0
            elif country in countries_dict:
                countries_dict[country] = freq1
                freq1 += 1
        elif country == 'GB':
            if country not in countries_dict:
                countries_dict[country] = freq2 + 0
            elif country in countries_dict:
                countries_dict[country] = freq2
                freq2 += 1
        elif country == 'CA':
            if country not in countries_dict:
                countries_dict[country] = freq3 + 0
            elif country in countries_dict:
                countries_dict[country] = freq3
                freq3 += 1

    # create bar chart showing the number of sightings per countries (usa, aus, can, gb)
    countries = list(countries_dict.keys())
    country_sightings = list(countries_dict.values())

    fig, ax = plt.subplots()
    ax.bar(countries, country_sightings, color='green')
    plt.title('Reported Sightings Worldwide per Country')
    plt.xlabel('Country')
    plt.ylabel('Total # of Sightings')

    # scatter plot that shows the changes in worldwide sightings from 1931-2014
    years_list = sorted_ufo['year']
    years_dict = {}

    for i in years_list:
        years_dict[i] = years_dict.get(i, 0) + 1

    sorted_years_dict = dict(sorted(years_dict.items(), key=lambda item: item[1]))

    year = list(sorted_years_dict.keys())
    sightings = list(sorted_years_dict.values())

    fig2, ax2 = plt.subplots()
    ax2.scatter(year, sightings, marker="*")
    plt.title('Reported Sightings Worldwide')
    plt.legend(['Sightings'])

    max_sightings = max(sightings)
    max_year = max(sorted_years_dict, key=sorted_years_dict.get)

    # Which year had the most reported UFO sightings
    st.success(f'Fun Fact: {max_year} was the year with the most reported sightings: {max_sightings}')

    col1, col2, col3, col4 = st.columns([1,4,4,1])
    with col1:
        st.write("")
    with col2:
        st.pyplot(fig2)
    with col3:
        st.pyplot(fig)
        with st.expander(' * Bar Chart Disclaimer * '):
            st.write("This bar char includes USA sightings with empty state values. In the USA section of this app, "
                     "the data presented won't include empty values. Dropping empty values resulted in a lower number "
                     "of total reported sightings")
    with col3:
        st.write("")

# Second option: United States
elif selected_where == 'United States':
    st.title('United States Sightings')

    # Made the states uppercase and the city names to begin with a capital letter
    us_df['state'] = us_df['state'].str.upper()
    us_df['city'] = us_df['city'].str.title()

    # List of all the states that reported UFO sightings
    states_list = list(us_df['state'])
    states_dict = {}

    # Creates a dictionary that counts the number of UFO sightings each US state had
    for i in states_list:
        states_dict[i] = states_dict.get(i, 0) + 1

    # Sorted the dictionary by state name
    sorted_states_dict = dict(sorted(states_dict.items(), key=lambda item: item[1]))

    state_sightings = list(sorted_states_dict.values())
    states = list(sorted_states_dict.keys())

    # In the US, what states experience the most UFO activity from 1931-2014 (show top 10) maybe ill do it
    # count sightings in US each state
    us_df['year'] = pd.DatetimeIndex(us_df['datetime']).year

    us_years_list = us_df['year']
    us_years_dict = {}

    for i in us_years_list:
        us_years_dict[i] = us_years_dict.get(i, 0) + 1

    sorted_us_years_dict = dict(sorted(us_years_dict.items(), key=lambda item: item[1]))

    year_us = list(sorted_us_years_dict.keys())
    sightings_us = list(sorted_us_years_dict.values())

    max_us_sightings = max(sightings_us)
    max_us_year = max(sorted_us_years_dict, key=sorted_us_years_dict.get)

    # Have user select which year they want to see
    selected_year = st.select_slider('Choose a year to view the number of sightings: ', sorted(year_us))

    # Create two dataframes based off the user's chosen year
    user_year = us_df.loc[(us_df['year'] == selected_year), ['datetime', 'city', 'state']]
    state_loc = us_df.loc[(us_df['year'] == selected_year), ['city', 'state', 'lat', 'lon', 'year']]
    year_sightings = len(user_year)

    # Displays the total number of sightings in that year
    if year_sightings > 0:
        msg = f"In {selected_year}, the United States had a total of {year_sightings} reported sightings!"
        st.success(msg)
    else:
        st.success(f"The United States had no reported sightings in {selected_year}")

    st.title("US Map of Sightings")

    # Icon map displays sightings based off the chosen user year. It will update every time the user chooses a different year
    # Custom icon URL
    ICON_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Circle-icons-ufo.svg/640px-Circle-icons-ufo.svg.png'

    # Format icon
    icon_data = {
        "url": ICON_URL,
        "width": 1000,
        "height": 1000,
        "anchorY": 1000
        }

    # Add icon to dataframe
    state_loc["icon_data"]=None
    for i in state_loc.index:
        state_loc["icon_data"][i] = icon_data

    # Create a layer with custom icon
    icon_layer = pdk.Layer(type="IconLayer",
                           data = state_loc,
                           get_icon="icon_data",
                           get_position='[lon,lat]',
                           get_size=4,
                           size_scale=10,
                           pickable=True)

    # Create a view of the map
    view_state = pdk.ViewState(
        latitude=state_loc["lat"].mean(),
        longitude=state_loc["lon"].mean(),
        zoom=3,
        pitch=0
        )

    # stylish tool tip
    tool_tip = {"html": "City: <b>{city}</b>",
                "style": {"backgroundColor": "black", "color": "white"}}

    us_icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        layers=[icon_layer],
        initial_view_state= view_state,
        tooltip=tool_tip)

    # Display map of US sightings
    st.pydeck_chart(us_icon_map)

    # Show top 10 states with the most sightings of all time
    fig, ax = plt.subplots()
    ax.bar(states[-11:], state_sightings[-11:], color='blue')
    plt.title('Top 10 States')
    plt.xlabel('States')
    plt.ylabel('# of Reported Sightings')

    # Columns: one displays the bar chart, the other displays a quick quiz question to engage the user more
    col1, col2, col3, col4 = st.columns([1, 9, 9, 1])
    with col1:
        st.write("")
    with col2:
        st.pyplot(fig)
    with col3:
        st.subheader('Quick Trivia!')
        options_dict = {'2011': False,
                        '2012': True,
                        '2007': False,
                        '2014': False}
        trivia = stb.multiple_choice('What year had the most reported UFO sightings?',
                                     options_dict=options_dict, success='Good job! 2012 had a total of 606 sightings.',
                                     error='Nope.. Try again!')
    with col4:
        st.write("")

# Third option: Great Britain
elif selected_where == 'Great Britain':

    # Show map of sightings in GB
    st.title('Great Britain Sightings')
    uk_df['year'] = pd.DatetimeIndex(uk_df['datetime']).year
    uk_df['city'] = uk_df['city'].str.title()
    sorted_uk = uk_df.sort_values(by=['duration (seconds)'], ascending=False)
    uk_years_list = list(uk_df['year'])

    # Have user select which year they want to see
    selected_year = st.select_slider('Choose a year to view the number of sightings: ', sorted(uk_years_list))

    # Create two dataframes that are filtered by the selected user year
    user_year = sorted_uk.loc[(sorted_uk['year'] == selected_year), ['datetime', 'city']]
    sighting_loc = sorted_uk.loc[(sorted_uk['year'] == selected_year), ['city', 'lat', 'lon', 'year']]
    year_sightings = len(user_year)

    if year_sightings > 0:
        msg = f"In {selected_year}, Great Britain had a total of {year_sightings} reported sightings!"
        st.success(msg)
    else:
        st.success(f"Great Britain had no reported sightings in {selected_year}")

    # Icon map displays sightings based off the chosen user year. It will update every time the user chooses a different year
    # Create custom icons
    ICON2_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Circle-icons-ufo.svg/640px-Circle-icons-ufo.svg.png'

    # Format icon
    icon2_data = {
        "url": ICON2_URL,
        "width": 100,
        "height": 100,
        "anchorY": 100
        }

    # Add icons to dataframe
    sighting_loc["icon_data"]=None
    for i in sighting_loc.index:
        sighting_loc["icon_data"][i] = icon2_data

    # Create a layer with custom icon
    icon2_layer = pdk.Layer(type="IconLayer",
                            data=sighting_loc,
                            get_icon="icon_data",
                            get_position='[lon,lat]',
                            get_size=4,
                            size_scale=10,
                            pickable=True)

    # Create a view of the map
    view_state2 = pdk.ViewState(
        latitude=sighting_loc["lat"].mean(),
        longitude=sighting_loc["lon"].mean(),
        zoom=5.3,
        pitch=0
        )

    # stylish tool tip
    tool_tip = {"html": "City: <b>{city}</b>",
                "style": {"backgroundColor": "black", "color": "white"}}

    uk_icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        layers=[icon2_layer],
        initial_view_state=view_state2,
        tooltip=tool_tip)

    # Display UK map
    st.pydeck_chart(uk_icon_map)

    # Create a chart for the top 2 longest UFO durations
    with st.expander('Report With Longest Duration: How long was it in comparison to the second longest?'):
        fig4, ax4 = plt.subplots()
        ax4.bar(sorted_uk['city'][:2], sorted_uk['duration (seconds)'][:2], color='red')
        plt.title('Top 2 Longest Reported Sightings')
        plt.xlabel('Cities')
        plt.ylabel('# of Seconds')

        st.write('The longest sighting was reported on April 11, 2013')

        # Column displays a bar chart of the top 2 longest sightings in GB
        col1, col2, col3 = st.columns([1,4,1])
        with col1:
            st.write("")
        with col2:
            st.pyplot(fig4)
        with col3:
            st.write("")

    # Expander includes the victim's account of that day
    with st.expander('What happened on that day?'):
        st.write('Victim testimony: ')
        st.write('"Abduction by government. There were what I believe to be men in alien 3d cloaked costumes that '
                 'looked like grey aliens, outside of my front garden? I had been alerted to them by crackling sounds '
                 'coming from outside my bedroom window. They fitted high powered lights by my fence and raised a concave '
                 'and convex cone shape that was two or three feet across in width and two cables ran to it from the lights. '
                 'They turned the lights on it was burning me through the glass and the cross of sellotape I had on the '
                 'window melted on hard. They then entered my house and I grabbed one of the alien looking feinds around '
                 'the neck it was indeed a suit of sorts because it felt like a normal width for a neck, about seven '
                 'inches-however it looked like the neck was two inches. We struggled around until the thing put its left '
                 'hand to my head I heard a buzz from the device it was holding and I done every action it did to walk '
                 'around and open doors for it. I was missing five days no one knows where I was" ((NUFORC Note: Witness '
                 'indicates that the date of the sighting is approximate.')
        st.write('Full victim account from: https://tinyurl.com/LongestSightingUK')

# Third option: Australia
elif selected_where == 'Australia':
    st.title('Australia Sightings')

    # Create new columns (year and month) to easily extract the information I want to display
    au_df['month'] = pd.DatetimeIndex(au_df['datetime']).month
    au_df['year'] = pd.DatetimeIndex(au_df['datetime']).year
    au_df['month'] = pd.DatetimeIndex(au_df['datetime']).strftime('%B')

    # Capitalizes the first letter of each city
    au_df['city'] = au_df['city'].str.title()

    months_list = list(au_df['month'])
    months_dict = {}

    # Creates a dictionary that counts the reported sightings of each month in the year
    for i in months_list:
        months_dict[i] = months_dict.get(i, 0) + 1

    sorted_months = dict(sorted(months_dict.items(), key=lambda item: item[0]))

    au_years_list = list(au_df['year'])

    # Have user select which year they want to see
    selected_year = st.select_slider('Choose a year to view the number of sightings: ', sorted(au_years_list))

    # Create two dataframes that are filtered by the selected user year
    user_year = au_df.loc[(au_df['year'] == selected_year), ['datetime', 'city']]
    sighting_loc = au_df.loc[(au_df['year'] == selected_year), ['city', 'lat', 'lon', 'year']]
    year_sightings = len(user_year)

    if year_sightings > 0:
        msg = f"In {selected_year}, Australia had a total of {year_sightings} reported sightings!"
        st.success(msg)
    else:
        st.success(f"Australia had no reported sightings in {selected_year}")

    # Icon map displays sightings based off the chosen user year. It will update every time the user chooses a different year
    # Create custom icons
    ICON3_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Circle-icons-ufo.svg/640px-Circle-icons-ufo.svg.png'

    # Format icon
    icon3_data = {
        "url": ICON3_URL,
        "width": 100,
        "height": 100,
        "anchorY": 100
        }

    # Add icons to dataframe
    sighting_loc["icon_data"]=None
    for i in sighting_loc.index:
        sighting_loc["icon_data"][i] = icon3_data

    # Create a layer with custom icon
    icon3_layer = pdk.Layer(type="IconLayer",
                            data=sighting_loc,
                            get_icon="icon_data",
                            get_position='[lon,lat]',
                            get_size=4,
                            size_scale=10,
                            pickable=True)

    # Create a view of the map
    view_state3 = pdk.ViewState(
        latitude=sighting_loc["lat"].mean(),
        longitude=sighting_loc["lon"].mean(),
        zoom=3,
        pitch=0
        )

    # stylish tool tip
    tool_tip = {"html": "City: <b>{city}</b>",
                "style": {"backgroundColor": "black", "color": "white"}}

    au_icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        layers=[icon3_layer],
        initial_view_state=view_state3,
        tooltip=tool_tip)

    # Displays the map
    st.pydeck_chart(au_icon_map)

    # Create pie chart that will show the percentage of sightings of each month
    fig4, ax4 = plt.subplots()
    ax4.pie(sorted_months.values(), labels=sorted_months.keys(), autopct='%.0f%%')
    plt.title('Australia Sightings by Month (%)')

    # Columns: col2 displays the pie char, col3 displays all the June sightings
    col1, col2, col3, col4 = st.columns([1,9, 9, 1])
    with col1:
        st.write("")
    with col2:
        st.pyplot(fig4)
    with col3:
        with st.expander('View all of the reported June sightings'):
            st.write(au_df.loc[(au_df['month'] == 'June'), ['datetime', 'city']])
    with col4:
        st.write("")

# Fourth option: Canada
elif selected_where == 'Canada':
    st.title('Canada Sightings')

    # Adds a new column (year) into the dataframe to easily extract information based off the year
    ca_df['year'] = pd.DatetimeIndex(ca_df['datetime']).year
    ca_df['city'] = ca_df['city'].str.title()

    ca_years_list = list(ca_df['year'])

    # Have user select which year they want to see
    selected_year = st.select_slider('Choose a year to view the number of sightings: ', sorted(ca_years_list))

    # Create two dataframes that are filtered by the selected user year
    user_year = ca_df.loc[(ca_df['year'] == selected_year), ['datetime', 'city']]
    sighting_loc = ca_df.loc[(ca_df['year'] == selected_year), ['city', 'lat', 'lon', 'year']]
    year_sightings = len(user_year)

    if year_sightings > 0:
        msg = f"In {selected_year}, Canada had a total of {year_sightings} reported sightings!"
        st.success(msg)
    else:
        st.success(f"Canada had no reported sightings in {selected_year}")

    # Icon map displays sightings based off the chosen user year. It will update every time the user chooses a different year
    # Create custom icons
    ICON4_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Circle-icons-ufo.svg/640px-Circle-icons-ufo.svg.png'

    # Format icon
    icon4_data = {
        "url": ICON4_URL,
        "width": 100,
        "height": 100,
        "anchorY": 100
        }

    # Add icons to dataframe
    sighting_loc["icon_data"]=None
    for i in sighting_loc.index:
        sighting_loc["icon_data"][i] = icon4_data

    # Create a layer with custom icon
    icon4_layer = pdk.Layer(type="IconLayer",
                            data=sighting_loc,
                            get_icon="icon_data",
                            get_position='[lon,lat]',
                            get_size=4,
                            size_scale=10,
                            pickable=True)

    # Create a view of the map
    view_state4 = pdk.ViewState(
        latitude=sighting_loc["lat"].mean(),
        longitude=sighting_loc["lon"].mean(),
        zoom=2.6,
        pitch=0
        )

    # stylish tool tip
    tool_tip = {"html": "City: <b>{city}</b>",
                "style": {"backgroundColor": "black", "color": "white"}}

    ca_icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        layers=[icon4_layer],
        initial_view_state=view_state4,
        tooltip=tool_tip)

    # Display the map
    st.pydeck_chart(ca_icon_map)

    ca_years_list = list(ca_df['year'])
    ca_years_dict = {}

    # Create a dictionary that keeps count of all the reported sightings each year
    for i in ca_years_list:
        ca_years_dict[i] = ca_years_dict.get(i, 0) + 1

    sorted_ca_years_dict = dict(sorted(ca_years_dict.items(), key=lambda item: item[0]))
    year_ca = list(sorted_ca_years_dict.keys())
    sightings_ca = list(sorted_ca_years_dict.values())

    # Create a bar char that shows the top 5 most active UFO years in Canada
    fig5, ax5 = plt.subplots()
    ax5.bar(year_ca[-5:], sightings_ca[-5:], color='orange')
    plt.title('Last 5 Years of Reported Sightings')
    plt.xlabel('Years')
    plt.ylabel('# of Sightings')

    # Columns: col2 displays the bar chart, col3 displays a quick trivia question to engage the user
    col1, col2, col3, col4 = st.columns([1,10,10, 1])
    with col1:
        st.write("")
    with col2:
        st.pyplot(fig5)
    with col3:
        st.subheader("Quick Trivia!")
        stb.true_or_false('True or False: Canada has reported more UFO sightings than Great Britain.', True,
                          success=f"It's true! Canada has a total of {len(ca_years_list)}, while Great Britain has a "
                                  f"total of {len(uk_df)}")
    with col4:
        st.write('')


# Last section is a quiz section where the user gets asked questions about the information presented in the other sections
elif selected_where == 'Test Your Knowledge':
    st.title('Quiz Time!')
    col1, col2 = st.columns([10,10])
    with col1:
        multiple_choice1 = stb.single_choice('1. What month has the most reported sightings of all time in Australia?',
                      options=["August", "March", "December", "June"], answer_index=3,
                                             success=f"Correct! Of all the months, June was the most active month of "
                                                     f"sightings, with a total of 13 sightings.")

        multiple_choice2 = stb.single_choice('2. Which US state has the most sightings of all time?',
                          options=["Washington", "Massachusetts", "Florida", "California"], answer_index=3,
                                              success='Correct! California has a total 868 reported sightings! Washington'
                                                      ' is the second most active state with 404 reported sightings.')

        multiple_choice3 = stb.single_choice('3. What year was the earliest reported UFO sighting in the data?',
                          options=["1940", "1931", "1937", "1952"], answer_index=1,
                                             success="That's right! The earliest recorded UFO sighting was in 1931 in"
                                                     " Abilene, Kansas.")

        multiple_choice4 = stb.single_choice('4. What year had the highest reported UFO sightings worldwide?',
                          options=["2013", "2012", "2009", "2007"], answer_index=0,
                                             success="Good job! In 2013, there was a total of 710 reported sightings!")

        multiple_choice5 = stb.single_choice('5. Which city in England had the longest reported sighting (duration in seconds)?',
                          options=["London", "Manchester", "Leadgate", "Dunstable"], answer_index=2,
                                             success="Yes! The longest reported sighting lasted over 400,000 seconds in "
                                                     "Leadgate, England. That's a total of 5 days!")
    with col2:
        st.image(r'https://tinyurl.com/AuUfoPic')
        st.write('')
        st.image(r'https://cdn.mos.cms.futurecdn.net/Co84KrcqX4LYGgNa44rnjT.jpg')
        st.write('')
        st.image(r'https://media-cldnry.s-nbcnews.com/image/upload/MSNBC/Components/Video/201909/ufothumb.jpg')

