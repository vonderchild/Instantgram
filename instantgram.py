from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from explicit import waiter, XPATH
import itertools
import time


class Instagram:

    def __init__(self, username, password):
        self.password = password
        self.username = username
        self.browser = webdriver.Firefox()

    def login(self):
        browser = self.browser
        browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        try:
            username_input = browser.find_element_by_name("username")
            pw_input = browser.find_element_by_name("password")

            username_input.send_keys(self.username)
            pw_input.send_keys(self.password)
            pw_input.send_keys(Keys.ENTER)
            time.sleep(3)

        except Exception as e:
            print("Error Code: ", e)

    def follow(self, user):

        expected_title = "Content Unavailable • Instagram"
        browser = self.browser
        browser.get("https://www.instagram.com/" + user + "/")
        time.sleep(2)

        try:
            title = browser.title
            if title == expected_title:
                print("account does not exist")
                return

            follow_button = browser.find_element_by_css_selector("._5f5mN")

            if follow_button.text == "Follow":
                follow_button.click()
                print("you're now following", "@" + user)
            else:
                print("you're already following this user")

        except Exception as e:
            print("Error Code: ", e)

    def unfollow(self, user):
        browser = self.browser

        try:
            browser.get("https://www.instagram.com/" + user + "/")
            time.sleep(2)

            follow_button = browser.find_element_by_css_selector("._5f5mN")

            if follow_button.text == "Following":
                follow_button.click()

                unfollow_button = browser.find_element_by_xpath('//button[text() = "Unfollow"]')
                unfollow_button.click()

                print("unfollowed", "@" + user)

            else:
                print("you're not following this user")

        except Exception as e:
            print("Error Code: ", e)

    def scrape_followers(self, username):
        browser = self.browser

        try:
            browser.get("https://www.instagram.com/" + username + "/")
            browser.find_element_by_partial_link_text('follower').click()

            waiter.find_element(browser, "//div[@role='dialog']", by=XPATH)

            follower_css = "ul div li:nth-child({}) a.notranslate"
            follower_index = 0
            for group in itertools.count(start=1, step=12):
                for follower_index in range(group, group + 12):
                    yield waiter.find_element(browser, follower_css.format(follower_index)).text
                last_follower = waiter.find_element(browser, follower_css.format(follower_index))
                browser.execute_script("arguments[0].scrollIntoView();", last_follower)

        except Exception as e:
            print("Error Code: ", e)

    def scrape_following(self, username):
        browser = self.browser
        try:
            browser.get("https://www.instagram.com/" + username + "/")
            browser.find_element_by_partial_link_text('following').click()

            waiter.find_element(browser, "//div[@role='dialog']", by=XPATH)

            following_css = "ul div li:nth-child({}) a.notranslate"
            following_index = 0
            for group in itertools.count(start=1, step=12):
                for following_index in range(group, group + 12):
                    yield waiter.find_element(browser, following_css.format(following_index)).text
                last_following = waiter.find_element(browser, following_css.format(following_index))
                browser.execute_script("arguments[0].scrollIntoView();", last_following)

        except Exception as e:
            print("Error Code: ", e)

    def logout(self):
        browser = self.browser

        try:
            browser.get("https://www.instagram.com/" + self.username + "/")
            time.sleep(2)

            settings_button = browser.find_element_by_css_selector(".dCJp8")
            settings_button.click()
            time.sleep(1)

            logout_button = browser.find_element_by_xpath('//button[text() = "Log Out"]')
            logout_button.click()

            print("successfully logged out")

        except Exception as e:
            print("Error Code: ", e)

    def close_browser(self):
        print("Exiting...")
        self.browser.close()


def get_following_list():
    target_user = input("enter target username: ")
    n = int(input("how many followings do you want to scrape? "))
    print()

    with open("following.txt", 'w') as f:
        for i, following in enumerate(instance.scrape_following(target_user), 1):
            print(i, following, sep=". ", end="\n")
            f.write(str(i) + "." + following + "\n")
            if i == n:
                break


def get_followers_list():
    target_user = input("enter target username: ")
    n = int(input("how many followers do you want to scrape? "))
    print()

    with open("followers.txt", 'w') as f:
        for i, follower in enumerate(instance.scrape_followers(target_user), 1):
            print(i, follower, sep=". ", end="\n")
            f.write(str(i) + "." + follower + "\n")
            if i == n:
                break


if __name__ == "__main__":
    print("{1}-- login\n"
          "{2}-- exit\n")
    choice = int(input())
    if choice != 1:
        print("Exiting...")
        exit(1)

    else:
        user_name = input("enter your username: ")
        pwd = input("enter your password: ")
        instance = Instagram(user_name, pwd)
        instance.login()
        print("successfully logged in", "\n")

        print("{1}-- follow\n"
              "{2}-- unfollow\n"
              "{3}-- get followers list\n"
              "{4}-- get following list\n"
              "{5}-- logout\n"
              )
        choice = int(input())
        if choice == 1:
            instance.follow(input("enter username to follow "))
        elif choice == 2:
            instance.unfollow(input("enter username to unfollow "))
        elif choice == 3:
            get_followers_list()
        elif choice == 4:
            get_following_list()

        print()
        instance.logout()
        instance.close_browser()
