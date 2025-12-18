def generate_Summary(sentiment_dist,pos_features,neg_features):
    """
    sentiment_dist={"positive":X,"negative":Y,"neutral":Z}
    pos_features=list of positive features
    neg_features=list of negative features
    """
    total=sentiment_dist.get("total",1)
    pos=sentiment_dist.get("positvie",0)
    neg=sentiment_dist.get("negative",0)
    neu=sentiment_dist.get("neutral",0)

    if pos > neg:
        overall="Customers generally feel positive about this product."
    elif neg>pos:
        overall="Cusotmers generally have negative opinions about this product."
    else:
        overall="Customer opinions are mixed."

    if pos_features:
        pos_text="Customers appreciated features like:"+",".join(pos_features[:5])+"."
    else:
        pos_text="No strong positive features were identified."
    
    if neg_features:
        neg_text="Customer reported issue with:"+",".join(neg_features[:5])+"."
    else:
        neg_text="No major negative issues were detected."
    
    summary=f"{overall} {pos_text} {neg_text}"


    return summary


    