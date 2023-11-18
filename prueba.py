import time
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

def wait_for_video_play(browser, video_playing):
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            assert "vjs-playing" in video_playing.get_attribute("class")
        except AssertionError:
            break
        time.sleep(1)
    assert time.time() - start_time >= 10, "El video no se reprodujo durante 10 segundos"

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_videos(browser):
    browser.get("https://videojs.com/advanced/?video=disneys-oceans")
    WebDriverWait(browser, 10).until(EC.title_contains("Advanced example | Video.js"))

    video = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "preview-player_html5_api"))
    )
    scroll_to_element(browser, video)

    play_button = browser.find_element(By.CLASS_NAME, "vjs-big-play-button")
    play_button.click()

    video_playing = browser.find_element(By.CLASS_NAME, "vjs-playing")
    assert "vjs-playing" in video_playing.get_attribute("class")
    wait_for_video_play(browser, video_playing)

    video2 = browser.find_element(By.XPATH, "//img[@src='//d2zihajmogu5jn.cloudfront.net/sintel/poster.png']")
    video2.click()

    wait_for_video_play(browser, video_playing)

    volume_slider = browser.find_element(By.XPATH, "(//div[contains(@class,'css-v50dlc')])[1]")
    actions = ActionChains(browser)
    slider_width = volume_slider.size['width']
    midpoint = slider_width / 4
    actions.click_and_hold(volume_slider).move_by_offset(-midpoint, 0).release().perform()
    time.sleep(4)
    mute = browser.find_element(By.CLASS_NAME, "CheckboxInput__Box-sc-stvf8-2.fkVQVl")
    mute.click()

    video3 = browser.find_element(By.XPATH, "//img[@src='//d2zihajmogu5jn.cloudfront.net/big-buck-bunny/bbb.png']")
    video3.click()
    mute.click()

    time.sleep(10)

    browser.quit()
