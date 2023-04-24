import os
import openai
import logging
import json

class ChatGPT:
    startMessageStack = [
        {"role": "system", "content": "You act as the middleman between USER and a DATABASE. Your main goal is to answer questions based on data in a SQLite3 database (SERVER). You do this by executing valid queries against the database and interpreting the results to anser the questions from the USER."},
        {"role": "user", "content": "From now you will only ever respond with JSON. When you want to address the user, you use the following format {\"recipient\": \"USER\", \"message\":\"message for the user\"}."},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"I understand.\"}."},
        {"role": "user", "content": "You can address the SQL Server by using the SERVER recipient. When calling the server, you execute a query. The format you will use for executing a query is as follows: {\"recipient\":\"SERVER\", \"message\":\"SQL command;\"}"},
        {"role": "user", "content": f"The database has only one table called user. It was created with the following statement: CREATE TABLE user (name text, phone text);"},
        {"role": "user", "content": f"Let's start! How many Users do we have whose name starts with the letter e?"},
        {"role": "assistant", "content": "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"SELECT COUNT(*) AS COUNT FROM User WHERE name like 'e%';\"}"},
        {"role": "user", "content": "COUNT\n243"},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"There are 243 users in the database with the name starting with the letter e.\"}."},
    ]

    def __init__(self, api_key, api_org = "", model = "gpt-3.5-turbo"):
        if api_org:
            openai.api_key
        openai.api_key = api_key
        self.model = model
        self.messages = self.startMessageStack.copy()

    def message(self, message, sender):
        logging.debug(message)
        if (sender):
            message = json.dumps({'message':message, 'sender':sender})
        self.messages.append({"role": "user", "content": message})
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        response = completion.choices[0].message.content 
        logging.debug(response)
        self.messages.append({"role": "assistant", "content": response})
        return response

    def reset(self):
        self.messages = self.startMessageStack.copy()
        print('model was reset to intial state')

