from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
from typing import List
import pandas as pd

def get_links(URL, job_keyword, webdriver):
    """
    Using Selenium, gets a list of linkedin jobs from an URL. Returns the list

    Parameters
    ----------
    URL : str
        the linkedin jobs URL
    job_keyword : str
        the job keyword to search for
    webdriver : selenium.webdriver.abc.ABCMeta
        the selenium webdriver object

    Return
    ------
    list
        list containing the url for each job
    """
    # Opening the page
    driver.get(URL)
    time.sleep(2)

    # Removing the location filter
    fechar_loc = driver.find_element(By.XPATH, '/html/body/main/section[1]/div/section/div[2]/section[2]/form/section[2]/button')
    driver.execute_script('arguments[0].click();', fechar_loc)
    time.sleep(2)

    # Inserting the keyword for the job search
    inserir_vaga = driver.find_element(By.NAME, 'keywords')
    inserir_vaga.send_keys(job_keyword)
    time.sleep(2)

    # Clicking on "Pesquisar vagas"
    pesquisar_vagas = driver.find_element(By.XPATH, '/html/body/main/section[1]/div/section/div[2]/button[2]')
    driver.execute_script('arguments[0].click();', pesquisar_vagas)
    time.sleep(2)

    # TODO: test how this impacts the solution (are jobs preloaded or must we actually load them)
    # Now let's scroll over the page until we get "Carregar mais vagas" button
    for i in range(10):
        driver.find_element(By.CSS_SELECTOR,'body').send_keys(Keys.CONTROL, Keys.END)
        time.sleep(2)

    new_url = driver.current_url

    # Now let's call Beautiful Soup to help us
    req = requests.get(new_url)
    soup = bs(req.content)

    # Getting all job links that appears on the html
    jobs_info = soup.select('[class~=base-card__full-link]')
    links = [info.get('href') for info in jobs_info]

    return links


def links_to_df(job_keyword : str, links : List[str], filter : List[str] = ['', '\n', '\xa0', ' ']) -> pd.DataFrame:
    """
    Turns a list of linkedin jobs links to a pandas DataFrame that looks like:
    
    { 
      'Keyword': 'keyword',
      'Title': 'title',
      'Company name': 'company_name',
      'Location': 'location',
      'Description': 'description',
      'Job link': 'link'
    }
    
    Returns the DataFrame.

    Parameters
    ----------
    job_keyword : str
        the keyword to search jobs on linkedin
    links : List(str)
        list of urls
    filter : List(str)
        List of filters for each line of the job description

    Return
    ----------
    pd.DataFrame
        DataFrame with the jobs and the characteristics
    """
    list_of_dicts = []

    for i in range(len(links)):
        
        r = requests.get(links[i])
        s = bs(r.content)

        body = s.find('body')
        try:
            job_title = body.find(class_='sub-nav-cta__header').get_text(strip=True)
            company_name = body.find(class_='sub-nav-cta__optional-url').get('title')
            job_location = body.find(class_='sub-nav-cta__meta-text').get_text(strip=True)
            details = body.find('div', {'class': 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5'})

            paragraphs_list = []
            for child in details.children:
                paragraphs_list.append(child.text)

        except:
            job_title = None
            company_name = None
            job_location = None
            
        # Filtering the list
        filter_list = ['', '\n', '\xa0', ' ']
        filtered_list = [item for item in paragraphs_list if not item in filter_list]

        job_dict = {
        'Keyword': job_keyword,
        'Title': job_title,
        'Company name': company_name,
        'Location': job_location,
        'Description': '\n'.join(filtered_list),
        'Job link': links[i]
        }
        
        list_of_dicts.append(job_dict)

    # Finally, let's transform these list elements into one big dataframe

    df_list = [pd.DataFrame(list_of_dicts[i], index=[i]) for i in range(len(list_of_dicts))]

    jobs_dataframe = pd.concat(df_list)
    jobs_dataframe = jobs_dataframe.rename(columns={
        'Keyword': 'keyword',
        'Title': 'title',
        'Company name': 'company_name',
        'Location': 'location',
        'Description': 'description',
        'Job link': 'link'}
        )
    
    return jobs_dataframe
