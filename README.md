# Review-Sentiment-Analysis
📊 Sentiment Analysis Web AppA lightweight Flask web application that performs Natural Language Processing (NLP) on text reviews. It classifies text as Positive, Negative, or Neutral and visualizes the results.This application supports both real-time single-entry analysis and bulk processing via CSV file uploads, storing all results in a local SQLite database.

🚀 FeaturesReal-time Analysis: Type a review and get instant sentiment feedback with polarity scores.Batch Processing: Upload a CSV file to analyze hundreds of reviews at once.Data Persistence: Automatically saves all analyses to a SQLite database.Smart Parsing: Automatically detects text columns in uploaded CSVs (looks for 'Review', 'Text', 'Content', etc.).History & Stats: API endpoints provided to fetch analysis history and aggregate statistics.Visual Indicators: Uses emojis (😊, 😐, 😠) to quickly represent sentiment.
🛠️ Tech StackBackend:
Python 3,
FlaskDatabase: SQLite 3Data Processing: PandasNLP Engine: TextBlob

📂 Project StructureTo run this application successfully, ensure your folder structure looks like this:Plaintext/your-project-folder
│
├── app.py              # The main Flask application code (provided)
├── README.md           # This documentation file
├── requirements.txt    # List of python dependencies
└── templates/          # Folder for HTML files
    └── index.html      # The frontend interface (required)
⚙️ Installation & SetupClone or Download the repository.Install Dependencies:Open your terminal/command prompt and run:Bashpip install flask pandas textblob
(Optional) If you run into issues with TextBlob, you may need to download the corpora:Bashpython -m textblob.download_corpora
Run the Application:Bashpython app.py
Access the App:Open your web browser and navigate to:http://127.0.0.1:5000

📖 Usage Guide1. Single AnalysisEnter text into the input field on the homepage.The system calculates a Polarity Score (from -1.0 to 1.0).Logic:Score > 0.1: Positive 😊Score < -0.1: Negative 😠Otherwise: Neutral 😐2. Bulk Upload (CSV)Prepare a CSV file. The app is smart enough to find the text column, but for best results, name your column Review or Text.Upload the file via the "Upload" section.The app will process every row, save it to the database, and return the count of processed items.

🔗 API EndpointsIf you want to extend the frontend or access data programmatically:MethodEndpointDescriptionGET/Renders the main HTML interface.POST/analyzeAccepts JSON {'review': 'text'}. Returns sentiment & score.POST/uploadAccepts a file named file. Returns process count.GET/historyReturns the last 50 entries from the database.GET/statsReturns a JSON summary of counts (e.g., {'Positive 😊': 15}).

🤝 ContributingFeel free to fork this project and submit pull requests. Future improvements could include:Adding authentication.Replacing TextBlob with a more advanced model (like VADER or BERT).Adding export functionality to download results as CSV.

💡 Next StepYour code references render_template('index.html'), but the HTML code wasn't included. Would you like me to generate a modern, responsive index.html file that connects to these API endpoints so the app is fully functional?
