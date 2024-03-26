import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

# Fetch HTML content
url = "https://www.mtsdvorana.rs/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all div elements with class "movie-item"
movie_items = soup.find_all('div', class_='movie-item')

# Create RSS feed
fg = FeedGenerator()
fg.title('Movie Feed')
fg.link(href=url, rel='alternate')
fg.description('RSS feed for movies')

# Loop through each movie item and add it to the feed
for movie_item in movie_items:
    title_element = movie_item.find('h2', class_='movie-item-title')
    if title_element:
        title = title_element.text.strip()
        link = title_element.find('a')['href']
    else:
        title = "Title Not Available"
        link = "Link Not Available"

    image_element = movie_item.find('a', class_='movie-item-image')
    if image_element:
        image_url = image_element.find('img')['src']
    else:
        image_url = "Image URL Not Available"

    # Create an entry for each movie
    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=link)
    fe.enclosure(image_url, 0, 'image/jpeg')  # Add image as enclosure

# Generate the RSS feed
rss_feed = fg.rss_str(pretty=True)

# Save the RSS feed to a file
with open('movie_feed.xml', 'wb') as f:  # Open file in binary mode
    f.write(rss_feed)


print("RSS feed generated successfully.")
