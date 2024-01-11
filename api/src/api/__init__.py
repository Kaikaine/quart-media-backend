from quart import Quart
from .databse import create_tables, SessionLocal
from quart_bcrypt import Bcrypt
from api.models.User import User
from api.models.Post import Post

app = Quart(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kairidev:l0ajmyo6qbDJ@ep-autumn-flower-96499455.us-east-2.aws.neon.tech/quarticle?sslmode=require'
app.config['SECRET_KEY'] = 'secret' 
bcrypt = Bcrypt(app)

# create_tables()


from api.routes.users import users
from api.routes.posts import posts

app.register_blueprint(users)
app.register_blueprint(posts)

# app.register_blueprint(posts)

# if __name__ == '__main__':
#     app.run(debug=True)

def run() -> None:
    app.run()