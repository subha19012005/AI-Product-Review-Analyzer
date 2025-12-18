from nlp.features import extract_features

test_input=[
    {"review": "Great battery life and amazing camera quality!", "sentiment": "positive"},
    {"review": "Poor charging speed and bad display.", "sentiment": "negative"},
    {"review": "Excellent build but expensive price.", "sentiment": "positive"}

]

pos,neg=extract_features(test_input)

print(pos)
print(neg)
