import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Table,Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Role(enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


#===============================================================================#
photos_tags = Table(
    "photos_tags",
    Base.metadata,
    Column("photo_id", ForeignKey("photos.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

#===============================================================================#


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(500), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)
    avatar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    confirmed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    #зв'язки
    photos: Mapped[list["Photo"]] = relationship(back_populates = "owner")
    comments: Mapped[list["Comment"]] = relationship(back_populates = "user")


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    #зв'язки
    owner: Mapped["User"] = relationship(back_populates="photos")
    comments: Mapped[list["Comment"]] = relationship(back_populates="photo", cascade="all, delete-orphan")
    tags: Mapped[list["Tag"]] = relationship(secondary=photos_tags, back_populates="photos")
    transformed_images: Mapped [list["TransformedImage"]] = relationship(back_populates="photo", cascade="all, delete-orphan")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    #зв'язки
    photos: Mapped[list["Photo"]] = relationship(secondary=photos_tags, back_populates="tags")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    photo_id: Mapped[int] = mapped_column(ForeignKey("photos.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    #зв'язки
    user: Mapped["User"] = relationship(back_populates="comments")
    photo: Mapped["Photo"] = relationship(back_populates="comments")

class TransformedImage(Base):
    __tablename__ = "transformed_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    photo_id: Mapped[int] = mapped_column(ForeignKey("photos.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(String(255))
    qr_code_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


    #зв'язки
    photo: Mapped["Photo"] = relationship(back_populates="transformed_images")




    

