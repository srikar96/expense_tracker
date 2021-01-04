from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import *
import requests
from datetime import time, timedelta
import datetime as dt
import pandas as pd
from bson.json_util import dumps
import pymongo as pm
from functions import *

client = pm.MongoClient("mongodb://localhost:27017/")
db = client['monefy']
col1 = db['expenses']
col2 = db['savings']

class ActionAddExpense(Action):
    '''
    Add expenses to db
    '''
    def name(self):
        return "action_add_expense"

    def run(self, dispatcher, tracker, domain):
        notes = tracker.latest_message['text'].strip().split('notes')
        if len(notes) == 1:
            notes = None
        else:
            notes = notes[-1]

        category = tracker.get_slot('category').strip()
        amount = tracker.get_slot('amount').strip()

        if not notes:
            dispatcher.utter_message("I added that to your expenses.\nYou said ${} for {}.".format(amount, category))
            col1.insert_one({"timestamp": dt.datetime.now(), "person": "srikar", "category": category.strip(), "amount": float(amount.strip())})
        else:
            dispatcher.utter_message("I added that to your expenses.\nYou said ${} for {} with {} in notes.".format(amount, category, notes.strip()))
            col1.insert_one({"timestamp": dt.datetime.now(), "person": "srikar", "category": category.strip(), "amount": float(amount.strip()), "notes": notes.strip()})

        return None

class ActionQueryExpense(Action):
    '''
    Query expenses to db
    '''
    def name(self):
        return "action_query_expense"

    def run(self, dispatcher, tracker, domain):
        category = tracker.get_slot('category')
        date = tracker.get_slot('DATE')

        #print(category, date)
        query = get_date_info(category, date)

        cur = col1.aggregate(query)

        amount = 0
        for val in cur:
            amount += float(val['amount'])

        if not category:
            dispatcher.utter_message("Here are your expenses for {}.\nYou spent ${}.".format(date, round(amount,2)))
        else:
            dispatcher.utter_message("Here are your expenses for {}.\nYou spent ${} on {}.".format(date, round(amount,2), category))

        return None

class ActionSlotReset(Action):
    '''
    Resets all the Slots
    '''
    def name(self):
        return 'action_slots_reset'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet(slot, None) for slot in ['category', 'amount', 'DATE']]
