import flask
from flask.helpers import url_for
from flask_sqlalchemy import model
from sqlalchemy.sql.functions import mode, user
from website import forms
from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user

from . import db, models
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    """
    this route shows the homepage of the page 
    """
    message_form = forms.LeaveYourMessageForm()
    
    if message_form.validate_on_submit():
        name = message_form.name.data
        content = message_form.content.data
        new_message = models.Message(name = name , content = content)
        new_message.save()
        flask.flash('Your message was send it whit succes', 'success')


       
    
    return render_template("index.html", user=current_user, message_form = message_form)


@views.route('/blog', methods=['GET', 'POST'])
def blog():
    '''
    This route shows all the entrances in the yoga blog

    '''
    all_posts = models.YogaPost.query.all()
    message_form = forms.LeaveYourMessageForm()
    
    if message_form.validate_on_submit():
        name = message_form.name.data
        content = message_form.content.data
        new_message = models.Message(name = name , content = content)
        new_message.save()
        flask.flash('Your message was send it whit success', 'success')
    
    return render_template("blog.html", user=current_user, posts = all_posts, message_form = message_form)


@views.route('/blog/<int:id>', methods=['GET', 'POST'])
def blog_details(id):
    """
    This route is to access the specific description of a post inside of the blog.
    Takes the id of the Yogapost as a parameter 
    """
    blog_post = models.YogaPost.query.get(id)
    post_description = blog_post.secondary_content.split('&')
    return render_template('post_details.html', user= current_user, post = blog_post, post_description = post_description)

@views.route('/delete-blog/<int:id>', methods=['GET', 'POST'])
def delete_blog(id):
    """
    This route is to delete a post inside of the blog. Only allowed to the administrator of the site
    Takes the id of the Yogapost as a parameter 
    """
    blog_post = models.YogaPost.query.get(id)
    blog_post.delete()
    return redirect(url_for('views.blog'))

@views.route('/add-yoga-post', methods=['GET', 'POST'])
def add_yoga_post():
    """
    This route was made for the administrator of the site. To add the entrances in the blog
    """
    form = forms.AddYogaPost()
   
    if form.validate_on_submit():
        title = form.title.data
        main_content = form.main_content.data
        secondary_content = form.secondary_content.data
        web_picture_url = form.web_picture.data

        new_yoga_post = models.YogaPost(title = title, main_content = main_content, secondary_content = secondary_content, image_url = web_picture_url)
        new_yoga_post.save()
        return redirect(url_for('views.blog'))
        
        
        
        


    return render_template('add_yoga_post.html', user = current_user, form = form)



@views.route('/recipes', methods=['GET', 'POST'])
def recipes():
    """
    This routes show all the recipes categories charged in to the database in to the recipes categories template
    """
    categories = models.Category.query.all()
    message_form = forms.LeaveYourMessageForm()
    
    if message_form.validate_on_submit():
        name = message_form.name.data
        content = message_form.content.data
        new_message = models.Message(name = name , content = content)
        new_message.save()
        flask.flash('Your message was send it whit success', 'success')
    
    return render_template("recipes_category.html", user=current_user, categories = categories, message_form = message_form)


@views.route('/recipes/<category>', methods=['GET', 'POST'])
def recipes_by_category(category):
    """
    This routes show all the recipes of a particular category
    """
    recipes = models.Category.query.filter_by(category_name = category).first().recipes_in_category
    message_form = forms.LeaveYourMessageForm()
    
    if message_form.validate_on_submit():
        name = message_form.name.data
        content = message_form.content.data
        new_message = models.Message(name = name , content = content)
        new_message.save()
        flask.flash('Your message was send it whit success', 'success')
    
    return render_template("recipes.html", user=current_user, recipes= recipes , message_form = message_form)


