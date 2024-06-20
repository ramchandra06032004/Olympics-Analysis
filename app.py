import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import preProcessing,helper
import plotly.figure_factory as ff

data = pd.read_csv('athlete_events.csv')
region = pd.read_csv('noc_regions.csv')
data=preProcessing.preprocess(data,region)
st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio(
    'Select an option',
    ("Medal Tally","Overall Analysis","Country-Wise Analysis","Athlete-Wise Analysis")
)


if user_menu=="Medal Tally":
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(data)
    selected_year=st.sidebar.selectbox("Select year",years)
    selected_country=st.sidebar.selectbox("Select country",country)
    medal_tally=helper.fetch_medal_tally(data,selected_country,selected_year)
    if selected_country=="Overall" and selected_year=="Overall":
        st.title("Overall Medal Tally")
    if selected_country!="Overall" and selected_year=="Overall":
        st.title("Medal Tally for "+selected_country)
    if selected_country=="Overall" and selected_year!="Overall":
        st.title("Medal Tally for "+str(selected_year)+" Olympics")
    if selected_country!="Overall" and selected_year!="Overall":
        st.title("Medal Tally for "+selected_country+" in "+str(selected_year)+" Olympics")
    st.table(medal_tally)

if user_menu=="Overall Analysis":
    st.title("Overall Analysis of Olympics")
    editions=data["Year"].unique().shape[0]-1
    cities=data["City"].unique().shape[0]
    sports=data["Sport"].unique().shape[0]
    athletes=data["Name"].unique().shape[0]
    countries=data["region"].unique().shape[0]
    events=data["Event"].unique().shape[0]

    col1,col2,col3=st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Athletes")
        st.title(athletes)
    with col2:
        st.header("Countries")
        st.title(countries)
    with col3:
        st.header("Events")
        st.title(events)
    nations_over_time=helper.participating_nations(data)
    fig=px.line(nations_over_time,x="Year",y="Country",title="Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time=helper.no_of_events(data)
    fig1=px.line(events_over_time,x="Year",y="No Of Events",title="Number of events over the years")
    st.plotly_chart(fig1)

    athletes_over_time=helper.no_of_athlite(data)
    fig2=px.line(athletes_over_time,x="Year",y="No Of Athlete",title="Number of Athlete over the years")
    st.plotly_chart(fig2)

    st.title("No of events over time")
    events_over_time=helper.number_of_events(data)
    fig,ax=plt.subplots(figsize=(20,20))
    ax.set_facecolor('black')
    
    ax=sns.heatmap(events_over_time,annot=True)
    st.pyplot(fig)

    st.title("Most succesful Athlete")
    sport_list=data["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")
    sport=st.selectbox("Select a Sport",sport_list)
    x=helper.most_succesful_athlete(data,sport)
    st.table(x)

if user_menu=="Country-Wise Analysis":
    st.title("Country-wise Analysis")
    year,country=helper.country_year_list(data)
    
    # Remove the first item from the list
    country.pop(0)
    
    st.sidebar.title("Year-wise Medal tally of every country")
    selected_country=st.sidebar.selectbox("Select a country",country)
    y=helper.medal_tally_year_wise(data,selected_country)
    fig=px.line(y,x="Year",y="Medal",title="Medals Tally")
    st.plotly_chart(fig)

    st.title("Country and No of Medals in all year Heatmap")
    x=helper.country_good_at_sport(data,selected_country)
    fig,ax=plt.subplots(figsize=(20,20))
    
    ax=sns.heatmap(x,annot=True)
    st.pyplot(fig)

    st.title("Successful Player of "+selected_country)
    z=helper.most_succesful_athlete_byCountry(data,selected_country)
    st.table(z)

if user_menu=="Athlete-Wise Analysis":
    x1,x2,x3,x4=helper.age_wise_athelete_anlysis(data)
    fig=ff.create_distplot([x4,x1,x2,x3],["All Medal Age distrubution","Gold medal age Distrubution ","Silver Medal age distrubution","Bronze Medal age distrubution"],show_hist=False,show_rug=False)
    st.title("Age Distribution")
    st.plotly_chart(fig)
    
    st.title("Height vs Weight distribution of Athlete with Medal")
    games=data["Sport"].unique().tolist()
    games.sort()
    sp=st.selectbox("Select a game",games)
    age_height_data=data[data["Sport"]==sp]
    age_height_data["Medal"].fillna("No Medal",inplace=True)
    fig,ax=plt.subplots(figsize=(10,5))
    ax=sns.scatterplot(x=age_height_data["Height"],y=age_height_data["Weight"],hue=age_height_data["Medal"],style=age_height_data["Sex"])
    st.pyplot(fig)

    st.title("Men Women Participation over the years")
    men,women=helper.men_women_count(data)
    final=men.merge(women,on="Year",how="left")
    final.rename(columns={"count_x":"Male","count_y":"Female"},inplace=True)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)

st.markdown("""
    <style>
    .reportview-container .main .block-container {
        max-width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: white;
        text-align: center;
    }
    </style>
    <div class="footer">
    <p>Copyright © 2024 Ramchandra Mulik. All rights reserved.</p>
    </div>
    """
st.markdown(footer, unsafe_allow_html=True)
    
