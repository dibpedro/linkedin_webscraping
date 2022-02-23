# linkedin_webscraping

This is the first step of a full project called "LinkedIn Job Posting Analysis" and consists of a data ingestion (Extract and Load) procedure to retrieve information about jobs requirements in the data fields (Data Science, Data Engineering, Data Analysis, etc).

I started by navigating through the LinkedIn jobs page and searching for the desired job keyword using Selenium. After I found a good amount of jobs, I used the BeautifulSoup library to inspect the page and get, from each announced job, the full link for that post. This is our first function, <code>get_links</code>.

Then, looping through that list and using BeautifulSoup I was able to get the Job Title, Company Name, Job Location and Job Description for each job link. After some filtering on the Descriptions list, the data retrieved was put on a dictionary and turned into a Pandas DataFrame. This is our second function, <code>jobs_dataframe</code>, and it returns something like this:

<img width="1317" alt="jobs_dataframe" src="https://user-images.githubusercontent.com/79810760/150280045-99c27787-1aee-4f7e-aa55-f38c2f81f6e1.png">

Finally, after some small validation, the data is ready to be stored into a database. For this, I created a PostgreSQL connection and a table using the sqlalchemy library to write SQL in Python. We can see the results in the picture below:

<img width="985" alt="jobs_in_database" src="https://user-images.githubusercontent.com/79810760/150281013-32e752cc-2353-43df-b653-e203fe044255.png">

Despite we're already able to make some Data Analysis and maybe some Machine Learning using the data we have, I want to stress that this is an ongoing project for some reasons:

-  First, maybe is it possible to refine a little bit more the description column and normalize all the table;
-  Second, this is just the first step of a bigger project, as I said earlier. So, we'll probably gonna make a lot of changes along the way, even though we may still use the EtLT pattern to do the engineering.

## Dependencies
This project was made using Python 3.10.0

## Executing
To run this project, in addition to Python, you'll need to have ChromeDriver and SQLite and its libraries for Python installed on your computer or on a virtual environment and chromedriver.exe on your project's folder. Then, run the <code>linkedin_scraper.py</code> file on your terminal window. Next, open the <code>scraping_jobs</code> notebook and substitute the keyword string of your interest on the <code>job_keyword</code> variable. Finally, run all cells and you're ready to open, on your database administration tool (mine's DBeaver), the data you've just got.

## Author
Pedro Dib (pedrodib100@gmail.com)

## Thanks
Thanks a lot to [Igor Magalhães](https://github.com/igormagalhaesr) for the project idea, and for helping me with tips on writing good code and best practices on documentation.
