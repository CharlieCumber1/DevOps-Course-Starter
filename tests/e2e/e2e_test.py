import os
import app
import trello_items as trello
from threading import Thread
import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv, find_dotenv

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    board_id = trello.create_board('e2e-test-board')
    os.environ['TRELLO_BOARD'] = board_id

    # construct the new application
    application = app.create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    trello.delete_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    title_input = driver.find_element_by_id('title')
    submit_info = driver.find_element_by_id('submit-button')

    task_title = 'This is a test item generated by selenium driver'

    title_input.send_keys(task_title)
    submit_info.click()
    assert check_task_in_table(driver, task_title, 'outstanding')
    assert not check_task_in_table(driver, task_title, 'pending')
    assert not check_task_in_table(driver, task_title, 'done')
    
    get_link_by_task_title(driver, task_title, 'Start').click()
    assert check_task_in_table(driver, task_title, 'pending')

    get_link_by_task_title(driver, task_title, 'Complete').click()
    assert check_task_in_table(driver, task_title, 'done')

    get_link_by_task_title(driver, task_title, 'Delete').click()
    assert not check_task_in_table(driver, task_title, 'outstanding')
    assert not check_task_in_table(driver, task_title, 'pending')
    assert not check_task_in_table(driver, task_title, 'done')

def get_link_by_task_title(driver, title, link):
    return driver.find_element_by_xpath(f'//table//tr[td/strong[text() = "{title}"]]//a[text() = "{link}"]')

def check_task_in_table(driver, title, status):
    try:
        driver.find_element_by_xpath(f'//table[@id="{status}"]//strong[text() = "{title}"]').is_displayed()
    except NoSuchElementException:
        return False
    return True