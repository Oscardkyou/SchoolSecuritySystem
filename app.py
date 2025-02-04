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
import watchtower
import boto3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CloudWatch handler in production
if os.getenv('FLASK_ENV') == 'production':
    cloudwatch = watchtower.CloudWatchLogHandler(
        log_group='dev-flask-selfie-onboarding-service',
        stream_name=datetime.now().strftime('%Y-%m-%d'),
        boto3_client=boto3.client('logs', region_name='eu-west-1')
    )
    logger.addHandler(cloudwatch)

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database setup
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/generate_link', methods=['POST'])
def generate_link():
    try:
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
        logger.info(f"Generated link for parent: {parent_data['parent_name']} {parent_data['parent_surname']}")
        return jsonify({'link': url_for('onboarding', unique_id=unique_id, _external=True)})
    except Exception as e:
        logger.error(f"Error generating link: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/onboarding/<unique_id>', methods=['GET', 'POST'])
def onboarding(unique_id):
    try:
        parent = db_session.query(Parent).filter(Parent.unique_id == unique_id).first()
        if not parent:
            logger.warning(f"Invalid unique_id accessed: {unique_id}")
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
            logger.info(f"Photo uploaded for parent: {parent.parent_name} {parent.parent_surname}")
            return "Photo uploaded successfully!", 200

        return render_template('onboarding.html', parent=parent)
    except Exception as e:
        logger.error(f"Error in onboarding: {str(e)}")
        return str(e), 500

@app.route('/')
def admin():
    parents = db_session.query(Parent).all()
    return render_template('admin.html', parents=parents)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run(debug=True, host='0.0.0.0', port=5000)
