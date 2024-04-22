import requests
import bs4
import pandas
res = requests.get("https://store.steampowered.com//")
soup = bs4.BeautifulSoup(res.text, "lxml")

# Gathering User Input
TagInput = input("Choose a genre or leave it blank for any genre (Singleplayer, Open World, RPG, Multiplayer, MOBA or Adventure): ")
PriceInput = input("Insert a price range using the max price as the input or leave it blank for all prices ('10' for games $10 and below or 'Free' for free games): ")

# get the topseller games
topsellers = soup.select("#tab_topsellers_content a.tab_item")

# create csv file
f = open("SteamTopGamesPy.csv", "w")

# header row of the csv file
f.write("Rank, Title, Price, Tags\n")

# iteration of topseller game details
for Rank, container in enumerate(topsellers, start=1):
    Title_element = container.select(".tab_item_name")
    FinalPrice_element = container.select(".discount_final_price")
    Tags_element = container.select(".tab_item_top_tags")

    # Check if all elements are present before accessing them
    if Title_element and FinalPrice_element and Tags_element:
        Title = Title_element[0].text.strip()
        FinalPrice = FinalPrice_element[0].text.strip()
        Tags = Tags_element[0].text.strip()

        # Use user input in order to sort tags. Entering nothing includes all tags
    if FinalPrice == "Free to Play":
        FinalPrice = "$0.00"
    if FinalPrice == "Free To Play":
        FinalPrice = "$0.00"
    if FinalPrice == "Free":
        FinalPrice = "$0.00"

    PriceInputFloat = float(PriceInput)
    if float(FinalPrice.replace("$", "")) <= PriceInputFloat:
        if TagInput.lower() in Tags.lower():
            f.write(f"{Rank}, {Title}, {FinalPrice.replace(',', '.')}, {Tags.replace(',', '.')}\n")
        else:
            if TagInput.lower() in Tags.lower():
                f.write(f"{Rank}, {Title}, {FinalPrice.replace(',', '.')}, {Tags.replace(',', '.')}\n")
        
    else:
        print(f"Missing element in container {Rank}")

# close the csv file
f.close()

# Read and print the CSV file
reading = pandas.read_csv("SteamTopGamesPy.csv")
print(reading)