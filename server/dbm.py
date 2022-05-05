import os
from flask import jsonify
import pandas as pd
#from .extensions import client



            

def get_db():

    """
    A function that returns the collection table from the mongo db

    """
    db = client[os.environ.get("CLUSTER_TABLE")]
    collection = db[os.environ.get("COLLECTION_TABLE")]

    return collection

def store_data_base(collection, json_value):

    """
    A function that stores data in the collection
    
    """

    collection.insert_one(json_value)


def read_data_base(collection):

    """
    A function that accepts collection and returns a pandas dataframe++
    
    """

    data_frame = []

    data_val = collection.find()

    for i in data_val:

        data_frame.append(i)

    df = pd.DataFrame(data_frame)

    return df

    
def data_base_object(json_value):

    """
    A function that returns a dataframe from
    """

    data_x = get_db()

    store_data_base(data_x, json_value)

    read_data = read_data_base(data_x)

    return jsonify (read_data)
