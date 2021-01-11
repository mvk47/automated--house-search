# complete
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

chrome_driver_path = # your chrome path

google_doc_link = # Link-to-google-doc

zillow_link = "https://www.zillow.com/homes/for_rent/1-1_beds/?searchQu" \
              "eryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%" \
              "3A%7B%22west%22%3A-122.55005873632813%2C%22east%22%3A-122." \
              "31659926367188%2C%22south%22%3A37.66109279195355%2C%22north%" \
              "22%3A37.88931398873887%7D%2C%22mapZoom%22%3A12%2C%22isMapVisi" \
              "ble%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max" \
              "%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3A1" \
              "%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%2" \
              "2value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc" \
              "%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afal" \
              "se%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22" \
              "value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%2" \
              "2pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%" \
              "3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

headers = {
    "Accept-Language": "en-US,en;q=0.9,te;q=0.8,la;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 "
                  "Safari/537.36"

}
full_list = []


class JobAutomation:
    def __init__(self):
        self.response = requests.get(url=zillow_link, headers=headers)
        self.data = self.response.text
        self.soup = BeautifulSoup(self.data, 'html.parser')
        print(self.soup.prettify())
        self.driver = webdriver.Chrome(chrome_driver_path)
        self.element = (self.soup.find_all(name='div', class_='list-card-info'))

    def data_from_beauti(self):
        new_item = []
        for link in self.element:
            new_link = (link.find(name='a').get("href"))
            if new_link[0] == "/":
                new_item.append("https://www.zillow.com"+new_link)
            else:
                new_item.append(new_link)
            new_item.append(link.find(name='address', class_='list-card-addr').text)
            try:
                new_item.append(link.find(name='div', class_='list-card-price').text)
            except AttributeError:
                new_item.append(link.find(name='ul', class_='list-card-details').find(name='li').text.split(" ")[0])
                continue
            full_list.append(new_item)
            new_item = []
        print(full_list)

    def adding_to_sheets(self):
        self.driver.get(# google form)
        time.sleep(6)
        for inner_list in full_list:
            self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2'
                                              ']/div/div[2]/div[1]/div/div/div'
                                              '[2]/div/div[1]/div/div[1]/input').send_keys(inner_list[1])
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div'
                                              '[2]/div[2]/div/div/div[2]/div/div[1]'
                                              '/div/div[1]/input').send_keys(inner_list[2])
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]'
                                              '/div[3]/div/div/div[2]/div/div[1]/div'
                                              '/div[1]/input').send_keys(inner_list[0])
            time.sleep(1)
            submit = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/'
                                                       'div/div[3]/div[1]/div/div/span')
            self.driver.execute_script("arguments[0].click();", submit)
            time.sleep(5)
            self.driver.find_element_by_css_selector('body > div.freebirdFormviewerViewFormContentWrapper '
                                                     '> div:nth-child(2) > div.freebirdFormviewerViewFormCard.ex'
                                                     'portFormCard > div > div.freebirdFormviewerViewResponseLinksCo'
                                                     'ntainer > a').click()

            time.sleep(5)

    def quit_terminal(self):
        self.driver.quit()


job1 = JobAutomation()
job1.data_from_beauti()
job1.adding_to_sheets()
time.sleep(3)
job1.quit_terminal()
