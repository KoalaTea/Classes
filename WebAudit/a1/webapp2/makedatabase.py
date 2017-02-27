#!flask/bin/python
import time
from pymongo import MongoClient, ASCENDING
from werkzeug.security import generate_password_hash
# TODO make usernames unique


client = MongoClient()
client.drop_database("ChambordPi")
db = client.ChambordPi

drinks = db.Drinks
alcohol = db.Alchohol
users = db.Users
orders = db.Orders
mixers = db.Mixers
beer = db.Beer
ingredients = db.Ingredients
statistics = db.Statistics

statistics.insert_one(
    {
        "id": 1,
        "time": int(time.time()*1000) ,
        "total_orders": 0,
        "drink_orders": [
            {"name": "Sky", "Orders": 0},
            {"name": "Malibu", "Orders": 0},
            {"name": "Bacardi", "Orders": 0}
        ]
    }
)

ingredients.insert_one(
        {
            "class": "alcohol",
            "type" : "vodka",
            "name" : "sky",
            "flavor" : None,
            "bottles" : 1,
            "available": True,
            "cost": 25,
            "times_ordered" : 0
        }
)
ingredients.insert_one(
        {
            "class": "alcohol",
            "type" : "",
            "name" : "Jager",
            "flavor" : None,
            "bottles" : 1,
            "available": True,
            "cost": 25,
            "times_ordered" : 0
        }
)
ingredients.insert_one(
        {
            "class": "alcohol",
            "type" : "rum",
            "name" : "Malibu",
            "flavor" : "Coconut",
            "bottles" : 1,
            "available": True,
            "cost": 25,
            "times_ordered" : 0

        }
)
ingredients.insert_one(
        {
            "class": "alcohol",
            "type" : "rum",
            "name" : "Bacardi",
            "flavor" : None,
            "bottles" : 1,
            "available": True,
            "cost": 25,
            "times_ordered" : 0

        }
)
ingredients.insert_one(
        {
            "class": "alcohol",
            "type" : "Gin",
            "name" : "New Amsterdam",
            "flavor" : None,
            "bottles" : 1,
            "available": True,
            "cost": 25,
            "times_ordered" : 0

        }
)
ingredients.insert_one(
        {
            "class": "alcohol",
            "type" : "Whiskey",
            "name" : "Jack Daniels",
            "flavor" : None,
            "bottles" : 1,
            "available": True,
            "cost": 25,
            "times_ordered" : 0

        }
)
ingredients.insert_one(
        {
            "class": "alcohol",
            "type" : "vodka",
            "name" : "UV Blue",
            "flavor" : None,
            "bottles" : 1,
            "available": True,
            "cost": 25,
            "times_ordered" : 0

        }
)


ingredients.insert_one(
        {
            "class": "mixer",
            "name": "Orange Juice",
            "bottles": 5,
            "available": True
        }
)
ingredients.insert_one(
        {
            "class": "mixer",
            "name": "Sprite",
            "bottles": 5,
            "available": True
        }
)
ingredients.insert_one(
        {
            "class": "mixer",
            "name": "Coca-Cola",
            "bottles": 5,
            "available": True
        }
)
ingredients.insert_one(
        {
            "class": "mixer",
            "name": "Ginger Ale",
            "bottles": 5,
            "available": True
        }
)
ingredients.insert_one(
        {
            "class": "mixer",
            "name": "Lemonade",
            "bottles": 5,
            "available": True
        }
)
ingredients.insert_one(
        {
            "class": "mixer",
            "name": "Tonic",
            "bottles": 5,
            "available": True
        }
)

drinks.create_index([("id", ASCENDING)], unique=True)

