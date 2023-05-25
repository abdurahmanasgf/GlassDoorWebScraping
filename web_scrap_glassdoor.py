from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import pdb

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        # try:
        #     driver.find_element(By.NAME, "selected").click()
        # except ElementClickInterceptedException:
        #     pass

        # time.sleep(.1)

        # try:
        #     driver.find_element(By.NAME, "ModalStyle__xBtn___29PT9").click()  #clicking to the X.
        # except NoSuchElementException:
        #     pass
#MainCol > div:nth-child(1) > ul
        
        #MainCol > div:nth-child(1) > ul
        #JAModal > div > div.modal_main.jaCreateAccountModalWrapper.gdGrid > span > svg
        #Going through each job in this page
        # job_buttons = driver.find_element(By.CSS_SELECTOR, "#MainCol > div:nth-child(1) > ul").find_elements(By.CSS_SELECTOR, "*")  #jl for Job Listing. These are the buttons we're going to click.
        job_buttons=driver.find_elements(By.CSS_SELECTOR, ".css-1kjejvf.eigr9kq3")
        
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            try: 
                driver.execute_script("arguments[0].click();", job_button)
                # job_button.click() 
            except Exception as err:
                pdb.set_trace()
                pass
            try:
                driver.find_element(By.CSS_SELECTOR, '#JAModal > div > div.modal_main.jaCreateAccountModalWrapper.gdGrid > span > svg').click() 
            except NoSuchElementException:
                pass
            
            time.sleep(.1)


            time.sleep(.1)

            collected_successfully = False

            while not collected_successfully:
                try:
                    # driver.find_elements(By.CSS_SELECTOR, ".css-1kjejvf.eigr9kq3")[1].find_element(By.CSS_SELECTOR, ".job-title.mt-xsm")
                    company_name = driver.find_element(By.CLASS_NAME, "css-87uc0g.e1tk4kwz1").text.split("\n")[0]
                    location = driver.find_element(By.CLASS_NAME, "css-56kyx5.e1tk4kwz5").text
                    job_title = driver.find_element(By.CLASS_NAME, "css-1vg6q84.e1tk4kwz4").text
                    job_description = driver.find_element(By.CLASS_NAME, "jobDescriptionContent").text
                    collected_successfully = True
                except Exception as err:
                    pdb.set_trace()
                    print("ERROR BRO: ", err.msg)
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element(By.CLASS_NAME, "css-1bluz6i.e2u4hf13").text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."

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
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            
            try:
                size = driver.find_element(By.XPATH, '//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]').text
            except NoSuchElementException:
                size = -1

            try:
                founded = driver.find_element(By.XPATH, '//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]').text
            except NoSuchElementException:
                founded = -1

            try:
                type_of_ownership = driver.find_element(By.XPATH,'//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]').text
            except NoSuchElementException:
                type_of_ownership = -1

            try:
                industry = driver.find_element(By.XPATH,'//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]').text
            except NoSuchElementException:
                industry = -1


            try:
                sector = driver.find_element(By.XPATH,'//*[@id="EmpBasicInfo"]/div[1]/div/div[5]/span[2]').text
            except NoSuchElementException:
                sector = -1

            try:
                revenue = driver.find_element(By.XPATH,'//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]').text
            except NoSuchElementException:
                revenue = -1


            if verbose:
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

        #Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH,'.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
