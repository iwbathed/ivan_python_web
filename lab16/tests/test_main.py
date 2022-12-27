

import pytest
from flask_login import current_user
from app import create_app, db


@pytest.fixture()
def app():
    app = create_app(config_name='test')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def logged_in_user(client):
    with client:
        client.post('/register',
                    data={'username': 'test', 'email': 'testmail@email.com', 'password': 'qwe123',
                                            "confirm_password": 'qwe123'},
                    follow_redirects=True)
        client.post('/login',
                    data={'email': 'testmail@email.com', 'password': 'qwe123', 'remember': 'y'},
                    follow_redirects=True)


@pytest.fixture
def create_cat(client, logged_in_user):
    with client:
        client.post('/task/category/create',
                    data={'name': 'homework'},
                    follow_redirects=True)


@pytest.fixture
def create_task(client, logged_in_user, create_cat):
    data = {
        'title': 'Test task',
        'description': 'task desc',
        'deadline': '2022-12-20',
        'priority': 1,
        'progress': 1,
        'category': 1
    }
    with client:
        client.post('/task/create', data=data,
                           follow_redirects=True)


def test_setup(client):
    assert client is not None


def test_index(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'About' in response.data


def test_user_register_login(client):
    with client:
        resp = client.post('/register',
                           data={'username': 'test', 'email': 'testmail@email.com', 'password': 'qwe123',
                                 "confirm_password": 'qwe123'},
                           follow_redirects=True)
        assert resp.status_code == 200
        assert 'login' in resp.get_data(as_text=True)
        resp = client.post('/login',
                           data={'email': 'testmail@email.com', 'password': 'qwe123', 'remember': 'y'},
                           follow_redirects=True)
        assert resp.status_code == 200
        assert current_user.username == "test"
        resp = client.get('/logout', follow_redirects=True)
        assert resp.status_code == 200
        assert current_user.is_anonymous

    # Testing Task model


def test_task_create(client, create_cat):
    data = {
        'title': 'Test task',
        'description': 'task desc',
        'deadline': '2022-12-20',
        'priority': 1,
        'progress': 1,
        'category': 1
    }
    resp = client.post('/task/create', data=data,
                       follow_redirects=True)

    assert "Task successfully added" in resp.get_data(as_text=True)


def test_list_tasks(client, create_task):
    resp = client.get('/task/', follow_redirects=True)

    assert 'Test task' in resp.get_data(as_text=True)
    assert 'task desc' not in resp.get_data(as_text=True)


def test_detail_task(client, create_task):
    resp = client.get('/task/1', follow_redirects=True)
    assert 'task desc' in resp.get_data(as_text=True)


def test_task_update(client, create_task):
    data = {
        'title': 'Test task2',
        'description': 'task desc2',
        'deadline': '2022-12-15',
        'priority': 2,
        'progress': 2,
        'category': 1
    }
    resp = client.post('/task/1/update', data=data, follow_redirects=True)
    assert 'task desc2' in resp.get_data(as_text=True)


def test_task_delete(client, create_task):
    resp = client.post('/task/1/delete', follow_redirects=True)
    assert 'Successfully deleted!' in resp.get_data(as_text=True)


def test_category_create(client, create_cat):
    resp = client.post('/task/category/create',
                            data={'name': 'main'},
                            follow_redirects=True)

    assert "Category successfully added" in resp.get_data(as_text=True)


def test_list_category(client, create_cat):
    resp = client.get('/task/category/', follow_redirects=True)

    assert 'homework' in resp.get_data(as_text=True)
    assert 'Category detail' not in resp.get_data(as_text=True)


def test_detail_category(client, create_cat):
    resp = client.get('task/category/1', follow_redirects=True)
    assert 'Category detail' in resp.get_data(as_text=True)


def test_category_update(client, create_cat):
    data = {
        'name': 'main_category',
    }
    resp = client.post('/task/category/1/update', data=data, follow_redirects=True)
    assert 'main_category' in resp.get_data(as_text=True)


def test_category_delete(client, create_cat):
    resp = client.post('/task/category/1/delete', follow_redirects=True)
    assert 'Successfully deleted!' in resp.get_data(as_text=True)


