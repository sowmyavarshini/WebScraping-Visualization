
# Web Scraping and Visualization

Data is scraped from a simple website and visualization is created.

## Website used: 
https://www.worldometers.info/coronavirus/

## Scraping Process

- BeautifulSoup - the web scraping library is used to scrape data from the website.
- Covid-19 data - the number of cases recorded, the number of cases recovered and deaths are scraped.
  
  
  ```python
  import requests
  from bs4 import BeautifulSoup
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
  ```
  ### Get Covid statistics
  
  ```python
   def get_covid_statistics(soup):
     total_cases = soup.find("div", class_="maincounter-number").span.text.strip()
     deaths = soup.find_all("div", class_="maincounter-number")[1].text.strip()
     recovered = soup.find_all("div", class_="maincounter-number")[2].text.strip()
     return int(total_cases.replace(",", "")), int(deaths.replace(",", "")), int(recovered.replace(",", ""))
  ```

## Visualization 

 - Flask framework is used and a route to view the visualization is created.
 - Plotly library is used to create pie chart of the scraped data.
 - plotly.io is used to return a copy of a figure   where all styling properties have been moved into the figure's template. It is used to convert a figure to an HTML string representation.
   
   ```bash
   import plotly.express as px
   import plotly.io as pio
   ```
## Visualization creation

```python
    def visualize_covid_statistics(total_cases, deaths, recovered):
      labels = ['Total Cases', 'Deaths', 'Recovered']
      values = [total_cases, deaths, recovered]

      fig = px.pie(names=labels, values=values)
      fig.update_traces(marker=dict(colors=['orange', 'red', 'green'], line=dict(color='#000000', width=2)))

      # Save Plotly chart to HTML file
      pio.write_html(fig, file='templates/covid_chart.html', full_html=False)
```
## Viewing visualizations

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>COVID-19 Statistics</title>
    <script src="https://mpld3.github.io/js/mpld3.v0.5.2.js"></script>
</head>
<body>

    <h1>COVID-19 Statistics</h1>

    <!-- Embed the generated HTML content -->
    <div id="chart-container">
        {% include 'covid_chart.html' %}
    </div>

</body>
</html>
```

## Pie chart

![piechart](https://github.com/sowmyavarshini/WebScraping-Visualization/assets/22410066/8eb7f463-4fc5-426f-bbc5-d4d2741951ef)

