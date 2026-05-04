from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGBLOB
from datetime import datetime
from zoneinfo import ZoneInfo

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # ФИО преподавателя
    full_name = db.Column(db.String(255), nullable=False)
    # Должность
    position = db.Column(db.String(255), nullable=False)

    # Пока без авторизации
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))

    isAdmin = db.Column(db.Boolean, default=False)

    acknowledgements = db.relationship(
        "Acknowledgement",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.full_name}>"


class Methodichka(db.Model):
    __tablename__ = "methodichka"

    id = db.Column(db.Integer, primary_key=True)

    # Номер темы
    number_theme = db.Column(db.String(255), nullable=False)

    # Название темы
    title = db.Column(db.String(255), nullable=False)

    # Автор темы
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Рецензент
    recenzent_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Имя файла
    filename = db.Column(db.String(255), nullable=False)

    # MIME тип
    mime_type = db.Column(
        db.String(255),
        default="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    # Сам файл Word
    file_data = db.Column(LONGBLOB, nullable=False)

    # Дата публикации
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Irkutsk")))

    # Замечания / комментарии
    notes = db.Column(db.Text)

    acknowledgements = db.relationship(
        "Acknowledgement",
        back_populates="metod",
        cascade="all, delete-orphan"
        )
    # Связь с автором
    author = db.relationship(
        "User",
        foreign_keys=[author_id],
        backref="author_metods"
    )
    recenzent = db.relationship(
        "User",
        foreign_keys=[recenzent_id],
        backref="recenzent_metods"
    )
    def __repr__(self):
        return f"<Methodichka {self.title}>"


class Acknowledgement(db.Model):
    """
    Галочка ознакомления
    """

    __tablename__ = "acknowledgements"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    metod_id = db.Column(
        db.Integer,
        db.ForeignKey("methodichka.id"),
        nullable=False
    )

    # Когда поставлена галочка
    acknowledged_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(ZoneInfo("Asia/Irkutsk")))

    user = db.relationship(
        "User",
        back_populates="acknowledgements"
    )

    metod = db.relationship(
        "Methodichka",
        foreign_keys=[metod_id],
        back_populates="acknowledgements"
    )

    # Один пользователь = одна галочка
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "metod_id",
            name="unique_user_metod_ack"
        ),
    )

    def __repr__(self):
        return (
            f"<Acknowledgement "
            f"user={self.user_id} "
            f"metod={self.metod_id}>"
        )