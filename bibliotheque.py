from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from waitress import serve

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

books = []

# Fonction pour vérifier si l'extension de fichier est autorisée
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Page d'accueil pour afficher la liste des livres
@app.route('/')
def index():
    return render_template('index.html', books=books)

# Formulaire d'ajout de livre
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        first_published = request.form['first_published']
        category = request.form['category']
        summary = request.form['summary']
        image = request.files['image']

        # Vérifier si l'image est autorisée et la sauvegarder dans le dossier d'upload
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Ajouter le livre à la liste des livres
        book = {
            'title': title,
            'author': author,
            'year': year,
            'first_published': first_published,
            'category': category,
            'summary': summary,
            'image': filename
        }
        books.append(book)

        return redirect(url_for('index'))

    return render_template('add_book.html')

"""if __name__ == '__main__':
    app.run(debug=True)"""
    
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
