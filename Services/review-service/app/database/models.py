from mongoengine import Document, StringField, IntField, UUIDField
from uuid import uuid4

class Review(Document):
    id = UUIDField(primary_key=True, default=uuid4, binary=False)
    title = StringField(required=True,max_length=60)
    description = StringField()
    apartment_id = IntField()
    user_email = StringField()

    def __str__(self):
        return (f"title={self.title}, description={self.description}"
                f"apartment_id={self.apartment_id}, user_email={self.user_email}")