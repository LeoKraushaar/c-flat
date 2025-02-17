import os
import datetime
import inflect
from dotenv import load_dotenv
from pymongo import MongoClient
from mongodb.preprocessing.food_categories import food_categories
import certifi

def ProcessItems(dict, quantity, date):
    '''
    Adds the processed item into db.
    '''
    load_dotenv()
    client = MongoClient(os.getenv('MONGO_URI'), tlsCAFile=certifi.where())
    db = client['SmartCart']
    collection = db['useritems']

    food = dict['hints'][0]['food']
    item = {}
    item['foodId'] = food['foodId']
    item['name'] = food['label']
    item['category'] = 'Others'
    item['quantity'] = f"{quantity}"
    item['expiryDate'] = date
    item['image'] = food['image']
    
    p = inflect.engine() # Helps convert nouns into singular form
    food_singular = p.singular_noun(item['name'])
    if food_singular == False:
        food_singular = item['name'].lower()
    else:
        food_singular = food_singular.lower()

    if any(food_singular in vegetable.lower() for vegetable in food_categories['vegetables']):
        item['category'] = 'vegetable'
    elif any(food_singular in fruit.lower() for fruit in food_categories['fruits']):
        item['category'] = 'fruit'
    elif any(food_singular in meat.lower() for meat in food_categories['meat']):
        item['category'] = 'meat'
    elif any(food_singular in dairy.lower() for dairy in food_categories['dairy']):
        item['category'] = 'dairy'
    elif any(food_singular in seafood.lower() for seafood in food_categories['seafood']):
        item['category'] = 'seafood'
    elif any(food_singular in condiments.lower() for condiments in food_categories['condiments/ingredients']):
        item['category'] = 'condiments/ingredients'

    try:
        collection.insert_one(item)
        print("Added successfully!")
        return item
    except Exception as e:
        print(e)
    finally:
        client.close()

def ProcessUnknownItems(name, quantity, date):
    '''
    For adding items that are not in the API to the collection.
    '''
    load_dotenv()
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client['SmartCart']
    collection = db['useritems']

    item = {}
    item['foodId'] = ''
    item['name'] = name
    item['category'] = 'Others'
    item['quantity'] = f"{quantity}"
    item['expiryDate'] = date
    item['image'] = 'https://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/hamburger.png'
  
    p = inflect.engine() # Helps convert nouns into singular form
    food_singular = p.singular_noun(item['name'])
    if food_singular == False:
        food_singular = item['name'].lower()
    else:
        food_singular = food_singular.lower()

    if any(food_singular in vegetable.lower() for vegetable in food_categories['vegetables']):
        item['category'] = 'vegetable'
    elif any(food_singular in fruit.lower() for fruit in food_categories['fruits']):
        item['category'] = 'fruit'
    elif any(food_singular in meat.lower() for meat in food_categories['meat']):
        item['category'] = 'meat'
    elif any(food_singular in dairy.lower() for dairy in food_categories['dairy']):
        item['category'] = 'dairy'
    elif any(food_singular in seafood.lower() for seafood in food_categories['seafood']):
        item['category'] = 'seafood'
    elif any(food_singular in condiments.lower() for condiments in food_categories['condiments/ingredients']):
        item['category'] = 'condiments/ingredients'

    try:
        collection.insert_one(item)
        print("Added successfully!")
        return item
    except Exception as e:
        print(e)
    finally:
        client.close()