import requests
import bs4
import pandas
res = requests.get("https://store.steampowered.com//")
soup = bs4.BeautifulSoup(res.text, "lxml")

# Gathering User Input
TagInput = input("Choose a genre or leave it blank for any genre (Singleplayer, Open World, RPG, Multiplayer, MOBA or Adventure): ")
PriceInput = input("Insert a price range using the max price as the input or leave it blank for all prices ('10' for games $10 and below or 'Free' for free games): ")

# get the topseller games from team
topsellers = soup.select("#tab_topsellers_content a.tab_item")

# create csv file
f = open("SteamTopGamesPy.csv", "w")

# creates header row of the csv file
f.write("Title, Price, Tags\n")

# iterates through the topseller game details
for Rank, container in enumerate(topsellers, start=1):
    Title_element = container.select(".tab_item_name")
    FinalPrice_element = container.select(".discount_final_price")
    Tags_element = container.select(".tab_item_top_tags")

    # Check if all elements are present before accessing them
    if Title_element and FinalPrice_element and Tags_element:
        Title = Title_element[0].text.strip()
        FinalPrice = FinalPrice_element[0].text.strip()
        Tags = Tags_element[0].text.strip()

    # Converts Free to play string to floats in order to match steam's pricing format
    if FinalPrice == "Free to Play":
        FinalPrice = "$0.00"
    if FinalPrice == "Free To Play":
        FinalPrice = "$0.00"
    if FinalPrice == "Free":
        FinalPrice = "$0.00"
    #Skips the Steam Deck
    if Title == "Steam Deck":
        continue

    # Converts user input to a float in order to match the steam price format in order to sort steam's prices by user input
    if PriceInput:
            PriceInputFloat = float(PriceInput)
            if float(FinalPrice.replace("$", "")) <= PriceInputFloat:
                if TagInput.lower() in Tags.lower():
                    f.write(f"{Rank}, {Title}, {FinalPrice.replace(',', '.')}, {Tags.replace(',', '.')}\n")
    else:
        if TagInput.lower() in Tags.lower():
            f.write(f"{Title}, {FinalPrice.replace(',', '.')}, {Tags.replace(',', '.')}\n")
#If any element is missing, it will print this message

# close the csv file
f.close()

# Read and print the CSV file
reading = pandas.read_csv("SteamTopGamesPy.csv")
print(reading)