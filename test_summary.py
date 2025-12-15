from nlp.summary import generate_Summary

sentiment_dist={"positive":15,"negative":5,"neutral":10,"total":30}
pos_features=["camera quality", "build", "display"]
neg_features=["battery life", "charging"]

summary=generate_Summary(sentiment_dist,pos_features,neg_features)

print(summary)