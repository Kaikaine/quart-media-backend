# posts/routes.py
from quart import Blueprint, request
from api.__init__ import db
from api.models.Post import Post
# from api.models.User import  User
from api.models.Comment import  Comment

from quart_auth import current_user, login_required

posts = Blueprint('posts', __name__)

@posts.route("/create_post", methods=['POST'])
@login_required
async def create_post():
    data = await request.get_json()
    content = data.get('content')
    caption = data.get('caption')
    image = data.get('image')
    date_posted = data.get('date_posted')

    if not content:
        return {'message': 'Content is required for creating a post'}, 400

    post = Post(
        content=content,
        caption=caption,
        image=image,
        date_posted=date_posted,
        user_id=current_user.id
    )

    db.session.add(post)
    await db.session.commit()

    return {'message': 'Post created successfully'}, 201

@posts.route("/edit_post/<int:post_id>", methods=['PUT'])
@login_required
async def edit_post(post_id):
    data = await request.get_json()
    content = data.get('content')
    caption = data.get('caption')
    image = data.get('image')
    date_posted = data.get('date_posted')

    if not content:
        return {'message': 'Content is required for editing a post'}, 400

    post = await Post.query.get(post_id)

    if post and post.author.id == current_user.id:
        post.content = content
        post.caption = caption
        post.image = image
        post.date_posted = date_posted

        await db.session.commit()

        return {'message': 'Post edited successfully'}, 200
    else:
        return {'message': 'Post not found or unauthorized to edit.'}, 404

@posts.route("/delete_post/<int:post_id>", methods=['DELETE'])
@login_required
async def delete_post(post_id):
    post = await Post.query.get(post_id)

    if post and post.author.id == current_user.id:
        db.session.delete(post)
        await db.session.commit()

        return {'message': 'Post deleted successfully'}, 200
    else:
        return {'message': 'Post not found or unauthorized to delete.'}, 404

@posts.route("/like_post/<int:post_id>", methods=['POST'])
@login_required
async def like_post(post_id):
    post = await Post.query.get(post_id)

    if post:
        if current_user not in post.likes:
            post.likes.append(current_user)
            await db.session.commit()
            return {'message': 'Post liked successfully'}, 200
        else:
            return {'message': 'You have already liked this post'}, 400
    else:
        return {'message': 'Post not found'}, 404

@posts.route("/unlike_post/<int:post_id>", methods=['POST'])
@login_required
async def unlike_post(post_id):
    post = await Post.query.get(post_id)

    if post:
        if current_user in post.likes:
            post.likes.remove(current_user)
            await db.session.commit()
            return {'message': 'Post unliked successfully'}, 200
        else:
            return {'message': 'You have not liked this post'}, 400
    else:
        return {'message': 'Post not found'}, 404

@posts.route("/comment_post/<int:post_id>", methods=['POST'])
@login_required
async def comment_post(post_id):
    data = await request.get_json()
    content = data.get('content')

    if not content:
        return {'message': 'Content is required for commenting on a post'}, 400

    post = await Post.query.get(post_id)

    if post:
        comment = Comment(content=content, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        await db.session.commit()
        return {'message': 'Comment added successfully'}, 201
    else:
        return {'message': 'Post not found'}, 404
    