from flask_sqlalchemy import SQLAlchemy
import os
from flask_avatars import Avatars
from flask_migrate import Migrate
# Create SQLAlchemy instances
db = SQLAlchemy()


def init_app(app):
    # Configure the Flask app
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # Ensure that templates are auto-reloaded during development

    from .user import User
    from .post import Post
    from .tag import Tag   
    from .message import Message   
    from .chat import Chat,ChatMember,ChatMessage   
    from .notification import Notification
        # Initialize the SQLAlchemy database
    db.init_app(app)
    migrate = Migrate(app, db)
    avatars = Avatars(app)

    # Create the database tables
    with app.app_context():
    
        db.create_all()
        # Tag.create_initial_tags()
   
    return app
    
    


# Function to drop SQLite database
def drop_database():
    try:
        # Drop all tables
        db.drop_all()
        # Remove the SQLite database file
                # Remove the SQLite database file
        db_file_path = 'local.db'  # Replace with your actual database file name
        if os.path.exists(db_file_path):
            db.engine.dispose()  # Close the database connection
            os.remove(db_file_path)
            print(f'Database file {db_file_path} removed successfully')
        else:
            print(f'Error: Database file {db_file_path} not found')
        
    except Exception as e:
        print(f'Error: {e}')
        


