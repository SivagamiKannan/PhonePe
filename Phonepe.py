import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json


#Database connection creation
import pandas as pd
import plotly.express as px
import mysql.connector
connection=mysql.connector.connect(       
    host='localhost',
    user='root',
    password='12345678',
    database='PhonePE_Project')
cursor=connection.cursor()

#Aggregate Transaction

cursor.execute("Select * from aggregated_transaction")
table1=cursor.fetchall()
Aggregate_Trans=pd.DataFrame(table1,columns=("State","Year","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#Aggregate Users
cursor.execute("Select * from aggregated_users")
table2=cursor.fetchall()
Aggregate_Users=pd.DataFrame(table2,columns=("State","Year","Quarter","Brands","Transaction_count","Percentage"))

#Map Transaction
cursor.execute("Select * from map_transaction")
table3=cursor.fetchall()
Map_Trans=pd.DataFrame(table3,columns=("State","Year","Quarter","Districts","Transaction_count","Transaction_amount"))

#Map Users
cursor.execute("Select * from map_users")
table4=cursor.fetchall()
Map_Users=pd.DataFrame(table4,columns=("State","Year","Quarter","Districts","RegisteredUsers","AppOpens"))

#Top Trans
cursor.execute("Select * from top_transaction")
table5=cursor.fetchall()
Top_Trans=pd.DataFrame(table5,columns=("State","Year","Quarter","Pincode","Transaction_count","Transaction_amount"))

#Top Users
cursor.execute("Select * from top_users")
table6=cursor.fetchall()
Top_Users=pd.DataFrame(table6,columns=("State","Year","Quarter","Pincode","RegisteredUsers_count"))


#function part

def trans_amount_count_year(df,Year):
    tacy=df[df["Year"]== Year]
    tacy.reset_index(drop=True,inplace=True)
    
    tacyg=tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    col3,col4=st.columns(2)

    with col1:
    
        plot1=px.bar(tacyg,x="State",y="Transaction_amount",color_discrete_sequence= px.colors.sequential.Inferno,
                     title=f"Transaction Amount Plot of {Year}",height=500,width=600)
        st.plotly_chart(plot1)
    with col2:        
        plot2=px.bar(tacyg,x="State",y="Transaction_count",color_discrete_sequence= px.colors.sequential.Cividis,
                         title=f"Transaction Count Plot of {Year}",height=500,width=600)
        st.plotly_chart(plot2)
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1=json.loads(response.content)
    states_list=[]
    for feature in data1["features"]:
        states_list.append(feature["properties"]["ST_NM"])
    states_list.sort()

    with col3:
        India_map1=px.choropleth(tacyg, geojson=data1,locations="State",featureidkey="properties.ST_NM",
                                 color="Transaction_amount",color_continuous_scale="icefire",range_color=    (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),hover_name="State",
                                 title=f"{Year} Transaction Amount",fitbounds="locations",height=650,width=600)
        India_map1.update_geos(visible=False)
        st.plotly_chart(India_map1)
    with col4:
        India_map2=px.choropleth(tacyg, geojson=data1,locations="State",featureidkey="properties.ST_NM",
                                 color="Transaction_count",color_continuous_scale="sunset",range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),hover_name="State",
                                 title=f"{Year} Transaction Count",fitbounds="locations",height=650,width=600)
        India_map2.update_geos(visible=False)
        st.plotly_chart(India_map2)
        
def Qtrans_type(df,state):
    tacy=df[df["State"]== state]
    tacy.reset_index(drop=True, inplace=True)
    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        pie_plot1=px.pie(data_frame=tacyg, names="Transaction_type",values="Transaction_amount",width=600,title=f"{state.upper()} Transaction Amount",hole=0.5)
        st.plotly_chart(pie_plot1)
    with col2:
        pie_plot2=px.pie(data_frame=tacyg, names="Transaction_type",values="Transaction_count",width=600,title=f"{state.upper()} Transaction Count",hole=0.5)
        st.plotly_chart(pie_plot2)


def Qdistricts_type(df,state):
    tacy=df[df["State"]== state]
    tacy.reset_index(drop=True, inplace=True)
    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        pie_plot1=px.bar(tacyg,x="Districts",y="Transaction_amount",color_discrete_sequence=px.colors.sequential.algae_r,height=550,width=500,title=f"{state.upper()} Transaction Amount")
        st.plotly_chart(pie_plot1)
    with col2:
        pie_plot2=px.bar(tacyg,x="Districts",y="Transaction_count",height=550,width=500,title=f"{state.upper()} Transaction Count")
        st.plotly_chart(pie_plot2)
def pincode_type(df,state):
    tacy=df[df["State"]== state]
    tacy.reset_index(drop=True, inplace=True)
    tacyg=tacy.groupby("Pincode")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        pie_plot1=px.bar(tacy,y="Transaction_amount",x="Quarter",hover_data="Pincode",title=f"{state.upper()} Transaction Amount")
        st.plotly_chart(pie_plot1)
    with col2:
        pie_plot2=px.bar(tacy,y="Transaction_count",x="Quarter",hover_data="Pincode",title=f"{state.upper()} Transaction Count")
        st.plotly_chart(pie_plot2)

#Aggregated User Analysis
def aggre_user_plot1(df,year):
    aguy=df[df["Year"]==year]
    aguy.reset_index(drop=True,inplace=True)
    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)
    plot1=px.bar(aguyg,x="Brands",y="Transaction_count",title="BRANDS AND TRANSACTION COUNT",
                width=700,height=650,color_discrete_sequence=px.colors.sequential.amp_r)
    st.plotly_chart(plot1)

