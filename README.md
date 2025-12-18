# AI Product Review Analyzer

AI Product Review Analyzer is a web application that helps analyze customer reviews of products.  
It performs sentiment analysis, extracts positive and negative features, generates a summary, and displays visualizations such as charts and word clouds. Users can submit reviews either as text input or via CSV files.

---

## Features

- Analyze sentiment (positive, negative, neutral) of product reviews.
- Extract positive and negative features from reviews.
- Generate a summary of customer opinions.
- Display sentiment distribution using bar charts.
- Display word clouds for positive and negative features.
- Accept reviews via text input or CSV upload.

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python, Flask  
- **NLP:** TextBlob  
- **Storage:** JSON files  
- **Visualization:** Chart.js, WordCloud2.js  

---

## Installation / Setup

1. Clone the repository:
```bash
git clone <your-repo-link>
cd backend
2. Create the virtual environment:
```bash
python -m venv venv
3.Activate the virtual environment:
Windows:
```bash
venv\Scripts\activate
Linux / MacOS:
```bash
source venv/bin/activate
4. Install dependencies:
```bash
pip install -r requirements.txt
5. Run the Flask app:
```bash
python app.py
6. Open your browser and navigate to:
http://127.0.0.1:5000/

---


Usage:

1. Enter a product name.
2. Enter reviews(one per line) or upload CSV file containing a review column.
3. Click Analyze
4. Go to the dashboard to view:
     Sentiment distribution (Positive, Neutral, Negative)
     Word clouds for positive and negative features
     Summary of customer opinion


Notes:
  CSV files must contain a column named review.
  TextBlob is used for sentiment analysis and feature extraction, which works best with longer sentences.
  The application supports multiple reviews at once, either via text input or CSV upload.


Screenshots:

Known Limitations
  TextBlob works better with longer sentences; short phrases may be classified as neutral.
  CSV input may not perfectly match text input for very short reviews.
  Does not yet support user authentication or database storage.

Future Improvements
  Integrate advanced NLP models like VADER or transformers for better sentiment accuracy.
  Add database support (MySQL/PostgreSQL) for persistent storage.
  Enhance frontend using React or another modern frontend framework.
  Include filtering and searching for multiple products in the dashboard.

