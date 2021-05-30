from datetime import datetime
from . import db

class ModelMixin:
    """
    Mixin for all the models
    """

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    modified_at = db.Column(db.DateTime(), onupdate=datetime.now)

    def save(self):
        """
        Saves a user into the DB
        If the model is a transient (if it's not added to the DB yet), the function will add it
        before commiting, else it will just commit the new modifications.
        """
        try:
            # Checking if the model is a transient, if so, add it to the DB
            if self._sa_instance_state.transient:
                db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(f"Failed to save user {self}, ignoring")

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def __repr__(self):
        return f"<{self.__class__.__name__.title()} {self.id}>"