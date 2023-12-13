from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

def get_news_titles(url, website_name):
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            titles = []

            if 'udn.com' in url:
                # Scraping logic for 聯合新聞網
                titles = [title.text.strip() for title in soup.select('.tab-link__title')]
                links = [link['href'] for link in soup.select('.tab-link')]
                return {'website_name': "聯合新聞網", 'titles': titles, 'links':links}

            elif 'ltn.com.tw' in url:
                # Scraping logic for 自由時報
                titles = [title.get('title') for title in soup.find_all('a', class_='ph listS_h')]
                links = [link.get('href') for link in soup.find_all('a', class_='ph listS_h')]

                return {'website_name': "自由時報", 'titles': titles, 'links':links}

            elif 'news.tvbs.com.tw' in url:
                # Scraping logic for TVBS新聞
                titles = [title.text.strip() for title in soup.find_all('div', class_='good_news_txt')]
                links = [link.find('a')['href'] for link in soup.find_all('div', class_='good_news_txt')]
                for i in range(len(links)):
                    links[i] = links[i] if links[i].startswith("http") else urljoin("https://news.tvbs.com.tw", links[i])

                return {'website_name': "TVBS新聞", 'titles': titles, 'links':links}

            elif 'www.ettoday.net' in url:
                # Scraping logic for ETtoday新聞雲
                titles = [title.text.strip() for title in soup.select('div.piece h3 a')]
                links = [link.get('href') for link in soup.select('div.piece h3 a')]
                for i in range(len(links)):
                    links[i] = links[i] if links[i].startswith("http") else urljoin("https://www.ettoday.net/news/hot-news.htm", links[i])
                return {'website_name': "ETtoday新聞雲", 'titles': titles, 'links':links}

            # Add more elif statements for additional news websites as needed

        else:
            return {'error': f'Error {response.status_code}: Unable to fetch the URL.'}
    except Exception as e:
        return {'error': f'An error occurred: {str(e)}'}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        selected_website = request.form['website']
        website_name = request.form['website'].split('/')[-2]  # Extract the website name from the URL

        result = get_news_titles(selected_website, website_name)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,port=5000, debug=True)
