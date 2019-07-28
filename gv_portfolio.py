from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime
import lxml


def run(url):
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y-%H")
    filename = 'gv-portfolio-' + dt_string + '.csv'
    csvFile = open(filename, 'w')
    csvFile.write("name,about,link,investor,exit\n")

    # retry 5 times
    for i in range(5):
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
            htmlContent = response.content
            break
        except Exception as e:
            print("Failed attempt: ", i)

    # Parse HTML Content
    soup = BeautifulSoup(htmlContent.decode('ascii', 'ignore'), 'html.parser')
    companies = soup.findAll('a', {'class': re.compile('companyList-item js-companyModalLink')})

    # for each Company build parse data
    for company in companies:
        name = company['data-name']
        if company.has_attr('href'):
            link = company['href']
        else:
            link = "No Link"
        about = company['data-about'].replace(',', '-')
        investors = company['data-investors'].replace(',', '-')
        if company.has_attr('data-exit'):
            exitDetail = company['data-exit'].replace(',', '-')
        else:
            exitDetail = "No Exit Yet"
        csvFile.write(name + "," + about + "," + link + "," + investors + "," + exitDetail + "\n")
    csvFile.close()


if __name__ == '__main__':
    url = 'https://www.gv.com/portfolio/'
    run(url)
