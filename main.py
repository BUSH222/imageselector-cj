import requests
import json
from PIL import Image
import os

def grab_image(keyword):
    url = f"https://loremflickr.com/1024/1024/{keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        image_link = response.url
        return image_link

def save_image_to_json(keyword, image_link):
    data = {}
    try:
        with open('images.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        pass

    if keyword in data:
        data[keyword].append(image_link)
    else:
        data[keyword] = [image_link]

    with open('images.json', 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
keyword = input("Enter a keyword: ")
while True:
    image_link = grab_image(keyword)
    try:
        image = Image.open(requests.get(image_link, stream=True).raw)
        image.save(os.getcwd()+"/tempimg.png")
    except Exception as e:
        print("Failed to display the image.")
    if image_link:
        answer = input(f"Does this image fit the keyword '{keyword}'? (yes/no): ")
        if answer.lower() == 'yes' or answer.lower() == 'y':
            save_image_to_json(keyword, image_link)
            print("Image link saved in images.json.")
        elif answer.lower() == 'no' or answer.lower() == 'n':
            print("Image not saved.")
        elif answer.lower() == 'keyword' or answer.lower() == 'kw':
            keyword = input("Enter a keyword: ")
        else:
            break

    else:
        print("Failed to grab the image.")