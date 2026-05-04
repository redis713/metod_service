import io
from flask import Flask, render_template, request, flash, send_file, redirect, url_for, Response, session
from flask_migrate import Migrate
from config import Config
from models import db, Methodichka, User, Acknowledgement
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
#csrf = CSRFProtect(app)



@app.route("/")
def index():

    all_metods = Methodichka.query.all()
    return render_template("index.html", all_metods=all_metods)

@app.route("/add_metod", methods=["GET", "POST"])
def add_metod():

    if request.method == "POST":
        number_theme = request.form.get("number_theme")
        title = request.form.get("title")
        author_id = request.form.get("author_id")
        recenzent_id = request.form.get("recenzent_id")
        notes = request.form.get("notes")

        uploaded_file = request.files.get("file")

        metod = Methodichka(
            number_theme=number_theme,
            title=title,
            author_id=author_id,
            recenzent_id=recenzent_id,
            filename=uploaded_file.filename,
            mime_type=uploaded_file.mimetype,
            file_data=uploaded_file.read(),
            notes=notes
        )

        db.session.add(metod)
        db.session.commit()

        return redirect(url_for("index"))

    users = User.query.order_by(User.full_name).all()
    return render_template("add_metod.html", users=users)


@app.route('/open_metod/<int:metod_id>', methods=['GET', 'POST'])
def open_metod(metod_id):
    metod = Methodichka.query.get(metod_id)

    if request.method == 'POST':
        print('изменение метода')
        metod.number_theme = request.form['number_theme']
        metod.title = request.form['title']
        metod.author_id = request.form['author_id']
        metod.recenzent_id = request.form['recenzent_id']
        metod.notes = request.form['notes']

        uploaded_file = request.files.get("file")


        if uploaded_file.mimetype != 'application/octet-stream':
            metod.mime_type = uploaded_file.mimetype
            metod.filename = uploaded_file.filename
            metod.file_data = uploaded_file.read()
            metod.uploaded_at = datetime.now(ZoneInfo("Asia/Irkutsk"))

            Acknowledgement.query.filter_by(
                metod_id=metod.id
            ).delete()

        #print("1111111111111111111111")
        #print(uploaded_file)
        #print(uploaded_file.mimetype)
        #print(uploaded_file.read())
        db.session.commit()

        return redirect(url_for("open_metod", metod_id=metod_id))
        #    db.session.commit(metod_id)
        #    return redirect(url_for('users_list'))



    users = User.query.order_by(User.full_name).all()
    author_name = User.query.get(metod.author_id).full_name
    recenzent_name = User.query.get(metod.recenzent_id).full_name
    acknowledgements = {
        ack.user_id: ack
        for ack in metod.acknowledgements
    }

    return render_template('open_metod.html', users=users, metod=metod, author_name=author_name, recenzent_name=recenzent_name, acknowledgements=acknowledgements)

'''
@app.route("/open_metod/<int:metod_id>/ack/<int:user_id>")
def acknowledge_metod(metod_id, user_id):

    existing = Acknowledgement.query.filter_by(
        metod_id=metod_id,
        user_id=user_id
    ).first()

    if existing:
        return redirect(url_for(
            "open_metod",
            metod_id=metod_id
        ))

    ack = Acknowledgement(
        metod_id=metod_id,
        user_id=user_id
    )

    db.session.add(ack)
    db.session.commit()

    return redirect(url_for(
        "open_metod",
        metod_id=metod_id
    ))
'''

@app.route("/ack/<int:metod_id>", methods=["POST"])
def acknowledge(metod_id):

    user = get_current_user()
    if not user:
        return "Не авторизован", 403

    existing = Acknowledgement.query.filter_by(
        user_id=user.id,
        metod_id=metod_id
    ).first()

    if not existing:
        ack = Acknowledgement(
            user_id=user.id,
            metod_id=metod_id,
            acknowledged_at=datetime.now(ZoneInfo('Asia/Irkutsk'))
        )
        db.session.add(ack)
        db.session.commit()

    return redirect(request.referrer)


@app.route('/delete/<int:metod_id>', methods=['GET', 'POST'])
def delete_metod(metod_id):
    metod = Methodichka.query.get(metod_id)
    db.session.delete(metod)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/open_metod/<int:metod_id>/file/<filename>', methods=['GET', 'POST'])
def get_file(metod_id, filename):
    metod = Methodichka.query.get_or_404(metod_id)
    print(metod.filename)
    return send_file(
        io.BytesIO(metod.file_data),
        mimetype=metod.mime_type,
        as_attachment=False,
        download_name=filename
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        print(login, password)

        user = User.query.filter_by(login=login).first()

        print(user)

        if user and user.password == password:
            session["user_id"] = user.id
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


def get_current_user():
    user_id = session.get("user_id")
    if user_id:
        print('userid', user_id)
        return User.query.get(user_id)
    print('нет никого')
    return None

@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())


if __name__ == '__main__':
    #with app.app_context():
    #    db.create_all()
    app.run(debug=False)