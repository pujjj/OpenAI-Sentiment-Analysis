# OpenAI-Sentiment-Analysis
I have created a project which analyses the sentiment of any text/review using OpenAI’s API which is a powerful tool for natural language processing tasks.I have used model for sentiment analysis.

Built with Flask , Sqlite.



### Prerequisite
To activate virtualvenv:

```bash
  source bin/activate
```

Install Flask:
```bash
  pip install Flask
```
Install OpenAI package:
```bash
  pip install openai 
```
Install matplotlib for plots:
```bash
pip install matplotlib 
```     

Go to **app.py** and replace the below with your api key:

```python3
openai.api_key = "my-api-key" 
```

### Run Program
To run the program:
```bash
  python3 app.py
```
The application will be accessible at the specified host and port, usually http://127.0.0.1:5000/ or http://localhost:5000/.

Once the Flask application is running, you can open a web browser and visit the specified URL to access the deployed application.

![Screenshot 2023-06-20 at 11 55 25 AM](https://github.com/pujjj/OpenAI-Sentiment-Analysis/assets/97466150/04dd75a3-e1fb-43eb-9e43-265c99800f84)






