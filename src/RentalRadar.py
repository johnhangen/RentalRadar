import requests
from lxml import html
import pandas as pd
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()


class RentalRadar(object):

    def __init__(self, city: str, num_bedrooms: int) -> None:
        self._city:str = city
        self._num_bedrooms: int = num_bedrooms
        self.url:str  = 'https://www.apartments.com/' + city + '/' + str(num_bedrooms) + '-bedrooms/'

        self.rental_links = []

    @property
    def city(self) -> str:
        return self._city
    
    @city.setter
    def city(self, city: str) -> None:
        self._city = city
        self.url = 'https://www.apartments.com/' + city + '/' + str(self._num_bedrooms) + '-bedrooms/'

    @property
    def num_bedrooms(self) -> int:
        return self._num_bedrooms
    
    @num_bedrooms.setter
    def num_bedrooms(self, num_bedrooms: int) -> None:
        self._num_bedrooms = num_bedrooms
        self.url = 'https://www.apartments.com/' + self._city + '/' + str(num_bedrooms) + '-bedrooms/'
    

    @staticmethod
    def fetch_html(url):
        try:
            headers = requests.utils.default_headers()

            headers.update(
                {
                    'User-Agent': 'My User Agent 1.0',
                }
            )
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                print("Error: Failed to fetch HTML. Status code:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print("Error: Failed to fetch HTML:", e)
            return None

    def scan(self) -> None:
        tree = html.fromstring(self.fetch_html(self.url))

        i = 1
        while True:
            link = tree.xpath(f'//*[@id="placardContainer"]/ul/li[{i}]/article/@data-url')

            if link != []:
                self.rental_links.append("/".join(link[0].split('/')[:-2]))
                i += 1
            else:
                break

    @staticmethod
    def load_data(path: str = 'data/rentals.csv') -> pd.DataFrame:
        return pd.read_csv(path, header=None)
    
    def save_data(self, path: str = 'data/rentals.csv') -> None:
        pd.DataFrame(self.rental_links).to_csv(path, index=False, header=False)

    def get_new_data(self) -> pd.DataFrame:
        prior = self.load_data()
        current = pd.DataFrame(self.rental_links)

        return current[~current.isin(prior)].dropna()
    
    def send_emails(self) -> None:
        updated_rentals = self.get_new_data()

        if not updated_rentals.empty:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(os.getenv("email"), os.getenv("password"))

            message = ""

            for i in range(len(updated_rentals)):
                message += updated_rentals.iloc[i][0] + "\n"

            server.sendmail(
                os.getenv("email"), 
                os.getenv("email"), 
                'Subject: {}\n\n{}'.format("RentalRadar update", message)
                )

            server.quit()

        self.save_data()


        
