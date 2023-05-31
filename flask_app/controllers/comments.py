
from flask_app import app
from flask import request, session, jsonify, redirect, render_template
from flask_app.models.user import User
from flask_app.models.book import Book
from flask_app.models.like import Like
from flask_app.models.comment import Comment
from flask_app.models.blacklist import Blacklist

@app.route('/comments/create', methods = ['POST'])
def create_comment():
    status = 'Fail'
    if Comment.validate(request.form):
        data = {
            **request.form,'user_id' : session['user_id']
        }
        Comment.save(data)
        status = request.form['book_id']
    return jsonify({'status' : status})

@app.route('/comments/<int:comment_id>/delete')
def delete_comment(comment_id):
    if 'user_id' in session:
        comment = Comment.getById({'id' : comment_id})
        if comment :
            if comment.user_id == session['user_id']:
                Comment.delete({'id' : comment_id})
                return redirect(f'/books/{comment.book_id}/view')
            else :
                hacker = User.get_by_id({'id' : session['user_id']})
                if hacker.warning<1 : #TRUE MEANS IT'S HIS FIRST TIME
                    User.add_warning({'id' : session['user_id']}) #ADD A WARNING
                    ip_address = request.remote_addr
                    return render_template('hackAttempt.html', hacker=hacker, book_id = comment.book_id, ip_address=ip_address)
                else:
                    #Blacklist The Hacker
                    Like.deleteByUser({'user_id' : hacker.id})
                    Comment.deleteByUser({'user_id' : hacker.id})
                    Book.deleteByUser({'user_id' : hacker.id})
                    User.delete({'id' : hacker.id})
                    Blacklist.save({'email': hacker.email})
                    session.clear()
                    return redirect('/')
        else :
            return render_template('404.html')
    return redirect('/')
        


