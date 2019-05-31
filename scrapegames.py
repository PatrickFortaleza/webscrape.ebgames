import bs4
import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver


my_url = 'https://www.ebgames.ca/SearchResult/QuickSearch?strokenPrice=Recent%20Drop&typeSorting=4&sDirection=Descending#group31'
# uClient = uReq(my_url)
# page_html = uClient.read()
# uClient.close()
browser = webdriver.Chrome()
browser.get(my_url)


last_height = browser.execute_script("return document.body.scrollHeight")
SCROLL_PAUSE_TIME = 0.5

while True:

    # Get scroll height
    ### This is the difference. Moving this *inside* the loop
    ### means that it checks if scrollTo is still scrolling 
    last_height = browser.execute_script("return document.body.scrollHeight")

    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:

        # try again (can be removed)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")

        # check if the page height has remained the same
        if new_height == last_height:
            # if so, you are done
            break
        # if not, move on to the next loop
        else:
            last_height = new_height
            continue

innerHTML = browser.execute_script("window.scrollTo(0, document.body.scrollHeight-10000);var lenOfPage=document.body.scrollHeight;return document.body.innerHTML;")

# Parse HTML
page_soup = soup(innerHTML,"html.parser")

filename = "games.csv"
f = open(filename,"w")

headers = "Game Title, Console, Discount Price, Retail Price, Release Date, Discount Rating\n"

#Grabs Each Product
containers = page_soup.findAll("div",{'class':'singleProduct'})

f.write(headers)

for container in containers:
    deal_status = ''

    #Grab the game title
    game_title = container.div.h3.a.text

    #Grab the game console
    game_console = container.div.h4.text
    game_console = game_console.split(' ')[0]

    #Grab the discount price
    try:
        price_container = container.find("p", {'class': 'buyNew'}).a.span.text
        price_container = price_container.strip().split('\n')[1]
        price_container = float(price_container.replace('$',''))
    except Exception as e:
        price_container = container.find("p", {'class': 'buyUsed'}).a.span.text
        price_container = price_container.strip().split('\n')[1]
        price_container = float(price_container.replace('$',''))

    #Grab the retail price
    try: 
        price_container2 = container.find("p", {'class': 'buyNew'}).a.span.text
        price_container2 = price_container2.strip().split('\n')[2]
        price_container2 = float(price_container2.replace('$',''))
    except Exception as e:
        price_container2 = price_container

    #Grab the release date
    release_date = container.div.ul.li.text
    release_date = release_date.split(' ')[2]

    #Rate the deal status
    the_discount = ((price_container2 - price_container)/price_container2)*100

    if the_discount == 0:
        deal_status = 'Used Game'
    elif the_discount <= 10:
        deal_status = 'Average Discount'
    elif the_discount > 10 and the_discount < 25:
        deal_status = 'Decent Discount'
    elif the_discount > 25 and the_discount < 50:
        deal_status = 'Good Discount'
    elif the_discount >= 50:
        deal_status = 'Great Discount'
    else:
        deal_status = 'Error Calculating Deal Status'

    print('\n')
    print("Game Title:\n" + game_title )
    print("Console:\n" + game_console)
    print("Discount Price:\n" + str(price_container))
    print("Retail Price:\n" + str(price_container2))
    print("Release Date:\n" + release_date)
    print("Deal Status:\n" + deal_status)

    f.write(game_title + "," + game_console + "," + str(price_container) + "," + str(price_container2) + "," + release_date + "," + deal_status + "\n")

f.close()
