from app import app, db
from app.models import User, Assignment, Submissions#, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Assignment': Assignment, 'Submissions': Submissions}#, 'Post': Post}
