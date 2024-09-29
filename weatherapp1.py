import streamlit as st
import requests
import json
import os

# Load environment variables from .env file
from dotenv import load_dotenv

from streamlit_tags import st_tags

load_dotenv()

st.set_page_config(page_title="The Amazing Weather Checker", layout="wide")

st.title("The Amazing Weather Checker!")
st.subheader("Secured with Auth0")

# Auth0 Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_IDENTIFIER = os.getenv("API_IDENTIFIER")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


# Function to get Auth0 token
def get_token(auth_code):
    token_url = f'https://{AUTH0_DOMAIN}/oauth/token'
    headers = {'content-type': 'application/json'}
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8501'
    }
    response = requests.post(token_url, json=payload, headers=headers)
    return response.json()


# Function to get user info
def get_user_info(token):
    userinfo_url = f'https://{AUTH0_DOMAIN}/userinfo'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(userinfo_url, headers=headers)
    return response.json()


authenticated = False
if (st.query_params):
    authenticated = True

# Login Button
st.markdown(
    f'<a href="https://{AUTH0_DOMAIN}/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=http://localhost:8501&scope=openid profile email">Login with Auth0</a>',
    unsafe_allow_html=True)

# print("Auth0 Domain:", os.getenv("AUTH0_DOMAIN"))
# print("Auth0 Client ID:", os.getenv("CLIENT_ID"))
# print("Auth0 Client Secret:", os.getenv("CLIENT_SECRET"))

# agree = st.checkbox("Athenticate?")

# if agree:
# authenticated = True

# Display content if user is authenticated
if authenticated:

    def get_weather_data(city, api_key):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        return data


    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "San Francisco", "Columbus", "Fort Worth", "Indianapolis", "Charlotte", "Seattle", "Denver", "El Paso", "Washington D.C.", "Boston", "Nashville", "Baltimore", "Oklahoma City", "Portland", "Las Vegas", "Louisville", "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Long Beach", "Kansas City", "Mesa", "Virginia Beach", "Atlanta", "Colorado Springs", "Omaha", "Raleigh", "Miami", "Cleveland", "Tulsa", "Oakland", "Minneapolis", "Wichita", "New Orleans", "Arlington", "Bakersfield", "Tampa", "Honolulu", "Anaheim", "Santa Ana", "St. Louis", "Pittsburgh", "Corpus Christi", "Riverside", "Cincinnati", "Lexington", "Anchorage", "Stockton", "Baton Rouge", "Toledo", "Greensboro", "Newark", "Chula Vista", "Buffalo", "Fort Wayne", "Jersey City", "Chandler", "St. Petersburg", "Laredo", "Norfolk", "Madison", "Durham", "Lubbock", "Irvine", "Winston-Salem", "Glendale", "Garland", "Hialeah", "Reno", "Chattanooga", "Scottsdale", "Baton Rouge", "Richmond", "Boise", "Des Moines", "Spokane", "San Bernardino", "Modesto", "Fontana", "Santa Clarita", "Oxnard", "Moreno Valley", "Fayetteville", "Vancouver", "Huntington Beach", "Salt Lake City", "Grand Rapids", "Tallahassee", "Overland Park", "Knoxville", "Port St. Lucie", "Worcester", "Brownsville", "Newport News", "Santa Rosa", "Sioux Falls", "Chesapeake", "Springfield", "Salinas", "Pensacola", "Eugene", "Torrance", "Pasadena", "Fort Collins", "Cary", "Jackson", "Lakewood", "Hollywood", "Tampa", "Augusta", "Amarillo", "Columbia", "Mobile", "Grand Prairie", "Aurora", "Costa Mesa", "Oceanside", "Salt Lake City", "Rancho Cucamonga", "Tempe", "Ontario", "Cape Coral", "Vancouver", "Gainesville", "Chattanooga", "Augusta", "Evansville", "Sandy Springs", "McKinney", "Pearland", "Jacksonville", "Tampa", "Kansas City", "Burbank", "West Palm Beach", "Waterbury", "Westminster", "Cleveland", "Provo"]

    city = st_tags(label='Enter city name', text='Press enter to add more', value=[], suggestions=cities, maxtags = 1)

    if city:
        api_key = "e9e68bcd6e1dd9c3614a4d6835a1eb8e"
        data = get_weather_data(city, api_key)
        if data["cod"] != "404":
            # st.write(data)
            st.write(f"Weather in {city[0]}:")
            st.write(f"Temperature: {data['main']['temp']}°C")
            st.write(f"Humidity: {data['main']['humidity']}%")
            st.write(f"Wind speed: {data['wind']['speed']} m/s")
            st.write(f"Description: {data['weather'][0]['description']}")
        else:
            st.write("City not found")

    st.markdown(
        "[Bored? Click Here!](https://play.unity.com/en/games/6b452830-c19a-4758-a4b6-dfc1db46ab4b/webgl-builds)")

