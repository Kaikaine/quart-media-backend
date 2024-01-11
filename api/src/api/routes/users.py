from quart import Blueprint,  request, jsonify
from ..__init__ import app, db, bcrypt
from ..models.User import User
from quart_auth import login_user, logout_user, current_user, login_required

users = Blueprint('users', __name__)

@users.route("/register", methods=['POST'])
async def register():
    data = await request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {'message': 'Incomplete registration data'}, 400

    hashed_password = await bcrypt.hash_password(password)
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    await db.session.commit()

    return {'message': 'Registration successful'}, 201

@users.route("/login", methods=['POST'])
async def login():
    data = await request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {'message': 'Incomplete login data'}, 400

    user = await User.query.filter_by(email=email).first()

    if user and await bcrypt.check_password_hash(user.password, password):
        await login_user(user)
        return {'message': 'Login successful'}, 200
    else:
        return {'message': 'Login unsuccessful. Check email and password.'}, 401

@users.route("/logout", methods=['POST'])
@login_required
async def logout():
    await logout_user()
    return {'message': 'Logout successful'}, 200

@users.route("/account", methods=['GET'])
@login_required
async def account():
    return {'message': 'You are logged in as ' + current_user.username}, 200

@users.route("/edit_profile", methods=['PUT'])
@login_required
async def edit_profile():
    data = await request.get_json()
    username = data.get('username')
    email = data.get('email')
    bio = data.get('bio')

    if not username or not email:
        return {'message': 'Incomplete profile data'}, 400

    current_user.username = username
    current_user.email = email
    current_user.bio = bio
    await db.session.commit()

    return {'message': 'Profile updated successfully'}, 200

@users.route("/user/<username>", methods=['GET'])
async def user_profile(username):
    user = await User.query.filter_by(username=username).first_or_404()
    return {'username': user.username, 'email': user.email, 'bio': user.bio}, 200


@users.route("/delete_profile", methods=['DELETE'])
@login_required
async def delete_profile():
    user = current_user

    try:
        db.session.delete(user)
        await db.session.commit()

        await logout_user()

        return jsonify({'message': 'Your account has been deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500