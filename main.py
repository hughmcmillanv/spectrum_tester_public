import time

from selenium import webdriver

PROMISED_DOWN = 400  # Enter your advertised download speed
PROMISED_UP = 10  # Enter your uploaded download speed
CHROME_DRIVER_PATH = "chrome_driver_path"  # Enter your Chrome driver path
TWITTER_USERNAME = "twitter_username"  # Enter your Twitter account username
TWITTER_PASSWORD = "twitter_password"  # Enter your Twitter account password


class InternetSpeedTwitterBot:

    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.down = 0
        self.up = 0

    def get_internet_speed(self) -> tuple[float, float]:
        """
        Uses SpeedTest.com to test the current Internet download and upload speeds

        :return Internet download and upload speeds expressed as floats within a tuple:
        :rtype tuple[float, float]:
        """
        url = "https://www.speedtest.net"
        self.driver.get(url)

        go_button = self.driver.find_element_by_class_name("start-text")
        go_button.click()

        time.sleep(45)

        down_speed = round(float(
            self.driver.find_element_by_class_name("result-data-large.number.result-data-value.download-speed").text),
            2)
        up_speed = round(float(
            self.driver.find_element_by_class_name("result-data-large.number.result-data-value.upload-speed").text), 2)

        print(f"down: {down_speed}")
        print(f"up: {up_speed}")

        self.down = down_speed
        self.up = up_speed

        return down_speed, up_speed

    def tweet_at_provider(self):
        """
        If get_internet_speed() returns Internet download and upload speeds less than Spectrum's promised download and
        upload speeds, expressed as constants, send a tweet with the the current inadequate download and upload speeds.

        :return: None
        :rtype: None
        """
        url = "https://twitter.com"
        self.driver.get(url)

        time.sleep(3)

        email_box = self.driver.find_element_by_css_selector("#react-root > div > div > div > main > div > div > div "
                                                             "> div.css-1dbjc4n.r-1777fci.r-1qmwkkh.r-nsbfu8 > "
                                                             "div.css-1dbjc4n.r-1awozwy.r-1d2f490.r-dnmrzs.r-1dye5f7"
                                                             ".r-u8s1d.r-19lq7b1 > div > form > div > div:nth-child("
                                                             "6) > div > label > div > "
                                                             "div.css-1dbjc4n.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1wzrnnt"
                                                             ".r-1udh08x.r-xd6kpl.r-1pn2ns4.r-ttdzmv > div > input")
        email_box.send_keys(TWITTER_USERNAME)

        password_box = self.driver.find_element_by_css_selector("#react-root > div > div > div > main > div > div > "
                                                                "div > div.css-1dbjc4n.r-1777fci.r-1qmwkkh.r-nsbfu8 > "
                                                                "div.css-1dbjc4n.r-1awozwy.r-1d2f490.r-dnmrzs.r"
                                                                "-1dye5f7.r-u8s1d.r-19lq7b1 > div > form > div > "
                                                                "div:nth-child(7) > div > label > div > "
                                                                "div.css-1dbjc4n.r-18u37iz.r-16y2uox.r-1wbh5a2.r"
                                                                "-1wzrnnt.r-1udh08x.r-xd6kpl.r-1pn2ns4.r-ttdzmv > div "
                                                                "> input")
        password_box.send_keys(TWITTER_PASSWORD)

        time.sleep(3)

        log_in_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div['
                                                          '1]/div[1]/div/form/div/div[3]/div')
        log_in_button.click()

        tweet_text = f"Hey Spectrum, why is my Internet speed {self.down}down/{self.up}up when I pay for" \
                     f" {PROMISED_DOWN}down/{PROMISED_UP}up? "

        time.sleep(3)

        tweet_box = self.driver.find_element_by_class_name(
            "public-DraftStyleDefault-block.public-DraftStyleDefault-ltr")
        tweet_box.send_keys(tweet_text)

        time.sleep(3)

        if self.down < PROMISED_DOWN or self.up < PROMISED_UP:
            tweet_button = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div['
                '1]/div/div/div/div[ '
                '2]/div[4]/div/div/div[2]/div[3]/div/span/span')
            tweet_button.click()
        else:
            print("Internet speeds are in line with Spectrum's promised speeds.")

        time.sleep(3)

        self.driver.quit()


bot = InternetSpeedTwitterBot(driver_path=CHROME_DRIVER_PATH)
bot.get_internet_speed()
bot.tweet_at_provider()
