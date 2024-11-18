# importing libraries

from typing import ItemsView
from pandas.core.frame import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import requests
import os

keywords = ["sweater","sweater pattern","knitting pattern"]


# creating the function to scrape link of images to be downloaded

def search_google(search_query):
    
    # breaking the name down
    
    converted_name = search_query.lower().replace(" ", "_")
    
    data_dic = {
                "Keyword":[],
                "Image Link":[]
               }
    
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"

    browser = webdriver.Chrome()

    # Open browser to begin search
    browser.get(search_url)
    
    # Maximize the window
    browser.maximize_window()
    
    time.sleep(3)
    
    count = 0
    
    for i in range(0,300):
        
        count += 1
        
        #click the picture
    
        img_box = browser.find_elements(By.CSS_SELECTOR,'div.fR600b')[i]
        
        try:
            img_box.click()
        

            time.sleep(5)
        
            # extract the link
        
        
            img_box_2 = browser.find_elements(By.CSS_SELECTOR,'div.p7sI2')[1]

            link = img_box_2.find_elements(By.TAG_NAME,'img')[0].get_attribute('src')
            
        except:
            
            # if the click gets interecepted
            
            try:
            
                browser.execute_script("window.scrollBy(0, 100);")

                time.sleep(2)

                img_box.click()


                time.sleep(5)

                # extract the link


                img_box_2 = browser.find_elements(By.CSS_SELECTOR,'div.p7sI2')[1]

                link = img_box_2.find_elements(By.TAG_NAME,'img')[0].get_attribute('src')
                
            except:
                
                pass

        # append to a dictionary
        
        
        data_dic["Keyword"].append(keyword)
        data_dic["Image Link"].append(link)
     
    # export the dictionary to an excel
        
        if count % 20 == 0:
    
            df = pd.DataFrame(data=data_dic)

            df.to_excel(f'excel_links/{converted_name}_links.xlsx', index=False)
            
            print(f"Downloaded {count} images of {search_query}")
    

    
    browser.close()
    
    
# running the seach function that we created above through the keywords

for keyword in keywords:
    print(f"Downloading Images of {keyword}")
    search_google(keyword)
    
# creating the function that saves images

def download_images(url,count,query):

    try:
    
        img_data = requests.get(url).content
        with open(f'raw_images/{query}/{query}_{count}.jpg', 'wb') as handler:
            handler.write(img_data)
    
    
    except Exception as e: 
        
        pass
 
 
# creating folders to save the images

# Specify the path where you want to create the folders
path = "google_images/"

# List of folder names you want to create
folders = [name.lower().replace(" ", "_") for name in keywords]

# Iterate over the list of folder names and create them
for folder in folders:
    folder_path = os.path.join(path, folder)
    os.makedirs(folder_path, exist_ok=True)  # exist_ok=True prevents an error if the folder already exists
    print(f"Folder '{folder}' created at {folder_path}")
    
 
 
 
# Importing the previously exported file (with links) and running a loop through the download_images function


query_list = [name.lower().replace(" ", "_") for name in keywords]

for query in query_list:

    
    url_data = pd.read_excel(f'excel_links/{query}_links.xlsx')

    #create a list of the urls

    url_list = list(url_data['Image Link'])

    # create a list for the number of images

    image_count = list(range(0,300))

    # create a list for the queries
    

    # download all images from the links

    for (i,f) in zip(url_list,image_count):

        download_images(i,f,query)
        
    print(f"Successfully saved images of {query}")