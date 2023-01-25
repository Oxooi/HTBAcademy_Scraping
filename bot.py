#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Import the required modules
from bs4 import BeautifulSoup as bs
import requests
import os

# Create a class to store all the functions
class scrapLinks():
    # Create a constructor to store the variables
    def __init__(self, url, file, cookies, links, inte):
        self.url = url
        self.file = file
        self.cookies = cookies
        self.links = links
        self.inte = inte

    # Create a function to get the content of the page
    def get(self):
        r = requests.get(self.url, cookies=self.cookies)
        soup = bs(r.content, 'html.parser')
        return soup

    # Create a function to get the title of the page
    def get_title(self):
        title = self.get().title.get_text()
        return title

    # Create a function to make a folder with the title of the page
    def make_folder(self):
        title = self.get_title()
        os.mkdir(title)
        return title

    # Create a function to get the list of all the links (In the sidebar (Table of contents)))
    def get_list(self):
        # Get the list of all the links inside the div tag with id TOC
        data = self.get().find('div', {'id': 'TOC'}).find_all('a')
        # Get the list of all the links inside the href attribute
        links = [link.get('href') for link in data]
        # Save into a file
        with open(self.file, 'w') as f:
            for link in links:
                f.write(link + '\n')
        return links

    # Create a function to get the content of the page
    def get_content(self):
        # Get the first h1 tag inside the div tag with class training-module
        title = self.get().find(
            'div', {'class': 'training-module'}).find('h1').text

        # Get the content of the page
        data = self.get().find('div', {'class': 'training-module'})
        # Keep only the content inside the div tag with class training-module
        final = data.decode_contents()

        # Save into a different file with a incrementing number
        with open(f'{self.inte}_{title}.md', 'w') as f:
            f.write(final)

        return title, final

if __name__ == '__main__':
    
    # Change the url to the url of the page you want to scrape
    url = 'https://academy.hackthebox.com/module/...'
    # Change the file name to whatever you want
    file = 'links.txt'
    # Change the cookies to the cookies of the website you want to scrape
    cookies = {"",""}
    # Create an empty list
    links = []
    # Create an integer to increment with every loop for indexing the files
    inte = 1

# Make a folder with the title of the page if it doesn't exist
    if os.path.exists(scrapLinks(url, file, cookies, links, inte).get_title()):
        # Change the directory to the folder with the title of the page
        os.chdir(scrapLinks(url, file, cookies, links, inte).get_title())
    else:
        # Make a folder with the title of the page
        os.mkdir(scrapLinks(url, file, cookies, links, inte).make_folder())
        
    # Get the list of all the links
    links = scrapLinks(url, file, cookies, links, inte).get_list()
    # Get the content of all the links
    for link in links:
        print(f"[+] Getting content of {link}")
        # Get the content of the page
        scrapLinks(link, file, cookies, links, inte).get_content()
        # Increase the inte number with every loop
        inte += 1
    
    # Delete the file with the list of links
    os.remove(file)

    print("[+] Done")