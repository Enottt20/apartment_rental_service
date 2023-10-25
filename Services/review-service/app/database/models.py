from mongoengine import Document
from mongoengine import StringField

class Review(Document):
    title = StringField(required=True,max_length=60)
    description = StringField()

    def __str__(self):
        return f"Product(title={self.title}, description={self.description})"