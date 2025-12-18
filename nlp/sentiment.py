from textblob import TextBlob

def analyze_sentiment(reviews):
    """
    reviews: list of strings
    Returns:
      results: list of dicts {review,polarity,sentiment}
      distribution:{"positive":x,"neutral":y,"negative":z}
    """
    result=[]
    dist={"positive":0,"neutral":0,"negative":0}

    for r in reviews:
        blob=TextBlob(r)
        polarity=blob.sentiment.polarity


        if polarity >= 0.1:
            sentiment="positive"
            dist["positive"]+=1
        elif polarity <= -0.1:
            sentiment="negative"
            dist["negative"]+=1
        else:
            sentiment="neutral"
            dist["neutral"]+=1

        result.append({
            "review":r,
            "polarity":polarity,
            "sentiment":sentiment

        })
        
    return result,dist