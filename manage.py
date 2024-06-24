from app import create_app, db
from app.models.Tickets import Tickets
from app.models.User import User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Test': Tickets, 'User': User}


if __name__ == "__main__":
    app.run(debug=True)
