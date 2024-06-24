from sqlalchemy.orm import relationship

from app import db


class Tickets(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    configuration = db.Column(db.Text, nullable=False)
    img = db.Column(db.LargeBinary, nullable=True)
    file = db.Column(db.LargeBinary, nullable=True)

    configs = relationship('Config', backref='test', lazy=True)

    def __repr__(self):
        return f"<Tickets(id={self.id}, name={self.name}, description={self.description})>"