def aggre_user_plot2(df,quarter):
    aguy=df[df["Quarter"]==quarter]
    aguy.reset_index(drop=True,inplace=True)
    aguyg=pd.DataFrame(aguy.groupby("Brands")[["Transaction_count","Percentage"]].sum())
    aguyg.reset_index(inplace=True)
    plot2=px.bar(aguyg,x="Brands",y="Transaction_count",title= f" Q{quarter} BRANDS AND TRANSACTION COUNT",
                width=700,height=650,hover_data="Percentage",color_discrete_sequence=px.colors.sequential.algae_r)
    st.plotly_chart(plot2)

#map user
def map_users_plot1(df,year):
    muy=df[df["Year"]==year]
    muy.reset_index(drop=True,inplace=True)
    muyg=pd.DataFrame(muy.groupby("State")[["RegisteredUsers","AppOpens"]].sum())
    muyg.reset_index(inplace=True)
    plot1=px.line(muyg,x="State",y=["RegisteredUsers","AppOpens"],title=f"{year} REGISTERED USERS, APPOPENS",width=1000,height=800,markers=True)
    st.plotly_chart(plot1)

def map_users_plot2(df,quarter):
    muy=df[df["Quarter"]==quarter]
    muy.reset_index(drop=True,inplace=True)
    muyg=pd.DataFrame(muy.groupby("State")[["RegisteredUsers","AppOpens"]].sum())
    muyg.reset_index(inplace=True)
    plot2=px.line(muyg,x="State",y=["RegisteredUsers","AppOpens"],title=f"Q{quarter} REGISTERED USERS, APPOPENS",width=1000,height=800,markers=True,
                     color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(plot2)

#top user functions
def top_user_plot1(df,year):
    tuyr=df[df["Year"]==year]
    tuyr.reset_index(drop=True,inplace=True)
    tuyrg=pd.DataFrame(tuyr.groupby(['State','Quarter'])['RegisteredUsers_count'].sum())
    tuyrg.reset_index(inplace=True)
    top_plot1=px.bar(tuyrg,x="State",y="RegisteredUsers_count",color="Quarter",width=1000,height=800,
                    color_discrete_sequence=px.colors.sequential.Burgyl,
                    title=f"{year} REGISTERED USERS")
    st.plotly_chart(top_plot1)
def top_user_plot2(df,state):
    tuys=df[df["State"]==state]
    tuys.reset_index(drop=True,inplace=True)
    top_plot2=px.bar(tuys,x="Quarter",y="RegisteredUsers_count",color="RegisteredUsers_count",width=600,height=650,
                    color_continuous_scale=px.colors.sequential.Magenta,hover_data="Pincode",
                    title=f"{state} PINCODE WISE REGISTERED USERS")
    st.plotly_chart(top_plot2)

#dataframe to filter year
def yearfn(df,year):
    tacy=df[df['Year']==year]
    return tacy  
    
#dataframe to filter quarter
def quarterfn(df,quarter):
    tacyq=df[df['Quarter']==quarter]
    return tacyq

# SQL Query function
def Transaction_AC(table_name):
    connection=mysql.connector.connect(       
    host='localhost',
    user='root',
    password='12345678',
    database='PhonePE_Project')
    cursor=connection.cursor()
    query1= f'''Select State, SUM(Transaction_amount) as Transaction_Amount
                FROM {table_name}
                GROUP BY State
                ORDER BY Transaction_Amount DESC
                LIMIT 10;'''
    cursor.execute(query1)
    d=cursor.fetchall()
    df1=pd.DataFrame(d,columns=("State","Transaction Amount"))
    st.write(df1)
    plot1=px.bar(df1,x="State",y="Transaction Amount",color_discrete_sequence= px.colors.sequential.algae_r,title=f"State VS Transaction Amount")
    st.plotly_chart(plot1)
    query2= f'''Select State, SUM(Transaction_count) as Transaction_Count
                FROM {table_name}
                GROUP BY State
                ORDER BY Transaction_Count DESC
                LIMIT 10;'''
    cursor.execute(query2)
    d=cursor.fetchall()
    df2=pd.DataFrame(d,columns=("State","Transaction Count"))
    st.write(df2)
    plot2=px.bar(df2,x="State",y="Transaction Count",color_discrete_sequence= px.colors.sequential.algae_r,title=f"State VS Transaction Count")
    st.plotly_chart(plot2)

def Registered_Users(table_name,State):
    query4=f'''Select Districts,SUM(RegisteredUsers) as Registered_Users
                FROM {table_name}
                WHERE State='{State}'
                GROUP BY Districts
                ORDER BY Registered_Users;'''
    cursor.execute(query4)
    d=cursor.fetchall()
    df4=pd.DataFrame(d,columns=("District","Registered_Users"))
    st.write(df4)
    plot4=px.bar(df4,x="District",y="Registered_Users",color_discrete_sequence= px.colors.sequential.Aggrnyl_r,title=f"District VS Registered_Users Count")
    st.plotly_chart(plot4)
    
def Brands(table_name,year):
    query7=f'''SELECT Brands, SUM(Transaction_count) as Transaction_Count 
          FROM {table_name}
          WHERE Year = {year}
          GROUP BY Brands
          ORDER BY Transaction_Count DESC;'''
    cursor.execute(query7)
    d=cursor.fetchall()
    df7=pd.DataFrame(d,columns=('Brands','Transaction_Count'))
    st.write(df7)
    plot6=px.bar(df7, x="Brands",y="Transaction_Count",title=f"Brands VS Transaction_Count in the {year}",color_discrete_sequence= px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(plot6)



#streamlit part

st.set_page_config(layout="wide")
st.title("Phonepe Pulse Data Visualization and Exploration")

with st.sidebar:
    select=option_menu("Main Menu",["HOME","DATA VISUALIZATION","DATA ANALYSIS"])
if select=="HOME":
    st.subheader("Key Takeaways")
    st.write("1. Extraction of Data From PhonePe Pulse Git Hub")
    st.write("2. Transformation of Data using Python")
    st.write("3. Insertion of Data using MYSQL")
    st.write("4. Visualization of Data using Plotly in Streamlit")
    st.write("5. Analaysis and Graphical Representation of Data using SQL Queries in Streamlit")
elif select=="DATA VISUALIZATION":
   tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
   with tab1:
       method1= st.radio("Select a method",["Aggregate Transaction Analysis","Aggregate User Analysis"])
       st.subheader("Yearly Analysis")
       if method1=="Aggregate Transaction Analysis":
           years=st.radio("Select a year for aggregated transaction",Aggregate_Trans["Year"].unique())
           trans_amount_count_year(Aggregate_Trans,years)
           st.subheader("Quarter Wise Analysis")
           state=st.selectbox("Select a state",Aggregate_Trans['State'].unique())
           quarter=st.radio("Select a quarter",Aggregate_Trans["Quarter"].unique())
           Qtrans_type(quarterfn(yearfn(Aggregate_Trans,years),quarter),state)

       
       elif method1=="Aggregate User Analysis":
            year=st.radio("Select a year for aggregated user",Aggregate_Users["Year"].unique())
            aggre_user_plot1(Aggregate_Users,year)
            quarter=st.radio("Select a quarter for aggregated user",Aggregate_Users["Quarter"].unique())
            aggre_user_plot2(yearfn(Aggregate_Users,year),quarter)
           
   with tab2:
       method2= st.radio("Select a method",["Map Transaction Analysis","Map User Analysis"])
       if method2=="Map Transaction Analysis":
           years=st.radio("Select a year for map transaction",Map_Trans["Year"].unique())
           trans_amount_count_year(Map_Trans,years)
           st.subheader("Quarter Wise Analysis")
           state=st.selectbox("Select a state for map",Map_Trans["State"].unique())
           quarter=st.radio("Select a quarter for map",Map_Trans["Quarter"].unique())
           Qdistricts_type(quarterfn(yearfn(Map_Trans,years),quarter),state)
           
       else:
           year=st.radio("Select a year for map user",Map_Users["Year"].unique())
           map_users_plot1(Map_Users,year)
           quarter=st.radio("Select a quarter for map user",Map_Users["Quarter"].unique())
           map_users_plot2(yearfn(Map_Users,year),quarter)
         
           
           
   with tab3:
       method3= st.radio("Select a method",["Top Transaction Analysis","Top User Analysis"])
       if method3=="Top Transaction Analysis":
           years=st.radio("Select a year for top transaction",Top_Trans["Year"].unique())
           trans_amount_count_year(Top_Trans,years)
           st.subheader("Quarter Wise Analysis")
           state=st.selectbox("Select a state for top",Top_Trans["State"].unique())
           pincode_type(yearfn(Top_Trans,years),state)
           
       else:
              years=st.radio("Select a year for top users",Top_Users["Year"].unique())
              top_user_plot1(Top_Users,years)
              state=st.selectbox("Select a state for top users",Top_Users["State"].unique())
              top_user_plot2(yearfn(Top_Users,years),state)
              
           
  
elif select=="DATA ANALYSIS":
    Question=st.selectbox("Select the Question",["1. List Top 10 Aggregated Transaction Amount and Count State Wise",
           "2. List Top 10 Map Transaction Amount and Count State Wise",
           "3. List Top 10 Top Transaction Amount and Count State Wise",
           "4. Average Transaction Count of Aggregated Users",
           "5. List the Registered Map Users State wise",
           "6. App Opens of Map Users for Top 20 States",
           "7. Quater-Wise Registered Users in the year of 2023 for TOP users",
           "8. Transaction Count for Brands in a year",
           "9. Registered User Count for Top User based on pincode for the state Maharashtra",
           "10. Aggregate Transaction Count and Amount based on Transaction Type",])
    
    if(Question=="1. List Top 10 Aggregated Transaction Amount and Count State Wise"):
        Transaction_AC("aggregated_transaction")
    elif(Question=="2. List Top 10 Map Transaction Amount and Count State Wise"):
        Transaction_AC("map_transaction")
    elif(Question=="3. List Top 10 Top Transaction Amount and Count State Wise"):
        Transaction_AC("top_transaction")
    elif(Question=="4. Average Transaction Count of Aggregated Users"):
        query3=f'''Select State, AVG(Transaction_count) as Transaction_Count 
        FROM aggregated_users 
        GROUP BY  State;'''
        cursor.execute(query3)
        d=cursor.fetchall()
        df3=pd.DataFrame(d,columns=("State","Transaction_Count"))
        st.write(df3)
        plot3=px.bar(df3,x="State",y="Transaction_Count",color_discrete_sequence= px.colors.sequential.Bluered,title=f"State VS Average Transaction Count Plot")
        st.plotly_chart(plot3)
    elif(Question=="5. List the Registered Map Users State wise"):
        State=st.selectbox('Select the State',Map_Users["State"].unique())
        Registered_Users("map_users",State)
    elif(Question=="6. App Opens of Map Users for Top 20 States"):
            query5=f'''Select State, SUM(AppOpens) as AppOpens 
            FROM map_users
            GROUP BY State
            ORDER BY State DESC
            LIMIT 20;'''
            cursor.execute(query5)
            d=cursor.fetchall()
            df5=pd.DataFrame(d,columns=("State","AppOpens"))
            st.write(df5)
            plot5=px.scatter(df5,x="State",y="AppOpens",color_discrete_sequence= px.colors.sequential.algae_r,title=f"State VS App Opens")
            st.plotly_chart(plot5)
    elif(Question=="7. Quater-Wise Registered Users in the year of 2023 for TOP users"):
        query6=f''' SELECT Quarter, SUM(RegisteredUsers_count) as Registered_Users FROM top_users WHERE year=2023
                  GROUP BY Quarter ORDER BY Registered_Users LIMIT 15;'''
        cursor.execute(query6)
        d=cursor.fetchall()
        df6=pd.DataFrame(d,columns=("Quarter","Registered_Users"))
        st.write(df6)
        plot6=px.line(df6, x="Quarter",y="Registered_Users",title=f"Registered_Users VS Quarter",color_discrete_sequence= px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(plot6)
    elif(Question=="8. Transaction Count for Brands in a year"):
        year= st.selectbox("Select the year",Aggregate_Users['Year'].unique())
        Brands("aggregated_users",year)
    elif(Question=="9. Registered User Count for Top User based on pincode for the state Maharashtra"):
        query8=f'''SELECT Pincode, SUM(RegisteredUsers_count) as RegisteredUsers_Count 
              FROM top_users
              WHERE State = 'Maharashtra'
              GROUP BY Pincode
              ORDER BY RegisteredUsers_Count;'''
        cursor.execute(query8)
        d=cursor.fetchall()
        df8=pd.DataFrame(d,columns=("Pincode","RegisteredUsers_Count"))
        st.write(df8)
        plot8=px.scatter(df8, x="Pincode",y="RegisteredUsers_Count",title=f"Maharashtra pincode wise Registered Users Count",color_discrete_sequence= px.colors.sequential.Agsunset,height=650,width=600,symbol="Pincode")
        st.plotly_chart(plot8)
    else:
        query9=f'''Select Transaction_type,SUM(Transaction_count) as Transaction_Count,SUM(Transaction_amount) as Transaction_Amount
                   FROM aggregated_transaction
                   GROUP BY Transaction_type
                   ORDER BY Transaction_Count,Transaction_Amount;'''
        cursor.execute(query9)
        d=cursor.fetchall()
        df9=pd.DataFrame(d,columns=("Transaction_type","Transaction_Count","Transaction_Amount"))
        st.write(df9)
        col1,col2=st.columns(2)
        with col1:
            plot1=px.pie(data_frame=df9, names="Transaction_type",values="Transaction_Amount",width=600,title="Transaction_type vs Transaction_Amount",hole=0.5)
            st.plotly_chart(plot1)
        with col2:
            plot2=px.pie(data_frame=df9, names="Transaction_type",values="Transaction_Count",width=600,title=f"Transaction_type vs Transaction_Count",hole=0.5)
            st.plotly_chart(plot2)
        
        
    
            
    
