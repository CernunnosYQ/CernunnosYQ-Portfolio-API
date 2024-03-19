from sqlalchemy.orm import Session
import lorem

from schemas import BlogpostShow, BlogpostCreate
from db.models.blogpost import create_new_blogpost


def create_random_test_blogpost(author_id: int, db: Session) -> BlogpostShow:
    """Create random blogposts and return them as a list"""

    data = {"title": lorem.sentence(), "content": lorem.paragraph()}

    return create_new_blogpost(
        db=db, blogpost=BlogpostCreate(**data), author_id=author_id
    )


def create_random_test_blogpost_list(
    author_id: int, db: Session, quantity: int = 1
) -> list[BlogpostShow]:
    """Create random blogposts and return them as a list"""

    data = {"title": lorem.sentence(), "content": lorem.paragraph()}
    post_list = []

    for i in range(quantity):
        if i != 0:
            data["title"] = data["title"] + str(i)
        post_list.append(
            create_new_blogpost(
                db=db, blogpost=BlogpostCreate(**data), author_id=author_id
            )
        )

    return post_list
