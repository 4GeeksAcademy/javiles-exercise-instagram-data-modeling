import os
import sys
from sqlalchemy import ( Column, ForeignKey, Integer, String, Text, DateTime, Enum, create_engine)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from eralchemy2 import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    email = Column(String(320), nullable=False)
    password = Column(String(30), nullable=False)
    full_name = Column(String(255))
    state = Column(Enum("Online", "Offline", name="state_enum"), server_default="Offline")

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    followers = relationship("Following", back_populates="follower", foreign_keys=["Following.follower_id"])
    followed = relationship("Following", back_populates="followed", foreign_keys=["Following.followed_id"])
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    saved_posts = relationship("Saved", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(Text)
    creation_date = Column(DateTime, server_default=func.now())
    number_likes = Column(Integer, default=0)
    number_comments = Column(Integer, default=0)
    number_saved = Column(Integer, default=0)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    saved = relationship("Saved", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(String(280))
    creation_date = Column(DateTime, server_default=func.now())

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")


class Following(Base):
    __tablename__ = 'following'
    id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    creation_date = Column(DateTime, server_default=func.now())

    follower = relationship(
        "User", back_populates="followers", foreign_keys=[follower_id])
    followed = relationship(
        "User", back_populates="followed", foreign_keys=[followed_id])


class Like(Base):
    __tablename__ = 'post_like'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    creation_date = Column(DateTime, server_default=func.now())

    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")


class Saved(Base):
    __tablename__ = 'saved'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    creation_date = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="saved_posts")
    post = relationship("Post", back_populates="saved")

    def to_dict(self):
        return {}


try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e