import requests
import pandas as pd

####
# Export purchase items for Formaviva for Michel 
###

# Insert your OAuth bearer user token
user_token = ""

# URL and headers for the request
url = "https://api.formaviva.com/api/v1/purchases?filter%5Bitem_type%5D=all&page=1&per_page=200&sales=true&sort=--created_at"
headers = {
    'Referer': 'https://formaviva.com/',
    'Authorization': 'Bearer ' + user_token
}

# List of allowed Formaviva attributes
allowed_attributes = [
    "purchase_id",
    "description",
    "quantity",
    "price",
    "total",
    "vat",
    "revenue_share",
    "subtotal",
    "status",
    "digital"
]

# Make the GET request to Formaviva endpoint
response = requests.get(url, headers=headers)
def filter_data(input_data, allowed_attributes):
  output_data = {}
  for key, value in input_data.items():
    if key in allowed_attributes:
      output_data[key] = value
  return output_data

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    json = response.json()
    data = json['data']

    items = [item for item in json['included'] if item['type'] == 'purchase_items']

    relevant_items = []
    for item in items:
      for purchase in data:
        if int(item['attributes']['purchase_id']) == int(purchase['id']):
            attributes = filter_data(item['attributes'], allowed_attributes)
            relevant_items.append(attributes)

    # Create DataFrame and save to CSV
    df = pd.DataFrame(relevant_items)
    df.to_csv('report.csv', index=False)
else:
    print(f"Failed to fetch data: Status code {response.status_code}")
