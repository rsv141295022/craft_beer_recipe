import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import concurrent.futures

def stop(time_sleep):
    time.sleep(np.random.rand() + time_sleep)


def get_recipe(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        
        # get number time of brew
        try:
            elem = driver.find_element(By.ID, 'brew-number')
            brew_time = elem.text
        except:
            brew_time = []

        # get ingredients => try div(class="ingredients") => find_elements ==> ul
        try:
            li_elements = driver.find_elements(By.CLASS_NAME, "ingredients")
            ingredients = [elem.text for elem in li_elements]
        except:
            ingredients = []

        # get direction => try div(class="directions") => find_elements ==> p
        try:
            li_elements = driver.find_elements(By.CLASS_NAME, "directions")
            directions = [elem.text for elem in li_elements]
        except:
            directions = []

        # get direction => try div(class="recipe-additional") => find_elements ==> p
        try:
            li_elements = driver.find_elements(By.CLASS_NAME, "recipe-additional")
            recipe_additional = [elem.text for elem in li_elements]
        except:
            recipe_additional = []
            
        return url, brew_time, ingredients, directions, recipe_additional
    
    except:
        return url, [], [], [], []
    
if __name__ == '__main__':
    path = r'C:\Users\y.patcharapol\OneDrive - Trans-cosmos (Thailand) Co.,Ltd\Desktop\Python\Beer\pro_clone_url.csv'
    df = pd.read_csv(path)
    all_urls = df['url'].values[:]
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
    # Submit tasks to the executor
        futures = [executor.submit(get_recipe, url) for url in all_urls]

        # Wait for all tasks to complete
        completed_futures, _ = concurrent.futures.wait(futures)

        # Get results in the order they were submitted
        all_recipes = []
        for future in futures:
            result = future.result()
            # print(f"Result: {result}")
            all_recipes.extend([result])
            
    df = pd.DataFrame(all_recipes, columns=['url', 'brewtime', 'ingredients', 'directions', 'recipe_additional'])
    filename = input('fill your filename: ')
    df.to_csv(fr'C:\Users\y.patcharapol\OneDrive - Trans-cosmos (Thailand) Co.,Ltd\Desktop\Python\Beer\{filename}.csv')