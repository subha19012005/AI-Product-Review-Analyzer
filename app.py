from flask import Flask, jsonify, request, render_template
from urllib.parse import unquote
import pandas as pd
import nltk
import textblob.download_corpora as dc

from storage.json_db import add_product, get_product
from nlp.sentiment import analyze_sentiment
from nlp.features import extract_features
from nlp.summary import generate_Summary

# -----------------------
# Download required corpora at startup
# -----------------------
nltk.download('punkt')
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
dc.download_all()  # TextBlob corpora

# -----------------------
# Flask App
# -----------------------
app = Flask(__name__)

# -----------------------
# Home / Upload Page
# -----------------------
@app.route("/")
def upload_page():
    return render_template("upload.html")

# -----------------------
# Dashboard Page
# -----------------------
@app.route("/dashboard/<product_name>")
def dashboard(product_name):
    try:
        product_name = unquote(product_name).strip().lower()
        product = get_product(product_name)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        analysis = product["analysis"]
        display_name = analysis.get("display_name", product_name)

        return render_template(
            "dashboard.html",
            product_name=display_name,
            sentiment=analysis["sentiment"],
            positive_features=analysis["features"]["positive"],
            negative_features=analysis["features"]["negative"],
            summary=analysis["summary"]
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Analyze Reviews
# -----------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        product_name_original = request.form.get("product_name")
        product_name = product_name_original.strip().lower() if product_name_original else None

        # Collect reviews
        reviews = []
        text_reviews = request.form.get("reviews")
        if text_reviews:
            reviews.extend([r.strip() for r in text_reviews.split("\n") if r.strip()])

        csv_file = request.files.get("csv_file")
        if csv_file:
            df = pd.read_csv(csv_file)
            if "review" not in df.columns:
                return jsonify({"error": "CSV must contain 'review' column"}), 400
            reviews.extend(df["review"].dropna().astype(str).tolist())

        if not product_name or not reviews:
            return jsonify({"error": "product_name and reviews required"}), 400

        # NLP processing
        sentiment_result, sentiment_dist = analyze_sentiment(reviews)
        pos_features, neg_features = extract_features(sentiment_result)
        summary = generate_Summary(sentiment_dist, pos_features, neg_features)

        # Store analysis
        analysis_data = {
            "sentiment": sentiment_dist,
            "features": {
                "positive": pos_features,
                "negative": neg_features
            },
            "summary": summary,
            "display_name": product_name_original
        }

        add_product(product_name, analysis_data)
        app.logger.info(f"Saved product: {product_name}")

        return jsonify({"success": True, "product_name": product_name})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Run Flask locally only
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
