from flask import Flask, render_template, request
import openai
import sqlite3
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure



app = Flask(__name__, static_folder='static')
DATABASE = 'reviews.db'


openai.api_key = "my-api-key"

def create_table():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                review_text TEXT,
                rating INTEGER,
                sentiment TEXT,
                date_time TEXT)''')
    conn.commit()
    conn.close()


def insert_review(name, email, review_text, rating, sentiment):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO reviews (name, email, review_text, rating, sentiment, date_time) VALUES (?, ?, ?, ?, ?, ?)",
          (name, email, review_text, rating, sentiment, date_time))

    conn.commit()
    conn.close()


def get_sentiment(text):
    messages = [
        {"role": "system", "content": """You are trained to analyze and detect the sentiment of given text. 
                                        If you're unsure of an answer, you can say "not sure" and recommend users to review manually."""},
        {"role": "user", "content": f"""Analyze the following product review and determine if the sentiment is: positive or negative. 
                                        Return answer in single word as either positive or negative: {text}"""}
        ]
   
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages, max_tokens=100, temperature=0)
    response_text = response.choices[0].message.content.strip().lower()
    return response_text

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        sentence = request.form['sentence']
        rating = int(request.form['rating'])+1

        sentiment = get_sentiment(sentence)
        insert_review(name, email,sentence,rating, sentiment)
        # return render_template('index.html', sentence=sentence, sentiment=sentiment)
        return render_template('index.html', sentence=sentence, sentiment=sentiment, name=name, email=email, rating=rating)

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Retrieve sentiment data from the database
    c.execute("SELECT sentiment FROM reviews")
    sentiment_rows = c.fetchall()
    # Count the occurrences of each sentiment
    sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
    for row in sentiment_rows:
        sentiment = row[0]
        if sentiment in sentiments:
            sentiments[sentiment] += 1
    # Create a bar plot for sentiment distribution
    sentiment_labels = list(sentiments.keys())
    sentiment_values = list(sentiments.values())
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)  # Set up a subplot grid with 1 row and 2 columns
    plt.bar(sentiment_labels, sentiment_values)
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.title('Sentiment Distribution')
    # Save the sentiment plot as a file
    sentiment_plot_file = 'static/plots/sentiment_plot.png'
    plt.savefig(sentiment_plot_file)
    app.config['SENTIMENT_PLOT_PATH'] = sentiment_plot_file

    # Retrieve rating data from the database
    c.execute("SELECT rating FROM reviews")
    rating_rows = c.fetchall()
    # Initialize a dictionary for rating counts
    ratings = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    # Count the occurrences of each rating
    for row in rating_rows:
        rating = row[0]
        if rating in ratings:
            ratings[rating] += 1
    # Create a bar plot for rating count
    rating_labels = list(ratings.keys())
    rating_values = list(ratings.values())
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)  # Set up a subplot grid with 1 row and 2 columns
    plt.bar(rating_labels, rating_values)
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.title('Rating Count')
    # Save the rating plot as a file
    rating_plot_file = 'static/plots/rating_plot.png'
    plt.savefig(rating_plot_file)
    app.config['RATING_PLOT_PATH'] = rating_plot_file

    #Sentiments vs date-time
    # Retrieve sentiment and date-time data from the database
    c.execute("SELECT sentiment, date_time FROM reviews")
    rows = c.fetchall()
    # Separate sentiment and date-time values
    sentiments = [row[0] for row in rows]
    date_times = [row[1] for row in rows]
    # Create a line plot for sentiment against date
    plt.plot(date_times, sentiments)
    plt.xlabel('Date')
    plt.ylabel('Sentiment')
    plt.title('Sentiment Trend')
    # Save the plot as a file
    datevsentiment_plot_file = 'static/plots/datevsentiment_plot.png'
    plt.savefig(datevsentiment_plot_file)
    app.config['DATEVSENTIMENT_PLOT_PATH'] = datevsentiment_plot_file

    
    # Pros and cons
    c.execute("SELECT review_text FROM reviews")
    rows = c.fetchall()
    reviews = [row[0] for row in rows]
    # Concatenate all reviews into a single text
    reviews_text = " ".join(reviews)
    # Analyze reviews using OpenAI API
    messages = [
        {"role": "system", "content": "You are trained to analyze the pros and cons of review text."},
        {"role": "user", "content": reviews_text}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        temperature=0
    )
    response_text = response.choices[0].message.content.strip()
    # Split the response into pros and cons if available
    split_pros = response_text.split('Pros:', 1)
    split_cons = response_text.split('Cons:', 1)
    overall_pros = split_pros[1].strip() if len(split_pros) > 1 else "No pros found."
    overall_cons = split_cons[1].strip() if len(split_cons) > 1 else "No cons found."

    # Render the template with the plots
    return render_template('dashboard.html', sentiment_plot_file=sentiment_plot_file, rating_plot_file=rating_plot_file,datevsentiment_plot_file=datevsentiment_plot_file ,overall_pros=overall_pros, overall_cons=overall_cons)




if __name__ == '__main__':
    create_table()
    app.run(debug=True)