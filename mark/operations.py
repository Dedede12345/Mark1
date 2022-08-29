import time
import tkinter as tk
from tkinter import simpledialog
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoAlertPresentException
from selenium.common import exceptions
from time import sleep
from multiprocessing import Queue
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from mark.common import Prerequisites
import json

def check_for_file(visited):
    while True:

        try:
            line = input("Do you want to save those links? [y/n] ")
            if line == 'y':
                with open('datafile.json', 'w') as file:
                    json.dump(visited, file)
                    break
            if line == 'n':
                # print('adsfasdfasdfasdfafdsf')
                break
            else:
                print('asdfasdfasdf')
                continue

        except EOFError:
            break


def greetings_and_creation():
    print("You are the chosen one to be honored to test pre-alpha of Mark1 By Dedede12345.\n Cheers!!!", )

    gmail = input(
        "Enter your gmail: "
    )

    password = input(
        "Enter your password: "
    )

    text = input(
        'Enter or paste your post text: '
    )

    return Prerequisites(gmail, password, text)


def choose_images(post: Prerequisites):

    counter = 0

    while True:


        if (line:=input(f'Pass{" another" * (counter > 0)} image into a post? [y/n] ')) == 'y': # line:=input('Pass image into a post [y/n] ') == 'y'

            Tk().withdraw()
            filename = askopenfilename()
            post.images.append(filename)

            counter += 1

            continue

        elif line == 'n':
            print(f'{counter} image{"s" * (counter > 1)} has been passed')
            break

        else:

            print(f'Wrong char({line}) try again.')
            continue


def get_element(driver, xpath):
    """
    Get required element via By and required value.
    :return:
    """


    try:
        element = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
        # driver.switch_to.alert.accept()
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass
    except Exception as e:
        raise e

    return element


def input_submit(driver, input, submit, value):
    """
    Enters fill and submit form
    :param driver: 
    :param input: 
    :param submit: 
    :return: 
    """
    #
    # time.sleep(1.5)


    ActionChains(driver).\
        click(input).\
        send_keys(value).\
        click(submit)\
        .perform()

    time.sleep(1)

    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass


def register(driver: Chrome, gmail, password, link='https://vk.com'):

    driver.get(link)

    input_submit(driver,
                 get_element(driver, '//input[@id="index_email"]'),
                 get_element(driver, '//*[@id="index_login"]/div/form/button'),
                 gmail)

    sleep(1)

    input_submit(driver,
                 get_element(driver, '//input[@name="password"]'),
                 get_element(driver, '/html/body/div[1]/div/div/div/div[2]/div/form/div[2]/button'),
                 password)


def visualize(driver):
    try:
        choose_photo = WebDriverWait(driver, 20).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//html/body/div[7]/div[1]/div[2]/div/div[2]/div/div[1]/div/div[1]/input'))
        )

        driver.execute_script("arguments[0].setAttribute('style', 'visibility: visible; position: absolute')",
                              choose_photo)
    except Exception as e:
        raise e


def propose_images(driver, images: list):

    photo_post_button = get_element(driver, '//*[@id="page_add_media"]/div[1]/a')

    for image in images:

        ActionChains(driver).click(photo_post_button).perform()

        visualize(driver)

        send_photo_button = driver.find_element('xpath', '//html/body/div[7]/div[1]/div[2]/div/'
                                                         'div[2]/div/div[1]/div/div[1]/input')
        send_photo_button.send_keys(rf'{image}')

        sleep(3)


def propose_text(driver, text):

    text_input = get_element(driver, '//*[@id="post_field"]')

    ActionChains(driver).click(text_input).send_keys(text).perform()


def propose_post(driver: Chrome, public_link: str, text, images=None):


    if not public_link.startswith('https://vk.com'):
        public_link = f'https://vk.com{public_link}'

    print(f'Sending post to : {public_link}')

    driver.get(public_link)

    sleep(3)

    try:
        if images:
            propose_images(driver, images)

    except exceptions.TimeoutException:
        pass

    propose_text(driver, text)

    submit_button = get_element(driver, '//*[@id="send_post"]')
    ActionChains(driver).click(submit_button).perform()


def get_links_json(queue: Queue):

    with open('datafile.json', 'r') as file:
        links = json.load(file)

        for link in links:
            queue.put(link)


def get_links_queue(driver: Chrome, queue: Queue):

    visited = []

    ActionChains(driver).click(get_element(driver, '//a[@href="/groups"]')).perform()

    sleep(2.5)

    try:

        WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//a[@href]'))
        )
    finally:

        links = driver.find_elements(By.XPATH, '//a[@class="group_row_title"]')
        links = list(set(link.get_attribute('href') for link in links))

        # links = set(Public(link.get_attribute('href'), link.text) for link in links)

        print(f'raw {len(links)} links: ', links, '\n' * 2)

    # Check links


    for link in links:
        driver.get(link)


        try:
            driver.find_element('xpath', '//*[@id="post_field"]')
            public_name = driver.find_element('tag name', 'h1').text
            # public = Public(link, public_name)
        except:
            print(f"Public {link.replace('https://vk.com/', '')} has no posting fields")
            continue

        ROOT = tk.Tk()

        ROOT.withdraw()

        User_inp = simpledialog.askstring(title="Posting", prompt=f"Send post to {public_name}? [y/n]")

        if User_inp == 'y':
            queue.put(link)
            visited.append(link)

        elif User_inp == 'n':
            continue

        else:
            continue

    print(f"Filtered links: {visited}")

    check_for_file(visited)

    return visited

        # queue.put(link)


def clean_queue(raw_queue: Queue, filtered_queue):

    while True:

        if not raw_queue.get():
            time.sleep(0.1)

        else:
            public = raw_queue.get()

            while True:

                if (line:= input(f'Send post to {public.name}')) == 'y':
                    filtered_queue.put(public.link)
                    break

                elif line == 'n':
                    break

                else:
                    print(f"Wrong char {line} try again")
                    continue
