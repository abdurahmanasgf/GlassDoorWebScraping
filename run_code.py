import web_scrap_glassdoor as gs
import pandas as pd

path = "C:/Users/user/Desktop/AmanPythonLearning/Data Analysis/web_scrapping"
df = gs.get_jobs('data scientist', 15, False, path, 15)
df.to_excel('./papa.xlsx')