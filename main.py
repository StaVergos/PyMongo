from mongoengine import *

from datetime import datetime
import os
import json

connect("mongo-dev-db")

# Defining documents

class User(Document):
    username = StringField(unique=True, required=True)
    email = EmailField(unique=True)
    password = BinaryField(required=True)
    age = IntField()
    bio = StringField(max_length=100)
    categories = ListField()
    admin = BooleanField(default=False)
    registered = BooleanField(default=False)
    date_created = DateTimeField(default=datetime.utcnow)

    def json(self):
        user_dict = {
            "username": self.username,
            "email": self.email,
            "age": self.age,
            "bio": self.bio,
            "categories": self.categories,
            "admin": self.admin,
            "registered": self.registered
        }
        return json.dumps(user_dict)

    meta = {
        "indexes": ["username", "email"],
        "ordering": ["-date_created"]
    }

# Dynamic documents

class BlogPost(DynamicDocument):
    title = StringField()
    content = StringField()
    author = ReferenceField(User)
    date_created = DateTimeField(default=datetime.utcnow)

    meta = {
        "indexes": ["title"],
        "ordering": ["-date_created"]
    }

# Save a document

user = User(
    username = "JoeDoe",
    email = "jdoe@gmail.com",
    password = os.urandom(16),
    age = "30",
    bio = "My name is Joe",
    admin = True
).save()

BlogPost(
    title = "My first blog post",
    content = "Learning PyMongo",
    author = user,
    tags=["Python", "MongoDB", "MongoEngine"],
    category = "MongoDB"
).save()

print("Done")