@views.route('/recipe/<int:id>', methods=['GET', 'POST'])
def recipe_detail(id):
    """
    This route is to access the specific description of a recipe inside of the recipes blog.
    Takes the id of the recipe as a parameter 
    """
    recipe = models.Recipe.query.get(id)
    recipe_ingredients = recipe.ingredients.split('&')
    recipe_preparation = recipe.preparation.split('&')
    extra_info = recipe.extra.split('&')
    return render_template('recipe_details.html', recipe = recipe, user = current_user, recipe_ingredients = recipe_ingredients,
                                            recipe_preparation = recipe_preparation, extra_info = extra_info)


@views.route('/delete-recipe/<int:id>', methods=['GET', 'POST'])
def delete_recipe(id):
    """
    This route is to access delete specific a recipe inside of the recipes blog. Only allowed by the administrator
    Takes the id of the recipe as a parameter 
    """
    recipe = models.Recipe.query.get(id)
    recipe.delete()
    return redirect(url_for('views.recipes'))



@views.route('/add-recipe', methods=['GET', 'POST'])
def add_recipe():
    """
    This route was made for the administrator of the site. To add the recipies to the recipies section
    There is 3 different categories in each recipie that the administrator is able to put on each recipe. If the category already exist
    will add the recipe to the category if not will create a new category and display it directly in to the categories template.
    """
    form = forms.AddRecipe()
    
   
    if form.validate_on_submit():
        name = form.title.data
        ingredients = form.ingredients.data
        preparation = form.preparation.data
        extra = form.extra.data
        web_picture_url = form.web_picture.data
        category1 = form.category1.data
        category2 = form.category2.data
        category3 = form.category3.data

        new_recipe = models.Recipe(name = name, ingredients = ingredients, extra = extra,  preparation= preparation, image_url = web_picture_url)
        new_recipe.save()
        if category1 != "":
            if models.Category.query.filter_by(category_name = category1).first():
                category1 = models.Category.query.filter_by(category_name = category1).first()
                new_recipe.categories.append(category1)
                category1.recipes_in_category.append(new_recipe)
                category1.save()
                new_recipe.save()
            else:
                new_category = models.Category(category_name = category1)
                new_category.save()
                new_recipe.categories.append(new_category)
                new_category.recipes_in_category.append(new_recipe)
                new_category.save()
                new_recipe.save()
        if category2 != "":
            if models.Category.query.filter_by(category_name = category2).first():
                category2 = models.Category.query.filter_by(category_name = category2).first()
                new_recipe.categories.append(category2)
                category2.recipes_in_category.append(new_recipe)
                category2.save()
                new_recipe.save()
            else:
                new_category = models.Category(category_name = category2)
                new_category.save()
                new_recipe.categories.append(new_category)
                new_category.recipes_in_category.append(new_recipe)
                new_category.save()
                new_recipe.save()
        if category3 != "":
            if models.Category.query.filter_by(category_name = category3).first():
                category3 = models.Category.query.filter_by(category_name = category3).first()
                new_recipe.categories.append(category3)
                category3.recipes_in_category.append(new_recipe)
                category3.save()
                new_recipe.save()
            else:
                new_category = models.Category(category_name = category3)
                new_category.save()
                new_recipe.categories.append(new_category)
                new_category.recipes_in_category.append(new_recipe)
                new_category.save()
                new_recipe.save()

        return redirect(url_for('views.recipes'))
        
        
        
        


    return render_template('add_recipe.html', user = current_user, form = form)



@views.route('/courses', methods=['GET', 'POST'])
def courses():
    """
    This route take all the courses from the database and diplayed in to the courses template.
    
    """
    all_courses = models.Course.query.all()
    message_form = forms.LeaveYourMessageForm()
    
    if message_form.validate_on_submit():
        name = message_form.name.data
        content = message_form.content.data
        new_message = models.Message(name = name , content = content)
        new_message.save()
        flask.flash('Your message was send it whit success', 'success')
    
    return render_template("courses.html", user=current_user, courses = all_courses, message_form = message_form)


