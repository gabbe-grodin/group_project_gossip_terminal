from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.post_model import Post

@app.route('/user/<int:id>/goss/add')
def post_show_add(id):

    if "user_id" not in session:
        return redirect('/login')
    data={
        "id":session["user_id"]
    }
    this_user=User.get_user_by_id(data)
    return render_template('add_one.html', this_user=this_user)

@app.route('/user/<int:id>/add_goss', methods=["POST"])
def add_post(id):
    if "user_id" not in session:
        return redirect('/login')
    
    if not Post.validate_post(request.form):
        return redirect('/user/'+str(id)+'/goss/add')
    
    data = {
        "post_category":request.form["post_category"],
        "post_title":request.form["post_title"],
        "post_text":request.form["post_text"],
        "user_id":session["user_id"]
    }
    Post.create_terminal_post(data)
    return redirect(f"/user/{id}/dashboard")
    # return redirect('/user/'+str(id)+'dashboard')

@app.route('/user/<int:id>/dashboard')
def user_dashboard(id):

    if "user_id" not in session:
        return redirect('/login')
    data = {
        "id":id
    }

    this_user=User.get_user_by_id(data)

    #get posts by user 
    user_posts = Post.get_all_posts_from_creator(data)
    #get posts by others
    others_posts = Post.get_posts_with_users()

    return render_template('dash.html', userPosts=user_posts, othersPosts= others_posts, this_user=this_user)

@app.route('/user/<int:id>/goss/<int:post_id>/view')
def view_post(id, post_id):
    if "user_id" not in session:
        return redirect('/login')
    data={
        "id":session["user_id"]
    }
    this_user=User.get_user_by_id(data)
    user_post = Post.show_one_post_w_creator(post_id)
    return render_template('view_one.html' ,post=user_post, this_user=this_user)


@app.route('/user/<int:id>/goss/<int:post_id>/edit')
def show_edit_post(id,post_id):
    if "user_id" not in session:
        return redirect('/login')
    data={
        "id":session["user_id"]
    }
    this_user=User.get_user_by_id(data)
    user_post = Post.show_one_post_w_creator(post_id)
    return render_template('edit_one.html', post=user_post, this_user=this_user)

@app.route('/user/<int:id>/goss/<int:post_id>/update', methods=['POST'])
def update_post(id,post_id):
    if "user_id" not in session:
        return redirect('/login')
    
    if not Post.validate_post(request.form):
        return redirect('/user/'+ str(id)+ '/goss/'+ str(post_id)+'/edit')
    
    data = {
        "id":post_id,
        "post_category":request.form["post_category"],
        "post_title":request.form["post_title"],
        "post_text":request.form["post_text"]
    }
    Post.update_post_info(data)
    return redirect(f"/user/{id}/dashboard")

#! delete
@app.route('/delete/<int:id>')
def delete(id):
    if "user_id" not in session:
        return redirect('/login')
    data = {"id":id}
    data2 = session['user_id']
    Post.delete_post(data)
    return redirect(f"/user/{data2}/dashboard")
