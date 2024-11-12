import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from fpdf import FPDF

games=pd.read_csv("vgsales.csv")
filtered_games = games
name = st.sidebar.text_input("Name")
name = name.lower() if name else ""

platform = st.sidebar.text_input("Platform")
platform = platform.lower() if platform else ""

year = st.sidebar.text_input("Year")

genre = st.sidebar.text_input("Genre")
genre = genre.lower() if genre else ""

publisher = st.sidebar.text_input("Publisher")
publisher = publisher.lower() if publisher else ""

if st.sidebar.button("Filter"):

    if name:
        filtered_games = filtered_games[filtered_games["Name"].str.lower() == name]

    if platform:
        filtered_games = filtered_games[filtered_games["Platform"].str.lower() == platform]

    if year:
        filtered_games = filtered_games[filtered_games["Year"] == int(year)]

    if genre:
        filtered_games = filtered_games[filtered_games["Genre"].str.lower() == genre]

    if publisher:
        filtered_games = filtered_games[filtered_games["Publisher"].str.lower() == publisher]

    st.write(filtered_games)

sales_by_year = games.groupby("Year")["Global_Sales"].sum()
st.write("Yıllara Göre Global Satış Trendleri")
st.line_chart(sales_by_year)

total_games = games.shape[0]
top_10_global = games.nlargest(10, 'Global_Sales')

st.write("Global Satışta Top 10 Oyun")
st.write(top_10_global[['Name','Global_Sales']])
st.write(f"Toplam Oyun Sayısı: {total_games}")

if st.sidebar.button("Download Report"):
    if not filtered_games.empty:
        
        filtered_games.to_excel("Filtered_Games_Report.xlsx", index=False)
        with open("Filtered_Games_Report.xlsx", "rb") as file:
            st.sidebar.download_button("Download Excel", file, file_name="Filtered_Games_Report.xlsx")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", size=12)
        pdf.cell(200, 10, txt="Satış Raporu", ln=True, align="C")
        pdf.cell(200, 10, txt="Yıllara Göre Global Satış Trendleri", ln=True, align="C")

        plt.figure()
        plt.plot(sales_by_year.index, sales_by_year.values)
        plt.xlabel("Yıl")
        plt.ylabel("Global Satış (Milyon)")
        plt.savefig("sales_trend.png")
        pdf.image("sales_trend.png", x=10, y=30, w=180)

        pdf.output("Sales_Report.pdf")
        with open("Sales_Report.pdf", "rb") as file:
            st.sidebar.download_button("Download PDF", file, file_name="Sales_Report.pdf")
    else:
        st.sidebar.write("Filtrelenmiş veri mevcut değil.")
