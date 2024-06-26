from . import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f"Tag(id={self.id}, name='{self.name}')"

    def get_all_tags(cls):
        return Tag.query.all()
    
    def create_initial_tags():
        initial_tags = [
       'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science',
    'Electrical Engineering', 'Mechanical Engineering', 'Environmental Science', 'logistics', 'health',
    'Philosophy', 'Languages', 'Art', 'Music', 'Architecture', 'Education', 'Business', 'Game Design', 'Hospitality'
        ]
        # Check if tags already exist
        existing_tags = Tag.query.filter(Tag.name.in_(initial_tags)).all()

        # Add missing tags
        missing_tags = set(initial_tags) - set(tag.name for tag in existing_tags)
        for tag_name in missing_tags:
            new_tag = Tag(name=tag_name)
            db.session.add(new_tag)

        # Commit the changes to the database
        db.session.commit()