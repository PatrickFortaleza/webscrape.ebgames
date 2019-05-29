import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.ebgames.ca/SearchResult/QuickSearch?strokenPrice=Recent%20Drop&typeSorting=4&sDirection=Descending#group21'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# Parse HTML
page_soup = soup(page_html,"html.parser")

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
    price_container = container.find("p", {'class': 'buyNew'}).a.span.text
    price_container = price_container.strip().split('\n')[1]
    price_container = float(price_container.replace('$',''))

    #Grab the retail price
    price_container2 = container.find("p", {'class': 'buyNew'}).a.span.text
    price_container2 = price_container2.strip().split('\n')[2]
    price_container2 = float(price_container2.replace('$',''))

    #Grab the release date
    release_date = container.div.ul.li.text
    release_date = release_date.split(' ')[2]

    #Rate the deal status
    the_discount = 3 #((price_container2 - price_container)/price_container2)*100

    if the_discount <= 10:
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
