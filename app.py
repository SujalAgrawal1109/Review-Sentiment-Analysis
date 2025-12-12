import sqlite3
import pandas as pd
from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from datetime import datetime

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    """Initializes the SQLite database and creates the table if it doesn't exist."""
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  content TEXT, 
                  sentiment TEXT, 
                  polarity REAL, 
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

# --- AI Analysis Logic ---
def analyze_sentiment(text):
    """Returns sentiment label and polarity score using NLP."""
    if not isinstance(text, str):
        return "Neutral", 0.0
        
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, polarity

def get_emoji(sentiment):
    """Helper to add emojis for display."""
    if sentiment == "Positive": return "Positive 😊"
    elif sentiment == "Negative": return "Negative 😠"
    else: return "Neutral 😐"

# --- Application Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyzes a single review submitted by the user."""
    data = request.get_json()
    text_content = data.get('review', '')
    
    sentiment, polarity = analyze_sentiment(text_content)
    display_sentiment = get_emoji(sentiment)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save to DB
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute("INSERT INTO reviews (content, sentiment, polarity, timestamp) VALUES (?, ?, ?, ?)", 
              (text_content, display_sentiment, polarity, timestamp))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'sentiment': display_sentiment, 'score': polarity})

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles CSV file uploads for batch processing."""
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file uploaded'})
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})

    try:
        # Read CSV using Pandas
        df = pd.read_csv(file)
        
        # Determine which column contains the text
        # We look for 'Review' or 'Text', otherwise take the first column
        target_col = None
        for col in ['Review', 'review', 'Text', 'text', 'Content']:
            if col in df.columns:
                target_col = col
                break
        if not target_col:
            target_col = df.columns[0]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        count = 0
        
        conn = sqlite3.connect('reviews.db')
        c = conn.cursor()
        
        # Process every row
        for index, row in df.iterrows():
            text = str(row[target_col])
            if text.strip(): # Skip empty rows
                sentiment, polarity = analyze_sentiment(text)
                display_s = get_emoji(sentiment)
                
                c.execute("INSERT INTO reviews (content, sentiment, polarity, timestamp) VALUES (?, ?, ?, ?)", 
                          (text, display_s, polarity, timestamp))
                count += 1
                
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'count': count})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/history', methods=['GET'])
def get_history():
    """Fetches the most recent 50 reviews."""
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute("SELECT content, sentiment, timestamp FROM reviews ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/stats', methods=['GET'])
def get_stats():
    """Calculates totals for the chart."""
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute("SELECT sentiment, COUNT(*) FROM reviews GROUP BY sentiment")
    rows = c.fetchall()
    conn.close()
    
    # Convert to dictionary: {'Positive 😊': 10, 'Negative 😠': 5}
    stats = {row[0]: row[1] for row in rows}
    return jsonify(stats)

if __name__ == '__main__':
    init_db()
    print("✅ App running on: http://127.0.0.1:5000")
    app.run(debug=True)