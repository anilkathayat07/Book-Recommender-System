from flask import Flask, render_template, request
import numpy as np
import pickle

popular_books = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similiraty_score = pickle.load(open('similiraty_score.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def page():
    return render_template('index.html',
    book_names = list(popular_books['Book-Title'].values),
    book_author = list(popular_books['Book-Author'].values),
    number_ratings = list(popular_books['Numbers-ratings'].values),
    average_ratings = list(popular_books['Average-ratings'].values),
    book_images = list(popular_books['Image-URL-M'].values),)

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similiraty_score[index])), key= lambda x:x[1], reverse=True)[1:5]
    
    books_data = []
    for i in similar_items:
        items = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        books_data.append(items)

    print(books_data)
    return render_template('/recommend.html', data=books_data)


if __name__ == '__main__':
    app.run(debug=True)

