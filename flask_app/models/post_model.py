from flask_app.config.mysqlconnection import connectToMySQL
#might need other import like flash or other classes and regex
from flask_app.models import user_model

from flask import Flask, request, session

from flask import flash

DB="group_project_terminal"

class Post:
    def __init__(self,data):
        self.id=data["id"]
        self.post_category=data["post_category"]
        self.post_title=data["post_title"]
        self.post_text=data["post_text"]
        self.user_id=data["user_id"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.creator=None
        self.comments=[]

    @classmethod
    def create_terminal_post(cls,data):

        query="""INSERT INTO posts(post_category,post_title,post_text,user_id)
        VALUES (%(post_category)s,%(post_title)s,%(post_text)s,%(user_id)s);"""

        return connectToMySQL(DB).query_db(query,data)
    
    @classmethod
    def get_all_posts_from_creator(cls,data):
        print("im here in the plant model line 32.")
        query = "SELECT * FROM posts WHERE user_id=%(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DB).query_db(query,data)
        print(results)
        # Create an empty list to append our instances of plants
        posts = []
        # Iterate over the db results and create instances of recipes with cls.
        for post in results:
            posts.append(cls(post))
        print(posts)
        return posts
    
    @classmethod
    def validate_post(cls,data):

        is_valid = True
#need to verify how we will categorize post by num or string
        if len(data["post_category"]) < 1:
            flash("Post category must be at least 2 Characters")
            is_valid = False
        if len(data["post_title"]) < 5:
            flash("Post title must be at least 5 Characters")
            is_valid = False
        if len(data["post_text"]) < 5:
            flash("Post information must be at least 5 Characters")
            is_valid = False
        
        return is_valid
    

    @classmethod
    def update_post_info(cls,post_data):
        print(post_data)

        query=""" 
        UPDATE posts 
        SET id=%(id)s,post_category=%(post_category)s, post_title=%(post_title)s, post_text=%(post_text)s
        WHERE id= %(id)s
        ;"""

        return connectToMySQL(DB).query_db(query,post_data) 



    @classmethod
    def get_posts_with_users(cls):
        query = """SELECT *  
                FROM posts 
                JOIN users
                ON posts.user_id = users.id
        ;"""
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DB).query_db(query)
        # Create an empty list to append our instances of friends
        print("results",results)
        
        posts_holder=[]
        # Iterate over the db results and create instances of plants with cls.
        for row_from_db in results:
            post_objects =cls(row_from_db) #hold all the recipe information and appends all the user information to the referenced object( if there is a where clause this goes outside of the for loop)
            
            user_data = { 
                "id" : row_from_db["users.id"],
                "first_name" : row_from_db["first_name"],
                "last_name" : row_from_db["last_name"],
                "email" : row_from_db["email"],
                "password" : row_from_db["password"],
                "created_at": row_from_db["users.created_at"],
                "updated_at": row_from_db["users.updated_at"]
            
            }
            post_objects.creator=(user_model.User(user_data))#
            posts_holder.append(post_objects)
            
        print("a",posts_holder)#recipe holder
        return posts_holder
    

    @classmethod
    def show_one_post_w_creator(cls,id):
    
        query="""SELECT * FROM posts JOIN users
        ON posts.user_id=users.id
        WHERE posts.id=%(id)s;"""

        results = connectToMySQL(DB).query_db(query,{'id': id})
        print(results[0])


        # Iterate over the db results and create instances of friends with cls.
        one_post_holder=cls(results[0])
        #hold all the recipe information and appends all the user information to the referenced object(where clause goes outside of the for loop)
        for row_from_db in results:

            user_data_results = { 
                "id" : row_from_db["users.id"],
                "first_name" : row_from_db["first_name"],
                "last_name" : row_from_db["last_name"],
                "email" : row_from_db["email"],
                "password" : row_from_db["password"],
                "created_at": row_from_db["users.created_at"],
                "updated_at": row_from_db["users.updated_at"]

                }
            one_post_holder.creator=(user_model.User(user_data_results))#the right side replaces "None" in the constructor method, One_recipe_holder follows the same constructor method, but is named differently then the user data is replaced when we get the query results back with the user information



            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",one_post_holder)#recipe holder
        return one_post_holder

    @classmethod
    def delete_post(cls,id):
        query="""Delete FROM posts WHERE id=%(id)s;"""
        return connectToMySQL(DB).query_db(query,id)
    
    @staticmethod
    def validate_post(data):
        is_valid = True
        
        if len(data["post_title"]) < 3 or len(data["post_title"]) > 100:
            flash("Goss name must be between 3 to 100 characters")
            is_valid = False
        
        if len(data["post_text"]) < 3 :
            flash("Goss description text must have more than 3 characters")
            is_valid = False

        return is_valid