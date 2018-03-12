import time
from selenium import webdriver


class CurateSearch:

    def __init__(self, search_term, custom_url, word_join):
        self.search_term = search_term
        self.custom_url = custom_url
        self.word_join = word_join

    @staticmethod
    def standard_search(search_term):
        return CurateSearch(search_term, None, "+")


class CurateDriver:

    DEFAULT_URL = "https://www.google.com/search?q={}"

    def run(self, searches, company):
        driver = webdriver.Chrome()

        main_window = driver.current_window_handle

        driver.switch_to.window(main_window)

        for i, search in enumerate(searches):

            split_words = company.split(" ")

            if search.custom_url:
                url = search.custom_url
            else:
                url = CurateDriver.DEFAULT_URL
                split_words.insert(0, search.search_term)

            url = url.format(search.word_join.join(split_words))

            if i == 0:
                driver.get(url)
            else:
                driver.execute_script("window.open('{}');".format(url))

            time.sleep(0.1)

        driver.switch_to.window(main_window)
        
        while True:
            pass

searches = [CurateSearch.standard_search('pitchbook'),
            CurateSearch.standard_search('crunchbase'),
            CurateSearch('youtube', 'https://www.youtube.com/results?search_query={}', "+"),
            CurateSearch.standard_search('twitter'),
            CurateSearch.standard_search('facebook')]

curate_driver = CurateDriver()
curate_driver.run(searches, "super evil megacorp")

