from multiprocessing import Process, Queue
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
from mark.operations import get_links_queue, register, propose_post


def filter_public_links(filteredQueue, gmail, password):

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = Chrome(
        ChromeDriverManager().install(),
    )

    register(driver, gmail, password)
    get_links_queue(driver, filteredQueue)

    driver.close()
    

def main_posts(filteredQueue: Queue, gmail, password, text="testing text", images=None
               ):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = Chrome(
        ChromeDriverManager().install(),
    )

    register(driver, gmail, password)

    while True:

        if not filteredQueue.empty():

            link = filteredQueue.get()

            print(link)

            if isinstance(link, list):
                for link in link:
                    propose_post(driver, link, text, images)
            else:
                propose_post(driver, link, text, images)
            sleep(2)

        else:
            sleep(0.5)


def main():

    processes = []

    filteredQueue = Queue()

    gmail = 'testingmak390@gmail.com'

    password = 'testing1!'

    text = "testing text"

    images = [r'D:\Мои документы\Изображения\real shit man\Портрет_агронома_М.Е._Вьюнникова.jpg']
    
    # processes.append(Process(target=get_public_links, args=(urlsQueue, filteredQueue)))
    processes.append(Process(target=filter_public_links, args=(filteredQueue, gmail, password)))
    processes.append(Process(target=main_posts, args=(filteredQueue, gmail, password, text, images)))

    for pr in processes:
        pr.start()
        sleep(10)


if __name__ == '__main__':
    main()