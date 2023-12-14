import requests
from bs4 import BeautifulSoup
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    # Step 1: Scrape data from the website
    soup = scrape_covid_data()

    # Step 2: Extract and analyze the data
    if soup:
        total_cases, deaths, recovered = get_covid_statistics(soup)

        # Step 3: Visualize the data
        visualize_covid_statistics(total_cases, deaths, recovered)

    return render_template('index.html')


def scrape_covid_data():
    url = "https://www.worldometers.info/coronavirus/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print(f"Error: Unable to retrieve data from the website. Status code: {response.status_code}")
        return None


def get_covid_statistics(soup):
    total_cases = soup.find("div", class_="maincounter-number").span.text.strip()
    deaths = soup.find_all("div", class_="maincounter-number")[1].text.strip()
    recovered = soup.find_all("div", class_="maincounter-number")[2].text.strip()
    return int(total_cases.replace(",", "")), int(deaths.replace(",", "")), int(recovered.replace(",", ""))


def visualize_covid_statistics(total_cases, deaths, recovered):
    labels = ['Total Cases', 'Deaths', 'Recovered']
    values = [total_cases, deaths, recovered]

    fig = px.pie(names=labels, values=values)
    fig.update_traces(marker=dict(colors=['orange', 'red', 'green'], line=dict(color='#000000', width=2)))

    # Save Plotly chart to HTML file
    pio.write_html(fig, file='templates/covid_chart.html', full_html=False)


if __name__ == "__main__":
    app.run(debug=True)
