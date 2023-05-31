from flask_app import app
from flask import render_template, redirect, request, session, jsonify
from flask_app.models.user import User
from flask_app.models.book import Book
from flask_app.models.like import Like
from flask_app.models.comment import Comment
from flask_app.models.blacklist import Blacklist

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        all_books = Book.get_all()
        if all_books == 'No Books Yet' :
            all_books=[]
        posted_books_id = Book.get_books_id_by_user({'id' : session['user_id']})
        logged_user = User.get_by_id({'id' : session['user_id']})
        liked_books_id = Like.get_books_id_for_user({'id' : session['user_id']})
        user_likes = Like.count_for_user({'user_id' : session['user_id']})
        liked_books = User.get_user_with_fav({'id' : session['user_id']})
        return render_template('dashboard.html', user = logged_user, all_books = all_books, liked_books_id = liked_books_id, user_likes=user_likes, posted_books_id=posted_books_id, liked_books=liked_books)
    return redirect('/')

@app.route('/books/api', methods=['POST'])
def api_book():
    session['api_info'] = request.get_json()
    return jsonify({'message' : 'success'})

@app.route('/books/<int:book_id>/view')
def view_book(book_id):
    if 'user_id' in session:
        book = Book.get_by_id({'id' : book_id})
        if book:
            logged_user = User.get_by_id({'id' : session['user_id']})
            creator = User.get_by_id({'id' : book.user_id})
            lovers = Book.get_book_with_fav({'id' : book_id})
            user_likes = Like.count_for_user({'user_id' : session['user_id']})
            liked_books = User.get_user_with_fav({'id' : session['user_id']})
            api_info = session['api_info']
            comments = Comment.getAllByBook({'book_id' : book_id})
            return render_template('view_book.html', liked_books=liked_books, api=api_info, book = book, user = logged_user, lovers=lovers, user_likes=user_likes, creator=creator, comments=comments)
    return redirect('/')

@app.route('/books/create', methods=['POST'])
def create_book():
    errors = Book.validate(request.form)
    if len(errors)==0:
        book_id = Book.save({**request.form, 'user_id':session['user_id']})
        Like.save({'user_id':session['user_id'], 'book_id':book_id})
        return jsonify({'errors' : []})
    return jsonify({'errors' : errors})

@app.route('/my_books')
def show_books():
    if 'user_id' in session:
        user_likes = Like.count_for_user({'user_id' : session['user_id']})
        posted_books = Book.get_books_by_user({'id' : session['user_id']})
        logged_user = User.get_by_id({'id':session['user_id']})
        liked_books = User.get_user_with_fav({'id' : session['user_id']})
        liked_books_id = Like.get_books_id_for_user({'id' : session['user_id']})
        return render_template('my_books.html', posted_books = posted_books, user = logged_user, user_likes=user_likes, liked_books=liked_books, liked_books_id=liked_books_id)
    return redirect('/')

@app.route('/books/<int:book_id>/edit')
def edit_book(book_id):
    if 'user_id' in session:
        book = Book.get_by_id({'id' : book_id})
        user = User.get_by_id({'id' : session['user_id']})
        liked_books = User.get_user_with_fav({'id' : session['user_id']})
        lovers = Book.get_book_with_fav({'id' : book_id})
        user_likes = Like.count_for_user({'user_id' : session['user_id']})
        if book:
            if book.user_id == session['user_id'] :
                return render_template('edit_book.html',liked_books=liked_books, book = book, user=user, lovers=lovers, user_likes=user_likes)
            else :
                if user.warning<1 : #TRUE MEANS IT'S HIS FIRST TIME
                    User.add_warning({'id' : session['user_id']}) #ADD A WARNING
                    ip_address = request.remote_addr
                    return render_template('hackAttempt.html', hacker=user, book_id = book.id, ip_address=ip_address)
                else:
                    #Blacklist The Hacker
                    Like.deleteByUser({'user_id' : user.id})
                    Like.deleteByBook({'book_id' : book_id})
                    Comment.deleteByUser({'user_id' : user.id})
                    Book.deleteByUser({'user_id' : user.id})
                    User.delete({'id' : user.id})
                    Blacklist.save({'email': user.email})
                    session.clear()
                    return redirect('/')
        else :
            return render_template('404.html')
    return redirect('/')

@app.route('/books/<int:book_id>/update', methods = ['POST'])
def update_book(book_id):
    errors = Book.validate(request.form)
    if len(errors)>0:
        return jsonify({'errors' : errors})
    data = {
        **request.form, 'user_id' : session['user_id'], 'id' : book_id
            }
    Book.update(data)
    return jsonify({'errors' : []})

@app.route('/books/<int:book_id>/delete')
def delete_book(book_id):
    if 'user_id' in session:
        book_to_delete = Book.get_by_id({'id' : book_id})
        if book_to_delete:
            if book_to_delete.user_id == session['user_id'] :
                Like.deleteByBook({'book_id' : book_id})
                Book.delete({'id' : book_id})
                return redirect('/dashboard')
            hacker = User.get_by_id({'id' : session['user_id']})
            if hacker.warning<1 : #TRUE MEANS IT'S HIS FIRST TIME
                User.add_warning({'id' : session['user_id']}) #ADD A WARNING
                ip_address = request.remote_addr
                return render_template('hackAttempt.html', hacker=hacker, book_id = book_id, ip_address=ip_address)
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

@app.route('/search', methods=['POST'])
def search():
    logged_user = User.get_by_id({'id':session['user_id']})
    user_likes = Like.count_for_user({'user_id' : session['user_id']})
    liked_books = User.get_user_with_fav({'id' : session['user_id']})
    liked_books_id = Like.get_books_id_for_user({'id' : session['user_id']})
    search = f"%%{request.form['search']}%%"
    data = {
        'filter' : request.form['filter'],
        'search' : search
    }
    if request.form['filter']!="poster":
        books = Book.search(data)
    else :
        books = Book.searchByPoster({'search':search})
    return render_template('search.html', books = books, user = logged_user, user_likes=user_likes, data = request.form, liked_books_id=liked_books_id, liked_books=liked_books)

