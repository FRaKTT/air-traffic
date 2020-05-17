from selenium import webdriver
import time
from datetime import datetime
import sys
import os
from config import FR24_URL, AREAS, RENDER_DELAY



def close_banners(driver):
    """Closing banners on the website"""
    #close cookies banner
    cookies_banner_xpath = {'firefox': '/html/body/div[3]/div[4]/button',
                            'chrome': '//*[@id="map"]/div[3]/div[4]/button'}
    xpath = cookies_banner_xpath[driver.name]
    element = driver.find_element_by_xpath(xpath)
    element.click()

    #close ads banner
    # xpath = '//*[@id="cbb"]/svg'
    # xpath = '/html/body/div[2]/div[2]/div/div/div[2]/div/div[3]/svg'
    # element = driver.find_element_by_xpath(xpath)
    # element.click()


def screenshot(driver, area, screenshot_name='latest.png'):
    """Take a screenshot of the area"""
    url = FR24_URL + area
    driver.get(url)

    # https://www.selenium.dev/documentation/en/webdriver/browser_manipulation/#window-management
    window_size = (1920, 1080)
    # window_size = (3000, 2000)
    driver.set_window_size(*window_size)
    
    # https://www.selenium.dev/documentation/en/webdriver/waits/
    # webdriver.support.ui.WebDriverWait(driver, timeout=3).until(some_condition)  # webdriver.support.expected_conditions.visibility_of_all_elements_located(locator)
    
    time.sleep(1)
    for i in range(3):
        try:
            close_banners(driver)
        except Exception as e:
            time.sleep(1)
            continue
    time.sleep(RENDER_DELAY)  # wait for all elements to appear
    screenshot = driver.save_screenshot(screenshot_name)


def get_driver_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(chrome_options=options)

def get_driver_firefox():
    options = webdriver.firefox.options.Options()
    options.headless = True
    return webdriver.Firefox(options=options)
      
def get_driver(browser):
    """Choose driver for browser, create it and return"""
    get_driver_functions = {'firefox': get_driver_firefox,
                            'chrome': get_driver_chrome}
    get_driver_func = get_driver_functions[browser]
    driver = get_driver_func()
    return driver


def shot_pathname(area_name, shots_dir='.', use_area_subdirs=True):
    """Set screenshot filename, create dirs and return path to it"""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'{area_name}_{now}.png'
    if use_area_subdirs:  # use subdir for area
        shots_dir = os.path.join(shots_dir, area_name)
    os.makedirs(shots_dir, exist_ok=True)  # make dir if it doesn't exist
    pathname = os.path.join(shots_dir, filename)
    return pathname


def shot(browser, area_name, shots_dir='.'):
    """Take screenshot of one area"""
    driver = get_driver(browser)
    screenshot_name = shot_pathname(area_name, shots_dir)
    area = AREAS[area_name]
    screenshot(driver, area, screenshot_name)
    print(f'Screenshot was taken: {screenshot_name}')
    driver.quit()


def shot_all(browser, shots_dir='.'):
    """Take screenshots of all areas"""
    driver = get_driver(browser)
    for area_name, area in AREAS.items():
        screenshot_name = shot_pathname(area_name, shots_dir)
        screenshot(driver, area, screenshot_name)
        print(f'Screenshot was taken: {screenshot_name}')
    driver.quit()


def loop():
    last_hour = None
    DELAY = 20
    while True:
        now = datetime.now()
        if now.minute == 0 and last_hour != now.hour:
            shot_all('firefox')
            last_hour = now.hour
        time.sleep(DELAY)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        path_to_save = sys.argv[1]
        shot_all('firefox', path_to_save)
    else:
        shot_all('firefox')
    
    # shot('firefox', 'russia')  # for test
