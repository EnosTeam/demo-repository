from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from DataBase import KSC_Web_Post_DB, KSC_Web_Notice_DB, KSC_Web_Sign_InUp_DB
from DataBase.KSC_Web_DB import db

admin_bp = Blueprint('admin_bp', __name__)

admin = Admin(admin_bp, name='KSC_Web_DB_Control', template_mode='bootstrap3')

class Post_ModelView(ModelView):
    column_list = ['id', 'title', 'letter']
admin.add_view(Post_ModelView(KSC_Web_Post_DB.Post, db.session, endpoint="Post"))

class Question_2_ModelView(ModelView):
    column_list = ['id', 'title', 'letter']
admin.add_view( Question_2_ModelView(KSC_Web_Notice_DB.Question_2, db.session, endpoint="question_2"))

class Answer_ModelView(ModelView):
    column_list = ['id', 'title', 'letter', 'question', 'question_id']
admin.add_view(Answer_ModelView(KSC_Web_Notice_DB.Answer, db.session, endpoint="answer"))

class User_ModelView(ModelView):
    column_list = ['id', 'username', 'password', 'email', 'birth_date', 'first_name', 'last_name']
admin.add_view(User_ModelView(KSC_Web_Sign_InUp_DB.User, db.session, endpoint="User"))