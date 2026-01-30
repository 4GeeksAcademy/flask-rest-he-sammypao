from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, Enum
import enum

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(250), nullable=False)
    firstname: Mapped[str] = mapped_column(String(250), nullable=False)
    lastname: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Follower(db.Model):
    __tablename__ = 'followers'

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    def serialize(self):
        return{
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }
    

class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    User_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    def serialize(self):
        return {
            "id": self.id,
            "User_id": self.User_id
        }


class MediaTypeEnum(enum.Enum):
    image = "image"
    video = "video"

class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaTypeEnum] = mapped_column(Enum(MediaTypeEnum))
    Url: Mapped[str] = mapped_column(String(250))
    Post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type.value if self.type else None,
            "Url": self.Url,
            "Post_id": self.Post_id
        }
    

class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    Comment_text: Mapped[str] = mapped_column(String(250))
    autor_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    Post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    def serialize(self):
        return {
            "id": self.id,
            "Comment_text": self.Comment_text,
            "autor_id": self.autor_id,
            "Post_id": self.Post_id
        }
    
    