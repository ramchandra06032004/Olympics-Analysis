import pandas as pd
import numpy as np
import plotly.express as px

def medal_Tally(data):
    medals = data.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medals = medals.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold",ascending=False).reset_index()
    medals["Total"] = medals["Gold"] + medals["Silver"] + medals["Bronze"]
    return medals

def country_year_list(data):
    years=data["Year"].unique().tolist()
    years.sort()
    years.insert(0,"Overall")

    country=np.unique(data["region"].dropna().values).tolist()
    country.sort()
    country.insert(0,"Overall")
    return years,country
def fetch_medal_tally(df,country , year):
    medals_df=df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    flag=1
    if country=="Overall" and year=="Overall":
        temp_df=medals_df
    if country!="Overall" and year=="Overall":
        flag=0
        temp_df=medals_df[medals_df["region"]==country]
    if country=="Overall" and year!="Overall":
        temp_df=medals_df[medals_df["Year"]==year]
    if country!="Overall" and year!="Overall":
        temp_df=medals_df[(medals_df["region"]==country) & (medals_df["Year"]==year)]
    if flag==1:
        x=temp_df.groupby("region")[["Gold","Silver","Bronze"]].sum().sort_values("Gold",ascending=False).reset_index()
    else:
        x=temp_df.groupby("Year")[["Gold","Silver","Bronze"]].sum().sort_values("Year",ascending=True).reset_index() 
    x["Total"]=x["Gold"]+x["Silver"]+x["Bronze"]
    return(x)

def participating_nations(data):
    country_count = data.drop_duplicates(["Year","region"])["Year"].value_counts().reset_index().sort_values("Year")
    country_count.rename(columns={"count":"Country"},inplace=True)
    return country_count
def no_of_events(data):
    events_tally=data.drop_duplicates(["Year","Event"])["Year"].value_counts().reset_index().sort_values("Year")
    events_tally.rename(columns={"count":"No Of Events"},inplace=True)
    return events_tally

def no_of_athlite(data):
    athlete_tally=data.drop_duplicates(["Year","Name"])["Year"].value_counts().reset_index().sort_values("Year")
    athlete_tally.rename(columns={"count":"No Of Athlete"},inplace=True)
    return athlete_tally

def number_of_events(data):
    x=data.drop_duplicates(["Year","Sport","Event"])
    x=x.pivot_table(index="Sport",columns="Year",values="Event",aggfunc="count").fillna(0).astype("int")
    return x

def most_succesful_athlete(df,game):
    temp_df=df.dropna(subset=["Medal"])
    if game!="Overall":
        temp_df=temp_df[temp_df["Sport"]==game]

    x=temp_df["Name"].value_counts().reset_index().head(15).merge(df,left_on="Name",right_on="Name",how="left").drop_duplicates("Name")[["Name","Sport","region","count"]]
    x.rename(columns={"region":"Country","count":"No Of Medals"},inplace=True)
    return x

def medal_tally_year_wise(df,country):
    temp_df=df.dropna(subset=["Medal"])
    temp_df=df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    temp_df=temp_df[(temp_df["region"]==country)]
    temp_df=temp_df.groupby("Year")["Medal"].count().reset_index()
    return temp_df
def country_good_at_sport(df,country):
    temp_df=df.dropna(subset=["Medal"])
    temp_df=df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    temp_df=temp_df[(temp_df["region"]==country)]
    pTable=temp_df.pivot_table(index="Sport",columns="Year",values="Medal",aggfunc="count").fillna(0).astype("int")
    return pTable

def most_succesful_athlete_byCountry(df,country):
    temp_df=df.dropna(subset=["Medal"])
    temp_df=temp_df[temp_df["region"]==country]
    x=temp_df["Name"].value_counts().reset_index().head(15).merge(df,left_on="Name",right_on="Name",how="left").drop_duplicates("Name")[["Name","Sport","region","count"]]
    x.rename(columns={"region":"Country","count":"No Of Medals"},inplace=True)
    return x

def age_wise_athelete_anlysis(data):
    athlete_data=data.drop_duplicates(subset=["Name","region"])
    x1=athlete_data[athlete_data["Medal"]=="Gold"]["Age"].dropna()
    x2=athlete_data[athlete_data["Medal"]=="Silver"]["Age"].dropna()
    x3=athlete_data[athlete_data["Medal"]=="Bronze"]["Age"].dropna()
    x4=athlete_data["Age"].dropna()

    return x1,x2,x3,x4  

def men_women_count(data):
    data=data.drop_duplicates(subset=["Name","region"])
    men=data[data["Sex"]=="M"]
    men=men.groupby("Year")["Name"].count().reset_index()
    men.rename(columns={"Name":"count"},inplace=True)
    women=data[data["Sex"]=="F"]
    women=women.groupby("Year")["Name"].count().reset_index()
    women.rename(columns={"Name":"count"},inplace=True)
    return men ,women