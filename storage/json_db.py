import json
import os
from datetime import datetime

DB_FILE="storage/data.json"


def load_file():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE,"r") as f:
        return json.load(f)



def save_db(data):
    with open(DB_FILE,"w") as f:
        json.dump(data,f,indent=4)


def add_product(product_name,analysis_Data):
    db=load_file()

    db[product_name]={
        "analysis":analysis_Data,
        "created_at":datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


    }
    save_db(db)


def get_product(product_name):
    db=load_file()
    return db.get(product_name)

def get_all_products():
    return load_file()
