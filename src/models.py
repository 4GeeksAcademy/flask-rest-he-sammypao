from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Enum
from typing import List
import enum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'  

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(250), nullable=False)
    lastname: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)


    posts: Mapped[List["Post"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="author", 
        cascade="all, delete-orphan"
    )

    following: Mapped[List["Follower"]] = relationship(
        foreign_keys="[Follower.user_from_id]", 
        back_populates="follower_user",
        cascade="all, delete-orphan"
    )

    followers: Mapped[List["Follower"]] = relationship(
        foreign_keys="[Follower.user_to_id]", 
        back_populates="followed_user",
        cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }


class Follower(db.Model):
    __tablename__ = 'follower'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # RELACIONES (Se quedan igual)
    follower_user: Mapped["User"] = relationship(
        foreign_keys=[user_from_id], 
        back_populates="following"
    ) 

    followed_user: Mapped["User"] = relationship(
        foreign_keys=[user_to_id], 
        back_populates="followers"
    )   

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }
    

class Post(db.Model):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id")) 


    user: Mapped["User"] = relationship(back_populates="posts")

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post", 
        cascade="all, delete-orphan"
    )

    media: Mapped[List["Media"]] = relationship(
        back_populates="post", 
        cascade="all, delete-orphan"
    )     

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }


class MediaTypeEnum(enum.Enum):
    image = "image"
    video = "video"


class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaTypeEnum] = mapped_column(Enum(MediaTypeEnum))
    url: Mapped[str] = mapped_column(String(250))  
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id", ondelete="CASCADE"))

    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type.value if self.type else None,
            "url": self.url,
            "post_id": self.post_id
        }


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(250))  
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))  
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }