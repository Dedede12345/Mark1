from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from time import sleep
from multiprocessing import Queue


def get_element(driver, xpath):
    """
    Get required element via By and required value.
    :return:
    """

    try:
        element = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
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
    ActionChains(driver).\
        click(input).\
        send_keys(value).\
        click(submit)\
        .perform()


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

        sleep(1.5)


def propose_text(driver, text):

    text_input = get_element(driver, '//*[@id="post_field"]')

    ActionChains(driver).click(text_input).send_keys(text).perform()


def propose_post(driver: Chrome, public_link: str, text, images=None):


    if not public_link.startswith('https://vk.com'):
        public_link = f'https://vk.com{public_link}'

    # print(f'public_link = {public_link}')

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


def main(gmail=None, password=None, text=None, images=None):

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = Chrome(
        ChromeDriverManager().install()
    )

    register(driver, gmail, password)

    sleep(4)

    print(get_links(driver))

    sleep(2.5)


    for public in get_links(driver):

        propose_post(driver, public, text, images)

        sleep(2.5)

    driver.close()


def get_links(driver: Chrome):

    ActionChains(driver).click(get_element(driver, '//a[@href="/groups"]')).perform()

    sleep(2.5)

    try:

        WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//a[@href]'))
        )
    finally:

        links = driver.find_elements(By.XPATH, '//a[@class="group_row_title"]')
        links = [link.get_attribute('href') for link in links]

    # Check links

    verified_links = []

    for link in links:

        if not link.startswith('https://'):
            driver.get(f'https://vk.com{link}')

        else:
            driver.get(link)

            try:

                WebDriverWait(driver, 3).until(
                    expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="post_field"]'))
                )

            except:
                continue

            finally:

                verified_links.append(link)


    return links

def get_links_queue(driver: Chrome, queue: Queue):

    ActionChains(driver).click(get_element(driver, '//a[@href="/groups"]')).perform()

    sleep(2.5)

    try:

        WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//a[@href]'))
        )
    finally:

        links = driver.find_elements(By.XPATH, '//a[@class="group_row_title"]')
        links = [link.get_attribute('href') for link in links]

    # Check links
    for link in links:
        driver.get(link)

        try:
            driver.find_element('xpath', '//*[@id="post_field"]')
        except:
            print(f"Public {link.replace('https://vk.com/', '')} has no posting fields")
            continue
        # finally:
        #     print(f"{link} has element {element}")

        print(link)

        queue.put(link)


#
# main(
#     gmail='testingmak390@gmail.com',
#     password='testing1!',
#     text='Another testing one, for fox\'s sake',
#     images=[r'D:\Мои документы\Изображения\real shit man\Портрет_агронома_М.Е._Вьюнникова.jpg'])
