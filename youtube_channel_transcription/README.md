BACKGROUND:
This project is part of a larger project to eventually be able to fine tune LLM models to conduct interview prep on niche roles and companies using embeddings and langchain. I've found that the large models like GPT4 are excellent for coming up with industry-level or popular job-role level questions. They, however, fail to include specifics about small companies or niche job roles. 
As I tried to collect text about a specific company BeautifulSoup kept failing to extract text from their webpages. I found that for my specific job interest, Sales Engineer, there was a treasure trove of information in the form of Youtube demo videos. So, I built this. 

INSTRUCTIONS: 
1. I used Jupyter-lab for this project. You will need to install the requirements listed in the requirements.txt
2. You will need to sign up for a Google Developer account and create a secret key to save to your .env
3. I found some videos on Youtube to be marked with age restrictions. Youtube deals with this by dropping a first-party cookie for a signed in user that gives you access to those videos. To then work around this with your code you will need to create a cookies.txt 