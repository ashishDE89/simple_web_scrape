import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['mongo_trial']  # Replace with your MongoDB database name
collection = db['mongo_trial']  # Replace with your MongoDB collection name

# Make a GET request to the website
url = 'https://www.bafu.admin.ch/bafu/en/home/topics/air/state/data/air-pollution--real-time-data/table-of-the-current-situation-nabel.html'
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table element
table = soup.find('table')

# Extract the table headers
headers = [th.text.strip() for th in table.find_all('th')]

# Extract the table rows
rows = []
for tr in table.find_all('tr'):
    row = [td.text.strip() for td in tr.find_all('td')]
    if row:
        rows.append(row)

# Create a list of dictionaries representing each row
data = []
for row in rows:
    data.append(dict(zip(headers, row)))

# Insert the data into MongoDB
collection.insert_many(data)

# Disconnect from MongoDB
client.close()