@views.route('/course/<int:id>', methods=['GET', 'POST'])
def course_detail(id):
    """
    This route is to access the specific description of a course inside of the courses page.
    Takes the id of the course as a parameter 
    """
    course = models.Course.query.get(id)
    course_description = course.description.split('&')
    return render_template('course_details.html', course = course, user = current_user, course_description = course_description)



@views.route('/add-course', methods=['GET', 'POST'])
def add_course():
    """
    This route was made for the administrator of the site. To add the courses to the courses section
    """
    form = forms.AddCourse()
    
   
    if form.validate_on_submit():
        name = form.name.data
        type_of_course = form.type_of_course.data
        price = form.price.data
        description = form.description.data
        

        new_course = models.Course(name_of_course = name, type_of_course = type_of_course, price = price, description = description )
        new_course.save()
        return redirect(url_for('views.courses'))
        
    return render_template('add_course.html', user = current_user, form = form)



@views.route('/delete-course/<int:id>', methods=['GET', 'POST'])
def delete_course(id):
    """
    This route is to delete a course from the courses database.
    Takes the id of the course as a parameter 
    """
    course = models.Course.query.get(id)
    course.delete()
    return redirect(url_for('views.courses'))


@views.route('/about-me')
def about_me():
    """
    This route is to display the about me section of the page
    """
    message_form = forms.LeaveYourMessageForm()
    
    if message_form.validate_on_submit():
        name = message_form.name.data
        content = message_form.content.data
        new_message = models.Message(name = name , content = content)
        new_message.save()
        flask.flash('Your message was send it whit success', 'success')
    

    return render_template('about_me.html', user = current_user, message_form = message_form)




@views.route('/messages')
def messages():
    """
    This route is to retrieve all the messages send it by users in to the send a message form. 
    """
    messages = models.Message.query.all()
    return render_template('messages.html', messages = messages, user = current_user)


@views.route('/delete-message/<int:id>', methods=['GET', 'POST'])
def delete_message(id):
    """
    This route is to delete a message from the messages list.
    Takes the id of the Message as a parameter 
    """
    message = models.Message.query.get(id)
    message.delete()
    return redirect(url_for('views.messages'))




@views.route('/suscribers')
def suscribers():
    """
    This route is to retrieve all the users that suscribe the email in to suscribe me form. 
    """
    subscribers = models.Email_user.query.all()
    return render_template('subscribers.html', subscribers = subscribers, user = current_user)



@views.route('/delete-suscriber/<int:id>', methods=['GET', 'POST'])
def delete_suscriber(id):
    """
    This route is to delete a suscriber form the suscribers list.
    Takes the id of the Suscriber as a parameter 
    """
    suscriber = models.Email_user.query.get(id)
    suscriber.delete()
    return redirect(url_for('views.suscribers'))


@views.route('/students')
def students():
    """
    This route is to retrieve all the students already register in the classes.
    
    """
    students = models.User.query.all()
    return render_template('students.html', students = students, user = current_user)




@views.route('/delete-student/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    """
    This route is to delete a student from the classes.
    Takes the id of the Student as a parameter 
    """
    student = models.User.query.get(id)
    student.delete()
    return redirect(url_for('views.students'))





@views.route('/suscribe', methods = ['GET', 'POST'])
def suscribe():
    """
    This route is to retrieve the suscribe form.
    """
    news_form = forms.LeaveYourEmailForm()
    if request.method == 'POST':
        if news_form.validate_on_submit:
            email = news_form.email.data
            new_suscriber = models.Email_user(email = email )
            new_suscriber.save()
            flash('THANKS FOR SUSCRIBE', 'success')
            return redirect(url_for('views.home'))

       

    return render_template('sendmail.html', news_form= news_form , user =  current_user)



@views.route('/delete-category/<int:id>', methods=['GET', 'POST'])
def delete_category(id):
    """
    This route is to delete a category from the recipes categories list.
    Takes the id of the category as a parameter
    only the admin of the page can acces to this. 
    """
    category = models.Category.query.get(id)
    category.delete()
    return redirect(url_for('views.recipes'))
