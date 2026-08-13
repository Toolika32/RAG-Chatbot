import requests
from bs4 import BeautifulSoup

url = "https://kyloresort.com/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary elements
    for element in soup(["script", "style", "nav", "footer"]):
        element.decompose()

    # Extract visible text
    text = soup.get_text(separator="\n", strip=True)

    # Save the text
    with open("Knowledge based/webscraping.txt", "w", encoding="utf-8") as file:
        file.write(text)

    print("Website scraped successfully!")

else:
    print("Failed to access website.")
    print("Status code:", response.status_code)