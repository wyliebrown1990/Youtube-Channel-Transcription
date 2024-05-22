# Youtube Channel Transcriber

## BACKGROUND:
This project is part of a larger project to eventually be able to fine tune LLM models to conduct interview prep on niche roles and companies using embedding retrievals. I've found that the large models like GPT4 are excellent for coming up with industry-level or popular job-role level questions. They, however, fail to include specifics about small companies or niche job roles. 

As I tried to collect text about a specific company BeautifulSoup kept failing to extract text from their webpages. I found that for my specific job interest, Sales Engineer, there was a treasure trove of information in the form of Youtube demo videos. So, I built this with the help of Chatgpt. 

## INSTRUCTIONS: 
1. You can clone and run this as a flask app locally by installing the requirements.txt
2. You will need to sign up for a Google Developer account and create a secret key to save to your .env
3. If you are trying to transcribe videos with mature content or really anything non-kid friendly then you will need to create a cookies.txt file in the correct format so the Google API recognizes you have permission
4. In the transcribe.py make sure to define the file path you want your .txt files to save to locally

### INTERVIEW APP:
If you want to use your transcribed data to fine tune an Openai (or really any gen ai) model you can clone my project here: https://github.com/wyliebrown1990/interview-app 
