from flask import Flask, jsonify, request, render_template
from urllib.parse import unquote
import pandas as pd

from storage.json_db import add_product, get_product
from nlp.sentiment import analyze_sentiment
from nlp.features import extract_features
from nlp.summary import generate_Summary

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
    # Normalize for lookup
    product_name = unquote(product_name).strip().lower()
    product = get_product(product_name)

    if not product:
       # print("Available products:", list(get_all_products()))
        return "Product not found", 404

    analysis = product["analysis"]

    # Use display_name if available
    display_name = analysis.get("display_name", product_name)

    return render_template(
        "dashboard.html",
        product_name=display_name,
        sentiment=analysis["sentiment"],
        positive_features=analysis["features"]["positive"],
        negative_features=analysis["features"]["negative"],
        summary=analysis["summary"]
    )


# -----------------------
# Analyze Reviews
# -----------------------
@app.route("/analyze", methods=["POST"])
def analyze():
   # data = request.json

    product_name_original = request.form.get("product_name")
    # Normalize product name for JSON key
    product_name = product_name_original.strip().lower() if product_name_original else None

    #reviews = data.get("reviews", [])
    reviews=[]
    text_reviews=request.form.get("reviews")
    if text_reviews:
        reviews.extend(
            [r.strip() for r in text_reviews.split("\n") if r.strip()]
        )
    csv_File=request.files.get("csv_file")
    if csv_File:
        df=pd.read_csv(csv_File)
        if "review" not in df.columns:
            return jsonify({"error":"CSV must contain 'review' column"}),400
        reviews.extend(df["review"].dropna().astype(str).tolist())



    if not product_name or not reviews:
        return jsonify({"error": "product_name and reviews required"}), 400

    

    # NLP processing
    sentiment_result, sentiment_Dist = analyze_sentiment(reviews)
    pos_features, neg_Features = extract_features(sentiment_result)
    summary = generate_Summary(sentiment_Dist, pos_features, neg_Features)

    # Store analysis
    analysis_data = {
        "sentiment": sentiment_Dist,
        "features": {
            "positive": pos_features,
            "negative": neg_Features
        },
        "summary": summary,
        "display_name": product_name_original  # keep original for dashboard display
    }

    add_product(product_name, analysis_data)
    print("Saved product:", product_name)

    return jsonify({
        "success":True,
        "product_name":product_name
    }
    )





# -----------------------
# Run Flask
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
