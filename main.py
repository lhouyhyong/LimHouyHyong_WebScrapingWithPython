import requests
from bs4 import BeautifulSoup
import json

# 1. Scrape the pickup lines

url = "https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


# Create dictionary to store data
pickup_lines_dict = {}


headings = soup.findAll("h2")
for heading in headings:
    title = heading.text.strip()
    pickup_lines = []

    # Find the sibling <ul> element containing the pickup lines
    ul_element = heading.find_next_sibling("ul")

    if ul_element:
        # Find all <li> elements within the <ul> element
        li_elements = ul_element.findAll("li")

        # Extract the pickup lines from the <li> elements
        for li in li_elements:
            pickup_line = li.text.strip()
            pickup_lines.append(pickup_line)

        pickup_lines_dict[title] = pickup_lines
    else:
        pickup_lines_dict[title] = []


# save to json file
with open("pickup_lines.json", "w") as json_file:
    json.dump(pickup_lines_dict, json_file, indent=4)