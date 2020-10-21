# # -*- coding: utf-8 -*-
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
