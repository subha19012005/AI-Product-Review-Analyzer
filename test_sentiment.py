from nlp.sentiment import analyze_sentiment

reviews=[
    "Amazing product, I love the battery life!",
    "Worst product ever, waste of money.",
    "Okay product, but shipping was slow"
]

result,dist=analyze_sentiment(reviews)

print(result)
print(dist)