drinks.insert_one(
        {
            "id": 0,
            "name": "Miller High Life",
            "type": "beer",
            "image": "beer.png",
            "recipe": [
                {
                    "type": "beer",
                    "flavor": None,
                    "amount": "1 oz"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 25
        }
)
drinks.insert_one(
        {
            "id": 1,
            "name": "Miller Lite",
            "type": "beer",
            "image": "beer.png",
            "recipe": [
                {
                    "type": "beer",
                    "flavor": None,
                    "amount": "1 oz"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 10
       }
)

drinks.insert_one(
        {
            "id": 2,
            "name": "Budweiser",
            "type": "beer",
            "image": "beer.png",
            "recipe": [
                {
                    "type": "beer",
                    "flavor": None,
                    "amount": "1 oz"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 10
       }
)

drinks.insert_one(
        {
            "id": 3,
            "name": "Shock Top",
            "type": "beer",
            "image": "beer.png",
            "recipe": [
                {
                    "type": "beer",
                    "flavor": None,
                    "amount": "1 oz"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 25
       }
)

drinks.insert_one(
        {
            "id": 4,
            "name": "Screwdriver",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "vodka",
                    "flavor": None,
                    "amount": "1 oz"
                },
                {
                    "type": "orange juice",
                    "flavor": None,
                    "amount": "1 oz"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 25
       }
)

drinks.insert_one(
        {
            "id": 5,
            "name": "Godfather",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "amaretto",
                    "flavor": None,
                    "amount": "1 oz"
                },
                {
                    "type": "whiskey",
                    "flavor": None,
                    "amount": "1 oz"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 50
       }
)

drinks.insert_one(
        {
            "id": 6,
            "name": "Mojito",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "lime",
                    "flavor": None,
                    "amount": "1/2"
                },
                {
                    "type": "white rum",
                    "flavor": None,
                    "amount": "2 oz"
                },
                {
                    "type": "club soda",
                    "flavor": None,
                    "amount": "2 oz"
                },
                {
                    "type": "mint",
                    "flavor": None,
                    "amount": "muddled"
                },
                {
                    "type": "sugar",
                    "flavor": None,
                    "amount": "tablespoon of sugar"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 50
       }
)

drinks.insert_one(
        {
            "id": 7,
            "name": "Dark and Stormy",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "lime",
                    "flavor": None,
                    "amount": "1/2"
                },
                {
                    "type": "rum",
                    "flavor": None,
                    "amount": "1 part"
                },
                {
                    "type": "ginger beer",
                    "flavor": None,
                    "amount": "1 part"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 25
       }
)

drinks.insert_one(
        {
            "id": 8,
            "name": "Moscow Mule",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "lime",
                    "flavor": None,
                    "amount": "1/2"
                },
                {
                    "type": "vodka",
                    "flavor": None,
                    "amount": "1 part"
                },
                {
                    "type": "ginger beer",
                    "flavor": None,
                    "amount": "1 part"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 25
       }
)

drinks.insert_one(
        {
            "id": 9,
            "name": "Rum Chata TODO",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "fireball",
                    "flavor": None,
                    "amount": "1 part"
                },
                {
                    "type": "rum chata",
                    "flavor": None,
                    "amount": "3 parts"
                },
                {
                    "type": "ginger beer",
                    "flavor": None,
                    "amount": "1 part"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 25
       }
)

drinks.insert_one(
        {
            "id": 10,
            "name": "Electric Boogaloo",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "UV Blue",
                    "flavor": None,
                    "amount": "3 shots"
                },
                {
                    "type": "Lemon juice",
                    "flavor": None,
                    "amount": "2 shots"
                },
                {
                    "type": "Sprite",
                    "flavor": None,
                    "amount": "Fill rest"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 75
       }
)

drinks.insert_one(
        {
            "id": 11,
            "name": "Martini",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Gin",
                    "flavor": None,
                    "amount": "3 shots"
                },
                {
                    "type": "Dry vermouth",
                    "flavor": None,
                    "amount": "2 shots"
                },
                {
                    "type": "Crushed ice",
                    "flavor": None,
                    "amount": "Varies"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 75
       }
)

drinks.insert_one(
        {
            "id": 12,
            "name": "Rum and Coke",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Rum",
                    "flavor": None,
                    "amount": "2 shots"
                },
                {
                    "type": "Coca-Cola",
                    "flavor": None,
                    "amount": "2 shots"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 50
       }
)

drinks.insert_one(
        {
            "id": 13,
            "name": "Whiskey and Coke",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Whiskey",
                    "flavor": None,
                    "amount": "2 shots"
                },
                {
                    "type": "Coca-Cola",
                    "flavor": None,
                    "amount": "2 shots"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 50
       }
)

drinks.insert_one(
        {
            "id": 14,
            "name": "Whiskey Sour",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Whiskey",
                    "flavor": None,
                    "amount": "2 shots"
                },
                {
                    "type": "Lemon Juice",
                    "flavor": None,
                    "amount": "2 shots"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 50
       }
)

drinks.insert_one(
        {
            "id": 15,
            "name": "Rum and Sprite",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Rum",
                    "flavor": None,
                    "amount": "2 shots"
                },
                {
                    "type": "Sprite",
                    "flavor": None,
                    "amount": "2 shots"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 50
       }
)

drinks.insert_one(
        {
            "id": 16,
            "name": "Shirley Temple",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Grenadine",
                    "flavor": None,
                    "amount": "1 shot"
                },
                {
                    "type": "Ginger ale",
                    "flavor": None,
                    "amount": "1 shot"
                },
                {
                    "type": "Sprite",
                    "flavor": None,
                    "amount": "1 shot"
                },
                {
                    "type": "Sky",
                    "flavor": None,
                    "amount": "1 shot"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 25
       }
)

drinks.insert_one(
        {
            "id": 17,
            "name": "Yellow Thunder",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Vodka",
                    "flavor": None,
                    "amount": "2 shots"
                },
                {
                    "type": "Lemonade",
                    "flavor": None,
                    "amount": "1 shot"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 50
       }
)

drinks.insert_one(
        {
            "id": 18,
            "name": "Jagerbomb",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Jager",
                    "flavor": None,
                    "amount": "1 shot"
                },
                {
                    "type": "Red Bull",
                    "flavor": None,
                    "amount": "1 shot"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 25
       }
)

drinks.insert_one(
        {
            "id": 19,
            "name": "Gin Sour",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Gin",
                    "flavor": None,
                    "amount": "2 shots"
                },
                {
                    "type": "Lemon juice",
                    "flavor": None,
                    "amount": "1 shot"
                },
                {
                    "type": "Sugar",
                    "flavor": None,
                    "amount": "Tablespoon"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 25
       }
)

drinks.insert_one(
        {
            "id": 20,
            "name": "Blowjob Shot",
            "type": "shot",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Khalua",
                    "flavor": None,
                    "amount": "1/2 shot"
                },
                {
                    "type": "Irish cream",
                    "flavor": None,
                    "amount": "1/2 shot"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 25
       }
)

drinks.insert_one(
        {
            "id": 21,
            "name": "Gin and Tonic",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Gin",
                    "flavor": None,
                    "amount": "2 shots"
                },
                {
                    "type": "Tonic",
                    "flavor": None,
                    "amount": "1 shot"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 50
       }
)

drinks.insert_one(
        {
            "id": 22,
            "name": "Alexander",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Brandy",
                    "flavor": None,
                    "amount": "1 shot"
                },
                {
                    "type": "Cream",
                    "flavor": None,
                    "amount": "1 shot"
                },
                {
                    "type": "Creme de cacao",
                    "flavor": None,
                    "amount": "1 shot"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 50
       }
)

drinks.insert_one(
        {
            "id": 23,
            "name": "White Russian",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Coffee liqueur",
                    "flavor": None,
                    "amount": "1 shot"
                },
                {
                    "type": "Vodka",
                    "flavor": None,
                    "amount": "2 shots TODO"
                },
                {
                    "type": "Cream",
                    "flavor": None,
                    "amount": "2 shots"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 75
       }
)

drinks.insert_one(
        {
            "id": 24,
            "name": "Vodka Red Bull",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Vodka",
                    "flavor": None,
                    "amount": "2 shots"
                },
                {
                    "type": "Red Bull",
                    "flavor": None,
                    "amount": "1 cup"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 50
       }
)

drinks.insert_one(
        {
            "id": 25,
            "name": "Black Russian",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Vodka",
                    "flavor": None,
                    "amount": "2 shots"
                },
                {
                    "type": "Coffee liqueur",
                    "flavor": None,
                    "amount": "1.5 shots"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 75
       }
)

drinks.insert_one(
        {
            "id": 26,
            "name": "Grasshopper TODO Blended?",
            "type": "mixed",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Mint cream",
                    "flavor": None,
                    "amount": "1.5 shots"
                },
                {
                    "type": "Creme de cacao",
                    "flavor": None,
                    "amount": "1.5 shots"
                },
                {
                    "type": "Fresh cream",
                    "flavor": None,
                    "amount": "1 shot"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 50
       }
)

drinks.insert_one(
        {
            "id": 27,
            "name": "B-52",
            "type": "part",
            "image": "dirty_martini.png",
            "recipe": [
                {
                    "type": "Kahlua",
                    "flavor": None,
                    "amount": "1 part"
                },
                {
                    "type": "Bailey's",
                    "flavor": None,
                    "amount": "1 part"
                },
                {
                    "type": "Brandy",
                    "flavor": None,
                    "amount": "1 part"
                }
                            ],
            "available": True,
            "times_ordered" : 0,
            "cost" : 75
       }
)

users.create_index([("username", ASCENDING)], unique=True)

users.insert_one(
        {
            "username" : "koalatea",
            "password" : generate_password_hash("temporary2017koalatea"),
            "credits" : 1000000,
            "roles" : [ "bartender", "admin", "user" ],
            "drinksOrdered" : 0
        }
)
