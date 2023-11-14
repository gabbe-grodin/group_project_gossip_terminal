from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.post_model import Post

@app.route('/user/<int:id>/goss/add')
def post_show_add(id):
    data={
        "id":session["user_id"]
    }
    this_user=User.get_user_by_id(data)
    return render_template('add_one.html', this_user=this_user)

@app.route('/user/<int:id>/add_goss')
def add_post(id):

    data = {
        "user_id":id,
        "post_category":request.form["post_category"],
        "post_title":request.form["post_title"],
        "post_text":request.form["post_text"]
    }
    Post.create_terminal_post(data)
    return redirect('/user/'+str(id)+'dashboard')

@app.route('/user/<int:id>/dashboard')
def user_dashboard(id):
    data = {
        "id":id
    }

    data2={
        "id":session["user_id"]
    }
    this_user=User.get_user_by_id(data2)
    
    #get posts by user 
    user_posts = Post.get_all_posts_from_creator(data)
    #get posts by others
    others_posts = Post.get_posts_with_users()

    return render_template('dash.html', userPosts=user_posts, othersPosts= others_posts, this_user=this_user)

@app.route('/user/<int:id>/goss/<int:post_id>/view')
def view_post(id, post_id):

    user_post = Post.show_one_post_w_creator(post_id)
    return render_template('view_one.html' , post= user_post)


@app.route('/user/<int:id>/goss/<int:post_id>/edit')
def show_edit_post(id,post_id):

    user_post = Post.show_one_post_w_creator(post_id)
    return render_template('edit_one.html' , post= user_post)

@app.route('/user/<int:id>/goss/<int:post_id>/update')
def update_post(id,post_id):
    data = {
        "id":id,
        "post_category":request.form["post_category"],
        "post_title":request.form["post_title"],
        "post_text":request.form["post_text"]
    }
    Post.update_post_info(data)
    return redirect('/user/'+str(id)+'/goss/'+str(post_id)+'/view')
