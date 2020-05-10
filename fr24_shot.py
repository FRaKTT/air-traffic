from selenium import webdriver
import time
from datetime import datetime
import sys

FR24_URL = 'https://www.flightradar24.com/'
AREAS = {'eurasia'  : '41.95,53.45/4',
        'europe'    : '48.77,18.64/5',
        'russia'    : '56.85,42.64/6',
        'russia2'   : '57.85,55.56/5',
        'moscow'    : '55.77,37.54/9',
        'usa'       : '38.28,-96.98/5',
        'asia'      : '33.29,101.83/4',
}


def close_banners(driver):
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
    time.sleep(5)  # wait for all elements to appear
    screenshot = driver.save_screenshot(screenshot_name)


def get_driver_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(chrome_options=options)


def get_driver_firefox():
    options = webdriver.firefox.options.Options()
    options.headless = True
    return webdriver.Firefox(options=options)
      

def shot(browser, area_name):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f'{area_name}_{now}.png'
    get_driver = {'firefox': get_driver_firefox,
                    'chrome': get_driver_chrome}
    driver = get_driver[browser]()
    screenshot(driver, AREAS[area_name], screenshot_name)
    print(f'Screenshot was taken: {screenshot_name}')
    driver.quit()


def shot_all(browser, path_to_save='.'):
    get_driver = {'firefox': get_driver_firefox,
                    'chrome': get_driver_chrome}
    driver = get_driver[browser]()
    for area_name, area in AREAS.items():
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f'{path_to_save}/{area_name}_{now}.png'
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
    # if len(sys.argv) == 2:
    #     path_to_save = sys.argv[1]
    #     shot_all('firefox', path_to_save)
    # else:
    #     shot_all('firefox')
    
    shot('firefox', 'russia')
