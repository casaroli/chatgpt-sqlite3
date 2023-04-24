import json
from chatgpt import ChatGPT
import sqlite3
import configparser

# Read the config file
config = configparser.ConfigParser()
config.read("config.ini")

# Access the config values
db_file = config.get("database", "file")
openai_api_key = config.get("openai", "api_key")
openai_org = config.get("openai", "org")
openai_model = config.get("openai", "model")

class Controller:
    def __init__(self):
        # initialise all the things
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()
        self.chatModel = ChatGPT(openai_api_key, openai_org, openai_model)

    def run(self, message, sender):
        responseString = self.chatModel.message(message, sender)
        try:
            response = json.loads(responseString[:-1] if responseString.endswith('.') else responseString)
        except ValueError:
            return self.run("Please repeat that answer but use valid JSON only.", "SYSTEM", counter + 1)
        match response["recipient"]:
            case "USER": 
                return response["message"]
            case "SERVER":
                # print ('SQL QUERY:', response["message"])
                result = repr(self.cur.execute(response["message"]).fetchall())
                self.con.commit()
                # print ('SQL RESULT:', result)
                return self.run(result, None)
            case _:
                print('error, invalid recipient')
                print(response)

    def reset(self):
        self.chatModel.reset()
