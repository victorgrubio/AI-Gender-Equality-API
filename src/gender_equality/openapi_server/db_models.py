# # -*- coding: utf-8 -*-
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy
# # import rq
# # import redis
# 
# db = SQLAlchemy()
# 
# 
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     password = db.Column(db.String(128))
# 
#     def __repr__(self):
#         return "<User: {}>".format(self.username)
# 
#     def set_password(self, password):
#         self.password = generate_password_hash(password)
# 
#     def check_password(self, password):
#         return check_password_hash(self.password, password)
