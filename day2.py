import requests
city = input("Enter the city name: ")
response = requests.get(f"https://wttr.in/{city}?format=3")
print(response.text)
print(response.status_code)