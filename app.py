from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import uuid
from PIL import Image
from datetime import datetime
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, Parent, Photo
from config import Config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Database setup
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/generate_link', methods=['POST'])
def generate_link():
    parent_data = {
        'parent_name': request.form['parent_name'],
        'parent_surname': request.form['parent_surname'],
        'child_name': request.form['child_name']
    }
    unique_id = str(uuid.uuid4())
    parent = Parent(
        unique_id=unique_id,
        parent_name=parent_data['parent_name'],
        parent_surname=parent_data['parent_surname'],
        child_name=parent_data['child_name']
    )
    db_session.add(parent)
    db_session.commit()
    return jsonify({
        'link': url_for('onboarding', unique_id=unique_id, _external=True)
    })

@app.route('/onboarding/<unique_id>', methods=['GET', 'POST'])
def onboarding(unique_id):
    parent = db_session.query(Parent).filter(Parent.unique_id == unique_id).first()
    if not parent:
        return "Invalid link", 404

    if request.method == 'POST':
        if 'photo' not in request.files:
            return "No photo uploaded", 400

        photo = request.files['photo']
        if photo.filename == '':
            return "No photo selected", 400

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{unique_id}_{timestamp}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        image = Image.open(photo)
        image.save(filepath)

        db_photo = Photo(
            parent_id=parent.id,
            filename=filename
        )
        db_session.add(db_photo)
        db_session.commit()

        return "Photo uploaded successfully!", 200

    return render_template('onboarding.html', parent=parent)

@app.route('/')
def admin():
    parents = db_session.query(Parent).all()
    return render_template('admin.html', parents=parents)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run(debug=True, host='0.0.0.0', port=5000)
