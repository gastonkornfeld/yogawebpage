from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from .mixins import ModelMixin



category_table = db.Table('categories',
                      db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                      db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

# importin the mixin and adding to the user model make our user be able to use the flask login 

class YogaPost(db.Model, ModelMixin):
    """
    This class is to add different posts in to the yoga blog. 
    """
    title = db.Column(db.String(10000))
    main_content = db.Column(db.String(10000))
    secondary_content = db.Column(db.String(10000))
    image_url = db.Column(db.String(100000))
    
    


class User(db.Model, UserMixin, ModelMixin):
    
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique = True)
    other_info = db.Column(db.String(500))
    


class Recipe(db.Model, ModelMixin):
    """
    This class is to add different recipies in to the recipies template
    """
    name = db.Column(db.String(10000))
    ingredients = db.Column(db.String(10000))
    preparation = db.Column(db.String(10000))
    extra = db.Column(db.String(10000))
    image_url = db.Column(db.String(100000))
    categories = db.relationship('Category', secondary = category_table, back_populates='recipes_in_category')


class Category(db.Model, ModelMixin):
    '''
    This is to give different categories to the recipes. 
    '''
    category_name = db.Column(db.String(10000))
    recipes_in_category = db.relationship('Recipe', secondary = category_table, back_populates='categories')


class Course(db.Model, ModelMixin):
    """
    This class is to add or delete different courses in the my courses part.
    """
    name_of_course = db.Column(db.String(10000))
    type_of_course = db.Column(db.String(10000))
    price = db.Column(db.String(10000))
    description = db.Column(db.String(10000))



class Email_user(db.Model, ModelMixin):
    """
    This class is to save the users that register in the newsletter. 
    """
    email = db.Column(db.String(10000))


class Message(db.Model, ModelMixin):
    """
    This class is made for the user to be able to leave a message to the admin of the page.
    """
    name = db.Column(db.String(10000))
    content = db.Column(db.String(10000))


