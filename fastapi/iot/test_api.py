import requests

url = "http://localhost:8000/api/getAll"

# The client should pass the API key in the headers
headers = {
  'Content-Type': 'application/json',
  'X-API-KEY': '12345678'
}

response = requests.get(url, headers=headers)
print(response.text)