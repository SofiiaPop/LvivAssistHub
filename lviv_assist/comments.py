
import sqlite3
from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import QueuePool
from flask_login import login_required

app = Flask(__name__)

engine = create_engine('sqlite:///commen.db', poolclass=QueuePool)

Base = declarative_base()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    name_from = Column(String)
    name_to = Column(String)
    surname_to = Column(String)
    email_to = Column(String)
    description = Column(String)
    comment = Column(String)

def add_comment(name_from, name_to, surname_to, email_to, description, comment):
    Session = sessionmaker(bind=engine)
    session = Session()
    existing_comments = get_comments(name_from, email_to, description)
    for existing_comment in existing_comments:
        if existing_comment.comment == comment:
            session.close()
            return None
    new_comment = Comment(
        name_from=name_from,
        name_to=name_to,
        surname_to=surname_to,
        email_to=email_to,
        comment=comment,
        description = description
    )
    session.add(new_comment)
    session.commit()
    return new_comment

def get_comments(name_from, email_to, description):
    Session = sessionmaker(bind=engine)
    session = Session()
    comments_table = session.query(Comment)
    if name_from is None:
        return comments_table.filter(Comment.email_to == email_to, Comment.description == description).all()
    comments = comments_table.filter(Comment.name_from == name_from,
                                      Comment.email_to == email_to,
                                      Comment.description == description).all()
    comments = [comment for comment in comments if comment.comment is not None]
    session.close()
    return comments

Base.metadata.create_all(engine)
