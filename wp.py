import base64
import streamlit as st
import datetime, requests
from plotly import graph_objects as go
import time

# Advanced page configuration
st.set_page_config(
    page_title='Advanced Atmospheric Prediction System',
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }
    .stSelectbox, .stTextInput {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
    }
    h1 {
        color: white;
        text-shadow: 2px 2px 4px #000000;
        text-align: center;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Keep your existing background image code
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("2473489103.jpg")

page_bg_img = f"""
<style>
.stApp {{
background-image: url('data:image/jpg;base64,{img}');
background-size: cover;
}} 
</style>
"""
           
st.markdown(page_bg_img, unsafe_allow_html=True)



st.title("🌥️🌧️ 7-DAY ATMOSPHERIC SYSTEM 🌧️🌥️")

# Add a loading spinner
with st.spinner("Loading Weather Forecast System..."):
    time.sleep(1)

# Create sidebar for inputs
with st.sidebar:
    st.markdown("## ⚙️ Configure Settings")
    city = st.text_input("🌆 Enter City Name", placeholder="e.g. Gunupur")
    unit = st.selectbox("🌡️ Temperature Unit", ["Celsius", "Fahrenheit"])
    speed = st.selectbox("💨 Wind Speed Unit", ["Metre/sec", "Kilometre/hour"])
    graph = st.radio("📊 Visualization Type", ["Bar Graph", "Line Graph"])

# Add these variables before the button
if unit=="Celsius":
    temp_unit=" °C"
else:
    temp_unit=" °F"
    
if speed=="Kilometre/hour":
    wind_unit=" km/h"
else:
    wind_unit=" m/s"

api="569eef40dd12adf0e06273470488a462"

if st.sidebar.button("🔍 Generate Forecast"):
    with st.spinner('Fetching weather data...'):
        try:
            # First API call to get coordinates
            url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"
            response=requests.get(url)
            x=response.json()  # Now 'x' is defined before being used
            
            # Check if city is valid before proceeding
            if 'coord' not in x:
                st.error("❌ City not found! Please check the spelling and try again.")
                st.stop()  # Stop execution here if city is invalid
            
            lon=x["coord"]["lon"]
            lat=x["coord"]["lat"]
            ex="current,minutely,hourly"
            url2=f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={ex}&appid={api}'
            res=requests.get(url2)
            y=res.json()

            maxtemp=[]
            mintemp=[]
            pres=[]
            humd=[]
            wspeed=[]
            desc=[]
            cloud=[]
            rain=[]
            dates=[]
            sunrise=[]
            sunset=[]
            cel=273.15
            
            for item in y["daily"]:
                
                if unit=="Celsius":
                    maxtemp.append(round(item["temp"]["max"]-cel,2))
                    mintemp.append(round(item["temp"]["min"]-cel,2))
                else:
                    maxtemp.append(round((((item["temp"]["max"]-cel)*1.8)+32),2))
                    mintemp.append(round((((item["temp"]["min"]-cel)*1.8)+32),2))

                if wind_unit=="m/s":
                    wspeed.append(str(round(item["wind_speed"],1))+wind_unit)
                else:
                    wspeed.append(str(round(item["wind_speed"]*3.6,1))+wind_unit)

                pres.append(item["pressure"])
                humd.append(str(item["humidity"])+' %')
                
                cloud.append(str(item["clouds"])+' %')
                rain.append(str(int(item["pop"]*100))+'%')

                desc.append(item["weather"][0]["description"].title())

                d1=datetime.date.fromtimestamp(item["dt"])
                dates.append(d1.strftime('%d %b'))
                
                sunrise.append( datetime.datetime.utcfromtimestamp(item["sunrise"]).strftime('%H:%M'))
                sunset.append( datetime.datetime.utcfromtimestamp(item["sunset"]).strftime('%H:%M'))

            def bargraph():
                fig=go.Figure(data=
                    [
                    go.Bar(name="Maximum",x=dates,y=maxtemp,marker_color='orange'),
                    go.Bar(name="Minimum",x=dates,y=mintemp,marker_color='cyan')
                    ])
                fig.update_layout(xaxis_title="Dates",yaxis_title="Temperature",barmode='group',margin=dict(l=70, r=10, t=80, b=80),font=dict(color="white"))
                st.plotly_chart(fig)
            
            def linegraph():
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=dates, y=mintemp, name='Minimum '))
                fig.add_trace(go.Scatter(x=dates, y=maxtemp, name='Maximimum ',marker_color='orange'))
                fig.update_layout(xaxis_title="Dates",yaxis_title="Temperature",font=dict(color="white"))
                st.plotly_chart(fig)
                
            icon=x["weather"][0]["icon"]
            current_weather=x["weather"][0]["description"].title()
            
            if unit=="Celsius":
                temp=str(round(x["main"]["temp"]-cel,2))
            else:
                temp=str(round((((x["main"]["temp"]-cel)*1.8)+32),2))
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("## Current Temperature ")
            with col2:
                st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png",width=70)
        
            
            col1, col2= st.columns(2)
            col1.metric("TEMPERATURE",temp+temp_unit)
            col2.metric("WEATHER",current_weather)
            st.subheader(" ")
            
            if graph=="Bar Graph":
                bargraph()
                
            elif graph=="Line Graph":
                linegraph()
        
             
            table1=go.Figure(data=[go.Table(header=dict(
                      values = [
                      '<b>DATES</b>',
                      '<b>MAX TEMP<br>(in'+temp_unit+')</b>',
                      '<b>MIN TEMP<br>(in'+temp_unit+')</b>',
                      '<b>CHANCES OF RAIN</b>',
                      '<b>CLOUD COVERAGE</b>',
                      '<b>HUMIDITY</b>'],
                      line_color='black', fill_color='orange',  font=dict(color='white', size=14),height=32),
            cells=dict(values=[dates,maxtemp,mintemp,rain,cloud,humd],
            line_color='black',fill_color=['#DADADA',['#FFFFFF', '#F1F1F1']*7], font_size=14,height=32
                ))])
        
            table1.update_layout(margin=dict(l=10,r=10,b=10,t=10),height=328)
            st.write(table1)
            
            table2=go.Figure(data=[go.Table(columnwidth=[1,2,1,1,1,1],header=dict(values=['<b>DATES</b>','<b>WEATHER CONDITION</b>','<b>WIND SPEED</b>','<b>PRESSURE<br>(in hPa)</b>','<b>SUNRISE<br>(in UTC)</b>','<b>SUNSET<br>(in UTC)</b>']
                      ,line_color='black', fill_color='orange',  font=dict(color='white', size=14),height=36),
            cells=dict(values=[dates,desc,wspeed,pres,sunrise,sunset],
            line_color='black',fill_color=['#DADADA',['#FFFFFF', '#F1F1F1']*7], font_size=14,height=36))])
            
            table2.update_layout(margin=dict(l=10,r=10,b=10,t=10),height=360)
            st.write(table2)
            
            st.header(' ')
            st.header(' ')
     
        except KeyError:
            st.error(" Invalid city!!  Please try again !!")
            
            # Enhanced visualization (move this inside the try block, before any possible errors)
            st.success(f"Successfully retrieved weather data for {city.title()}")
            
            # Weather Overview Section
            st.markdown("### 📊 Weather Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Temperature", f"{temp}{temp_unit}", delta="Now")
            with col2:
                st.metric("Weather", current_weather)
            with col3:
                st.metric("Humidity", f"{x['main']['humidity']}%")

            st.markdown("### 📈 Temperature Trends")
            st.plotly_chart(fig)
            
            # Enhanced tables with better styling
            st.markdown("### 📋 Detailed Forecast")
            st.write(table1)
            st.write(table2)
            
            st.header(' ')
            st.header(' ')
     
        except KeyError:
            st.error("❌ City not found! Please check the spelling and try again.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")

        # Add footer (move outside the try-except block)
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; color: black; background: rgba(0, 0, 0, 0.5); padding: 1rem; border-radius: 10px;'>
                <h4>Advanced Weather Forecast System</h4>
                <p>Powered by OpenWeatherMap</p>
            </div>
        """, unsafe_allow_html=True)