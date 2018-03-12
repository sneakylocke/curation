import time
from selenium import webdriver


class CurateSearch:

    def __init__(self, website, custom_url, word_join):
        self.website = website
        self.custom_url = custom_url
        self.word_join = word_join

    @staticmethod
    def standard_search(search_term):
        return CurateSearch(search_term, None, "+")


class CurateDriver:

    DEFAULT_URL = "https://www.google.com/search?q={}"
    SLEEP_TIME = 0.0

    def run(self, searches, company):

        # Open chrome
        driver = webdriver.Chrome()

        # Get handle to first window
        main_window = driver.current_window_handle

        # Maximize chrome
        driver.switch_to.window(main_window)

        # Open all tabs
        for i, search in enumerate(searches):

            # Split company words so we can form a string that works with a url
            split_words = company.split(" ")

            # If we have a custom url we can drop the website from the words we are joining (the term 'youtube' is not
            # needed when we do a search within youtube itself)
            if search.custom_url:
                url = search.custom_url
            else:
                url = CurateDriver.DEFAULT_URL
                split_words.insert(0, search.website)

            # Make final url
            url = url.format(search.word_join.join(split_words))

            # First iteration do not make a new tab
            if i == 0:
                driver.get(url)
            else:
                driver.execute_script("window.open('{}');".format(url))

            # Chill
            time.sleep(CurateDriver.SLEEP_TIME)

        # Go back to first tab
        driver.switch_to.window(main_window)

        # Wait forever, this holds the chrome open
        while True:
            pass

# A list of all the searches
searches = [CurateSearch.standard_search('pitchbook'),
            CurateSearch.standard_search('crunchbase'),
            CurateSearch('youtube', 'https://www.youtube.com/results?search_query={}', "+"),
            CurateSearch('twitter', 'https://twitter.com/search?q={}&src=typd', "%20"),
            CurateSearch('facebook', 'https://facebook.com/search/top/?q={}', "+"),
            CurateSearch.standard_search('itunes'),
            CurateSearch.standard_search('google play'),
            CurateSearch.standard_search('instagram')]

# The company you are researching
company = "mad paws"

# Create the driver and run it
curate_driver = CurateDriver()
curate_driver.run(searches, company)
