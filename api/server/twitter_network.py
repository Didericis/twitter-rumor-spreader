from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os


"""
This will create a network of twitter users from a starting user. The size indicates
the number of users in the network. For each user in the network, we will download a list of
all of the users that user is following.
"""
class TwitterNetwork():
    FILE_NAME =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'network.json')

    def __init__(self, starting_user, size=20):
        self.size = size
        self.starting_user = starting_user

    # Downloading all of a user's followers can take a while, so we want to load
    # the users we've already downloaded from a cache.
    def _load_network_from_cache(self):
        print('Loading from cache...')
        if os.path.isfile(self.FILE_NAME):
            with open(self.FILE_NAME, 'r') as file:
                cache = json.load(file)
                if self.starting_user in cache:
                    print('Loaded {} users from cache'.format(len(cache)))
                    file.close()
                    return cache
                else:
                    print('Cache does not contain current user: ignoring...')
                    return {}
        else:
            print('No cache found.')
            return {}


    # This will download all of the users this particular user is following.
    def _get_following(self, username):
        print('Getting users {} is following...'.format(username))
        driver = self.driver
        flwrx = "//div[@data-testid='UserCell']//span[starts-with(text(),'@')]"
        driver.get('https://twitter.com/{}/following'.format(username))
        driver.set_window_size(400, 800)
        following = set()
        last_height = 0
        count = 0
        while count < 10:
            for element in driver.find_elements_by_xpath(flwrx):
                try:
                    following.add(element.text)
                except Exception as e:
                    pass
            height = driver.execute_script("return window.pageYOffset;")
            if (height > 0) and (height == last_height):
                count += 1
            else:
                count = 0
            driver.execute_script("window.scrollTo(0,window.pageYOffset+400)")
            last_height = height
        print('Got {} followers'.format(len(following)))
        return list(map(lambda t: t.replace('@', ''), following))

    # This is the loop where we build up our network.
    # A "Level" refers to the number of users that are the same distance away
    # from the starting user. For example, consider the following tree:
    #
    #                      0
    #                    / | \
    #                  /   |   \
    #                 /    |    \
    #                1     1     1
    #               /|\   /|\   /|\
    #              2 2 2 2 2 2 2 2 2
    #
    # 0, 1 and 2 are each a level
    # Note that any user within our network could be following a previous user.
    def _get_network(self, starting_user):
        next_level = [starting_user]
        while len(self.network) < self.size:
            new_level = []
            for username in next_level:
                self.network[username] = self._get_following(username)
                self._save()
                # when our network reaches the desired size, bail out
                if len(self.network) == self.size:
                    return self.network
                self._add_followers_to_level(username, new_level)
            next_level = new_level
        return self.network

    # this will add at most 3 users that our user is following
    # to our network, and will make sure that we do not add any users
    # that we aready have in our network
    def _add_followers_to_level(self, username, level=[]):
        num_new_users_in_level = 0
        for user in self.network[username]:
            if num_new_users_in_level >= 3:
                break
            if user not in self.network:
                num_new_users_in_level += 1
                level.append(user)
        return []

    # saves the network to file
    def _save(self):
        print('Got user {}/{}'.format(len(self.network), self.size))
        print("Saving...")
        with open(self.FILE_NAME, 'w') as f:
            json.dump(self.network, f)
            f.close()

    def download(self):
        self.network = self._load_network_from_cache()

        if len(self.network) >= self.size:
            return self.network

        baseurl = "https://www.twitter.com"
        login = os.environ.get('TWITTER_USERNAME')
        pwd = os.environ.get('TWITTER_PASSWORD')

        usrx = "//input[@name='session[username_or_email]']"
        pwdx = "//input[@name='session[password]']"
        submitx = "//input[@type='submit']"

        # executable_path = '/usr/local/bin/chromedriver'
        # executable_path = '/usr/bin/firefox'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(baseurl)
        self.driver.find_element_by_xpath(usrx).clear()
        self.driver.find_element_by_xpath(usrx).send_keys(login)
        self.driver.find_element_by_xpath(pwdx).clear()
        self.driver.find_element_by_xpath(pwdx).send_keys(pwd)
        self.driver.find_element_by_xpath(submitx).click()
        self._get_network(self.starting_user)
        self.driver.quit()
        return self.network
