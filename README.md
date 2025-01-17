"" 

# Sensitive Content Evaluator

A Flask-based application to evaluate sensitive words in text and provide risk levels.

## Features
- RESTful API for content evaluation.
- Email notifications for flagged content.
- Database support to store and manage sensitive words.

## Setup
1. Install dependencies:

   `pip install -r requirements.txt`
2. Set up database and smtp service
   At root/config/default.py

3. Set api key 
   windows:`setx API_KEY "your_api_key_here"`

4. Run the application:
   `python app.py`
## Needs improvement
- Interface optimization
- Remote deployment
- Improvement of Spiders