from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import pdb

def get_jobs(num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=%22Data%20Analyst%22&clickSource=searchBox&locId=1&locT=N&locName=United%20States'
    driver.get(url)
    jobs = []
 
    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.    

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        job_buttons=driver.find_elements(By.CSS_SELECTOR, ".css-1kjejvf.eigr9kq3")
        
        for job_button in job_buttons:  
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            try: 
                driver.execute_script("arguments[0].click();", job_button)
                # job_button.click() 
            except Exception as err:
                pass
            
            #Test for the "Sign Up" prompt and get rid of it.
            try:
                driver.find_element(By.CSS_SELECTOR, '#JAModal > div > div.modal_main.jaCreateAccountModalWrapper.gdGrid > span > svg').click() 
            except NoSuchElementException:
                pass

            #Skip
            if bool(driver.find_elements(By.CSS_SELECTOR, '#JDCol > div > div.css-17bh0pp.erj00if0 > h3')) == True:
                continue
            else:
                pass

            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.CSS_SELECTOR, '#JDCol > div > article > div > div:nth-child(1) > div > div > div.css-vwxtm.evnfo7p1 > div.css-19txzrf.e14vl8nk0 > div.css-w04er4.e1tk4kwz6 > div.d-flex.justify-content-between').text.split('\n')[0]
                    location = driver.find_element(By.CLASS_NAME, "css-56kyx5.e1tk4kwz5").text
                    job_title = driver.find_element(By.CLASS_NAME, "css-1vg6q84.e1tk4kwz4").text
                    job_description = driver.find_element(By.CLASS_NAME, "jobDescriptionContent").text
                    collected_successfully = True
                except Exception as err:
                    print("ERROR BRO: ", err.msg)
                    time.sleep(3)
            
            if bool(driver.find_elements(By.CLASS_NAME, "css-1bluz6i.e2u4hf13")) == True:
                salary_estimate = driver.find_element(By.CLASS_NAME, "css-1bluz6i.e2u4hf13").text
            else:
                continue

            try:
                rating = driver.find_element(By.CLASS_NAME, "css-1m5m32b.e1tk4kwz2").text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            company_overview = {element.text.split('\n')[0]: element.text.split('\n')[1] for element in driver.find_elements(By.CSS_SELECTOR, '.css-rmzuhb.e1pvx6aw0')}

            if company_overview.get("Size") is not None:
                size = company_overview['Size']
            else:
                size = -1

            if company_overview.get("Founded") is not None:
                founded = company_overview['Founded']
            else:
                founded = -1

            if company_overview.get("Type") is not None:
                type_of_ownership = company_overview['Type']
            else:
                type_of_ownership = -1

            if company_overview.get("Industry") is not None:
                industry = company_overview['Industry']
            else:
                industry = -1

            if company_overview.get("Sector") is not None:
                sector = company_overview['Sector']
            else:
                sector = -1
            
            if company_overview.get("Revenue") is not None:
                revenue = company_overview['Revenue']
            else:
                revenue = -1                          

            if verbose:
                if len(driver.find_elements(By.CSS_SELECTOR, '.css-rmzuhb.e1pvx6aw0')) == 0:
                    print("Size: {}".format(size))
                    print("Founded: {}".format(founded))
                    print("Type of Ownership: {}".format(type_of_ownership))
                    print("Industry: {}".format(industry))
                    print("Sector: {}".format(sector))
                    print("Revenue: {}".format(revenue))
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            #add job to jobs


        time.sleep(1)
        #Clicking on the "next page" button
        try:
            np= driver.find_element(By.XPATH, '//*[@id="MainCol"]/div[2]/div/div[1]/button[7]')
            driver.execute_script("arguments[0].click();", np)
            # driver.find_element(By.XPATH, '//*[@id="MainCol"]/div[2]/div/div[1]/button[7]').click()
            time.sleep(1)
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break
        
    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
