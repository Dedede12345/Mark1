from multiprocessing import Process, Queue
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep, time
from mark.operations import get_links_queue, register, propose_post, clean_queue, choose_images, greetings_and_creation, get_links_json
from mark.common import Prerequisites
from os.path import exists

start = time()

visited = []

def basic_links(post, filteredQueue):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = Chrome(
        ChromeDriverManager().install(),
    )

    register(driver, post.gmail, post.password)
    get_links_queue(driver, filteredQueue)
    driver.close()

def filter_public_links(filteredQueue, post):

    if not exists('datafile.json'):
        basic_links(post, filteredQueue)

    else:
        while True:
            try:
                if line:=input(f"Do you want to use previously used links? [y/n]") == 'y':
                    get_links_json(filteredQueue)
                    break
                elif line == 'n':
                    basic_links(post, filteredQueue)
                    break
                else:
                    continue
            except EOFError:
                break




def main_posts(filteredQueue: Queue, post):

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = Chrome(
        ChromeDriverManager().install(),
    )

    register(driver, post.gmail, post.password)


    while True:


        if not filteredQueue.empty():

            # links = []

            links = filteredQueue.get()

            # links.extend(filteredQueue.get())


            if isinstance(links, list):
                # links = [link for link in links if link not in visited]
                for link in links:
                    # visited.append(link)
                    propose_post(driver, link, post.text, post.images)

                    try:
                        if filteredQueue.empty(): # Check here, for queue type
                            print("First")
                            driver.close()
                            break
                    except ValueError:
                        pass
            else:
                propose_post(driver, links, post.text, post.images)
                if filteredQueue.empty():
                    print("Second")
                    driver.close()
                    break

            sleep(2)

        else:
            sleep(0.5)


def main():

    processes = []

    filteredQueue = Queue()

    gmail = 'testingmak390@gmail.com'

    password = 'testing1!'

    text = "testing text"
    post = Prerequisites(gmail, password, text)
    # images = [r'D:\Мои документы\Изображения\real shit man\Портрет_агронома_М.Е._Вьюнникова.jpg']
    # post = greetings_and_creation()
    #
    # choose_images(post)
    
    # processes.append(Process(target=filter_public_links_test, args=(rawQueue, gmail, password)))
    # processes.append(Process(target=clean_queue, args=(rawQueue, filteredQueue)))

    finding_Dory = Process(target=filter_public_links, args=(filteredQueue, post))
    finding_Dory.start()

    for _ in range(int(input("Enter number of bot-tabs to open (2 is recommended): "))):
        processes.append(Process(target=main_posts, args=(filteredQueue, post)))

    # processes.append(Process(target=main_posts, args=(filteredQueue, post)))
    # processes.append(Process(target=main_posts, args=(filteredQueue, post)))

    while finding_Dory.is_alive():
        sleep(0.5)


    for pr in processes:
        pr.start()
        sleep(15)

    while True:

        if not processes:
            print(f"Total time: {time() - start}")
            break

        for pr in processes:
            if not pr.is_alive():
                processes.remove(pr)


    # for pr in processes:
    #     pr.terminate()
    #     pr.close()

if __name__ == '__main__':
    main()
