from app import db


class Config(db.Model):
    __tablename__ = 'configs'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    device_name = db.Column(db.String(15), nullable=False)
    config = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Config(id={self.id}, test_id={self.test_id}, device_name={self.device_name})>"
