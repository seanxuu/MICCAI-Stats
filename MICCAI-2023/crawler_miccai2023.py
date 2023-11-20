import requests
from bs4 import BeautifulSoup
import csv
import re

BASE_URL = "https://conferences.miccai.org/2023/papers/"
OUTPUT_FILE = "papers_data.csv"

def get_paper_links():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    paper_links = []


    for link in soup.select(".posts-list-item-name a"):
        href = link.get('href')
        full_url = "https://conferences.miccai.org" + href
        paper_links.append((full_url, href))
    
    return paper_links


def extract_paper_data(url, href1):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.select_one('title').text

    parts = title.split('|')

    title=parts[0]
    abstract = soup.find(id="abstract-id").find_next('p').get_text(strip=True)


    code_link_tag = soup.find(id="code-id").find_next('p').find('a')
    if code_link_tag:
        code_link = code_link_tag.get('href')
    else:
        code_link = None  

    dataset_link_tag = soup.find(id="dataset-id").find_next('p').find('a')
    if dataset_link_tag:
        dataset_link = dataset_link_tag.get('href')
    else:
        dataset_link = None  

    print(dataset_link)

    categories = extract_categories(soup)
    
    return [title, abstract, code_link, dataset_link, categories]


def extract_categories(soup):
    category_tags = soup.select(".post-categories .post-category")
    

    def extract_key_part(category_str):
        return category_str.split("-", 1)[-1].strip()

    return [extract_key_part(tag.get_text()) for tag in category_tags]

def main():
    paper_links = get_paper_links()

    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        

        headers = ["Title", "Abstract", "Code Repository Link", "Dataset Link"]
        headers.extend([f"Category {i+1}" for i in range(10)])
        writer.writerow(headers)

        for full_url, href1 in paper_links:
            title, abstract, code_link, dataset_link, categories = extract_paper_data(full_url, href1)
            

            while len(categories) < 10:
                categories.append(None)

            data = [title, abstract, code_link, dataset_link] + categories
            
            writer.writerow(data)



if __name__ == "__main__":
    main()
