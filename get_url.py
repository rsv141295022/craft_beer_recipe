import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import concurrent.futures

def stop(time_sleep):
    time.sleep(np.random.rand() + time_sleep)

def get_recipe_url_in_page(url):
    driver = webdriver.Chrome()
    driver.get(url) # main_url + '2/'
    all_article_page_path = '/html/body/div[1]/strong/strong/div[1]/div/main/div[1]/article'
    articles = driver.find_elements(By.XPATH, all_article_page_path)
    all_recipe = []
    for i in range(len(articles)):
        article_path = all_article_page_path + f'[{1+i}]'
        style_path = article_path + '/div/a'
        name_recipe_path = article_path + '/div/header/p/a'
        final_results_path = article_path + '/div/div[1]/p'
        
        style_elem = driver.find_element(By.XPATH, style_path)
        style_text = style_elem.text
        name_elem = driver.find_element(By.XPATH, name_recipe_path)
        name_text = name_elem.text
        url_recipe = name_elem.get_attribute("href")
        final_result_text = [t.text for t in driver.find_elements(By.XPATH, final_results_path)]
        
        all_recipe.append([style_text, name_text, final_result_text, url_recipe])
    return all_recipe

if __name__ == '__main__':
    main_url = 'https://www.homebrewersassociation.org/beer-recipes/pro-clone-homebrew-recipes/'
    all_url = [main_url + f'page/{i}/' for i in range(2,16)]
    all_url.insert(0, main_url)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [executor.submit(get_recipe_url_in_page, url) for url in all_url]

        # Wait for all tasks to complete
        completed_futures, _ = concurrent.futures.wait(futures)

        # Get results in the order they were submitted
        all_url = []
        for future in futures:
            result = future.result()
            # print(f"Result: {result}")
            all_url.extend(result)
        
    df = pd.DataFrame(all_url, columns=['style', 'beer_name', 'final_results', 'url'])
    filename = input('fill your filename: ')
    df.to_csv(fr'C:\Users\y.patcharapol\OneDrive - Trans-cosmos (Thailand) Co.,Ltd\Desktop\Python\Beer\{filename}.csv')