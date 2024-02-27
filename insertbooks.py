#!/usr/bin/python3

"""
    This module defines a function that creates book data from request data
    data contains another key 'publisher' that has keys 'id'
    and optionally 'name'. if 'name' is present,
    we need to create a new publisher
    if 'name' is not present, we need to find the publisher by 'id'
    data also contains another key 'authors'
    that has an array of objects with keys 'id' and optionally 'name'
    we need to iterate through the array and create new authors
    if 'name' is present and store the 'id' in an array
    if 'name' is not present, we need to append the 'id' to the array
    same for categories """
import json
import requests


def create_book_data(data):
    # Extract the required details
    title = data.get('title', None)
    description = data.get('description', None)
    image = data.get('image-url', None)
    isbn = data.get('isbn', None)
    price = data.get('price', None)
    numberOfPages = data.get('num_pages', None)
    publishDate = data.get('publish_date', None)
    publishers = [
        {
            'name': publisher
        } for publisher in data['publisher']
    ]
    edition = data.get('edition', None)
    categories = [
        {
            'name': category
        } for category in data['subjects']
    ]
    authors = [
        {
            'name': author['name']
        } for author in data['authors']
    ]
    return {
        'title': title,
        'description': description,
        'image': image,
        'isbn': isbn,
        'price': float(price),
        'publishers': publishers,
        'edition': edition,
        'authors': authors,
        'categories': categories,
        "unitsInStock": 45,
        "publish_date": publishDate,
        "numberOfPages": int(numberOfPages[0])
    }


api_url = "http://127.0.0.1:5002/api/v1/books"
if __name__ == "__main__":
    with open("final_v3.json", "r") as f:
        books = json.load(f)
        for book in books:
            book_data = create_book_data(book)
            # Post the book data to the API
            response = requests.post(api_url, json=book_data)
            if response.status_code == 201:
                print(f"Book with ISBN {book_data['isbn']} added successfully")
            elif response.status_code == 200:
                print(f"Existing book with ISBN {book_data['isbn']} updated successfully")
            else:
                print(f"Failed to add book with ISBN {book_data['isbn']}.Status code: {response.status_code}")

