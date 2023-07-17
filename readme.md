# Data Analyst Salary: Project Overview 
* Scraped over 100+ job descriptions from glassdoor using python and selenium
* Engineered features from the text of each job description to quantify the value companies put on python, excel, aws, and spark. 
* Optimized Linear, Lasso, and Random Forest Regressors using GridsearchCV to reach the best model. 

## Code and Resources Used 
**Python Version:** 3.7  
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, selenium
**For Web Framework Requirements:**  ```pip install -r requirements.txt```  
**Scraper Github:** https://github.com/arapfaik/scraping-glassdoor-selenium  
**Scraper Article:** https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905  
**Youtube Guide:** https://www.youtube.com/watch?v=MpF9HENQjDo&list=PL2zq7klxX5ASFejJj80ob9ZAnBHdz5O1t&index=1
**Flask Productionization:** https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2

## Web Scraping
Tweaked the web scraper GitHub repository (above) to scrape 100+ job postings from [here](https://www.glassdoor.com/Job/jobs.htm?sc.keyword=%22Data%20Analyst%22&clickSource=searchBox&locId=1&locT=N&locName=United%20States). With each job, we got the following:
*	Job title
*	Salary Estimate
*	Job Description
*	Rating
*	Company 
*	Location
*	Company Size
*	Company Founded Date
*	Type of Ownership 
*	Industry
*	Sector
*	Revenue

In essence, we'll create a Python script that will produce a DataFrame similar to this:

![alt text](https://github.com/abdurahmanasgf/GlassDoorWebScraping/blob/main/Dataframe.png)

Python code did the following job with the script that has been created, automatically scrolling down the web page and clicking on each job in all job listings and clicking on the different panels to receive another detail information about the company. When it has scraped until the end, it will move on to the next page. The end product will look like the following simulation of Google Chrome. There is no human contact and interaction because everything is automated.

![alt text](https://github.com/abdurahmanasgf/GlassDoorWebScraping/blob/main/ScrapingProcess.png)

The other problem while we scape the web page using python is in the middle oof the process, the sign-in panel will appear on the screen and it blocks Selenium from clicking anywhere else. The way we are dealing with this is that we click the X button and the searching process will become normal again.

![alt text](https://github.com/abdurahmanasgf/GlassDoorWebScraping/blob/main/Sign-in.png)

```python
#Test for the "Sign Up" prompt and get rid of it.

try:
  driver.find_element(By.CSS_SELECTOR, '#JAModal > div > div.modal_main.jaCreateAccountModalWrapper.gdGrid > span > svg').click() 
except NoSuchElementException:
  pass

```

Some of the work panels display blank space, making it impossible for us to get the data we need. Another Python code was built to identify that dark panel, return to skip that page next page and continue searching to the next panel to prevent the process from being stuck in the middle.

```python
#Skipping the blank panel

if bool(driver.find_elements(By.CSS_SELECTOR, '#JDCol > div > div.css-17bh0pp.erj00if0 > h3')) == True:
  continue
else:
  pass

```

You can access the complete Python code [here](https://www.google.com), if you were able to understand what we did above and have a basic knowledge of Python, you should be able to read the code with comments. The final point is that this GlassDoor website might be changed at any time, therefore it's likely that there will be a few minor adjustments over time because the code is only valid for the immediate future. Therefore, it is best for you to thoroughly comprehend HTML so that you can troubleshoot that issue.


## Data Cleaning
After scraping the data, I needed to clean it up to make it usable for our model. I made the following changes and created the following variables:

*	Parsed numeric data out of salary 
*	Made columns for employer-provided salary and hourly wages 
*	Removed rows without salary 
*	Parsed rating out of company text 
*	Made a new column for the company state 
*	Added a column for if the job was at the company’s headquarters 
*	Transformed the founded date into the age of the company 
*	Made columns for if different skills were listed in the job description:
    * Python  
    * R  
    * Excel  
    * AWS  
    * Spark 
*	Column for simplified job title and Seniority 
*	Column for description length 

## EDA
I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the pivot tables. 

![alt text](https://github.com/abdurahmanasgf/GlassDoorWebScraping/blob/main/Seniority.png "Salary by Position")

![alt text](https://github.com/abdurahmanasgf/GlassDoorWebScraping/blob/main/output1.png "Job Opportunities by State")

![alt text](https://github.com/abdurahmanasgf/GlassDoorWebScraping/blob/main/output2.png "Correlations 1")

![alt text](https://github.com/abdurahmanasgf/GlassDoorWebScraping/blob/main/output3.png "Correlations 2")


## Model Building 

First, I transformed the categorical variables into dummy variables. I also split the data into train and test sets with a test size of 20%.   

I tried three different models and evaluated them using Mean Absolute Error. I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad in for this type of model.   

I tried three different models:
*	**Multiple Linear Regression** – Baseline for the model
*	**Lasso Regression** – Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.
*	**Random Forest** – Again, with the sparsity associated with the data, I thought that this would be a good fit. 

