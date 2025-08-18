from sqlalchemy import select

from one_piece_api.models.user_model import User


def test_create_user(session):
    db_new_user = User(
        username='User Test Database', password='password.test#1234', email='testing.mydb@test'
    )
    session.add(db_new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'User Test Database'))

    assert user.username == 'User Test Database'
    assert user.email == 'testing.mydb@test'
    assert user.password == 'password.test#1234'
