from textblob import TextBlob
from collections import Counter


def extract_features(sentiment_results):
    """
    sentiment_results: list of dicts
    {review: "...", polarity: 0.5, sentiment: "positive"}

    Returns:
      postivie_features (list)
      negative_features (list)
       
    """

    pos_words=[]
    neg_words=[]

    for item in sentiment_results:
        review=item["review"]
        sentiment=item["sentiment"]

        blob=TextBlob(review)
        phrases=blob.noun_phrases

        words=[]
        for word,tag in blob.tags:
            if tag.startswith("NN") or tag.startswith("JJ"):
                words.append(word)
        
        combined=list(set(phrases+words))

        if sentiment=="positive":
            pos_words.extend(combined)
        elif sentiment== "negative":
            neg_words.extend(combined)
    pos_top=[]
    for word,count in Counter(pos_words).most_common(10):
        pos_top.append(word)
    neg_top=[]
    for word,count in Counter(neg_words).most_common(10):
        neg_top.append(word)
    
    return pos_top,neg_top


