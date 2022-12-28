import data_scraping as gs
path = '/home/amin/Dokumente/Python/Data-Science-Salary/chromedriver'

df = gs.fetch_jobs('data scientist', 10, path, 2)
