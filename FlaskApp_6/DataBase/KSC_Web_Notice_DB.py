from DataBase.KSC_Web_DB import db

class Question_2(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    letter = db.Column(db.Text(), nullable = False)
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    letter = db.Column(db.Text, nullable=False)
    question = db.relationship('Question_2', backref=db.backref('answers', lazy=True))
    question_id = db.Column(db.Integer, db.ForeignKey('question_2.id'), nullable=False)