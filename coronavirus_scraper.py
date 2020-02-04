# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import datetime
import json
import selenium.webdriver
import time

from selenium.webdriver.common.by import By


# --------------------------------------------------------------------------------
# WebDriver Builder
# --------------------------------------------------------------------------------

def init_webdriver():
  opts = selenium.webdriver.ChromeOptions()
  opts.add_argument('headless')
  browser = selenium.webdriver.Chrome(options=opts)
  browser.implicitly_wait(10)
  browser.maximize_window()
  return browser


# --------------------------------------------------------------------------------
# CoronavirusData
# --------------------------------------------------------------------------------

class CoronavirusData:

  def __init__(self, updated=0, confirm=0, suspect=0, cure=0, dead=0, timestamp=None):
    self.updated = updated
    self.confirm = confirm
    self.suspect = suspect
    self.cure = cure
    self.dead = dead
    self.timestamp = datetime.datetime.utcnow() if not timestamp else timestamp
  
  def is_different_from(self, other):
    return \
      self.confirm != other.confirm or \
      self.suspect != other.suspect or \
      self.cure != other.cure or \
      self.dead != other.dead
  
  def __str__(self):
    return json.dumps({
      'timestamp': str(self.timestamp),
      'updated': self.updated,
      'confirm': self.confirm,
      'suspect': self.suspect,
      'cure': self.cure,
      'dead': self.dead
    })
  
  def __repr__(self):
    return self.__str__()


# --------------------------------------------------------------------------------
# QQCoronavirusPage
# --------------------------------------------------------------------------------

class QQCoronavirusPage:

  @staticmethod
  def xpath_number(name):
    return f'//div[contains(@class, "topdataWrap")]//div[contains(@class, "{name}")]/div[contains(@class, "number")]'

  URL = 'https://news.qq.com//zt2020/page/feiyan.htm'

  UPDATED = (By.XPATH, '//div[contains(@class, "topdataWrap")]//div[contains(@class, "timeNum")]//span[contains(., "2020")]')
  CONFIRM = (By.XPATH, xpath_number.__func__('confirm'))
  SUSPECT = (By.XPATH, xpath_number.__func__('suspect'))
  CURE = (By.XPATH, xpath_number.__func__('cure'))
  DEAD = (By.XPATH, xpath_number.__func__('dead'))

  def __init__(self, browser):
    self.browser = browser

  def load(self):
    self.browser.get(self.URL)

  def get_updated(self):
    return browser.find_element(*self.UPDATED).text

  def get_confirm(self):
    return browser.find_element(*self.CONFIRM).text

  def get_suspect(self):
    return browser.find_element(*self.SUSPECT).text

  def get_cure(self):
    return browser.find_element(*self.CURE).text

  def get_dead(self):
    return browser.find_element(*self.DEAD).text
  
  def get_latest_data(self):
    return CoronavirusData(
      self.get_updated(),
      self.get_confirm(),
      self.get_suspect(),
      self.get_cure(),
      self.get_dead()
    )
  
  def take_screenshot(self):
    name = self.get_updated().replace(':', '')
    self.browser.save_screenshot(f'{name}.png')


# --------------------------------------------------------------------------------
# Logging Functions
# --------------------------------------------------------------------------------

def append_log(path, data):
  with open(path, 'a+') as f:
    f.write(str(data))
    f.write('\n')


# --------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------

CHANGES_LOG = 'changes.log'
FULL_LOG = 'full.log'


if __name__ == '__main__':

  previous = CoronavirusData()

  while True:

    try:
      browser = init_webdriver()
      page = QQCoronavirusPage(browser)

      page.load()
      data = page.get_latest_data()
      append_log(FULL_LOG, data)

      if data.is_different_from(previous):
        print(data)
        append_log(CHANGES_LOG, data)
        page.take_screenshot()
      
      previous = data

    finally:
      browser.quit()
      time.sleep(10)
