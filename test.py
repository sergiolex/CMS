#!flask/bin/python
import os
import unittest
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for
)
from app import app, db
from app.article.models import Article
from app.authentication.models import User

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class createarticlecase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        self.app = app.test_client()
        db.create_all()
        ctx = app.app_context()
        ctx.push()
        return app


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def testarticlecreateget(self):
        test = app.test_client(self)
        response = test.get('/art/create/', content_type='html/text')
        self.assertEqual(response.status_code, 302)
        assert 'token' in session
        self.assertTrue(User.verify_token(session['token'])!=None)


    def testarticlecreatepost(self):
        user = User(username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
            )
        db.session.add(user)
        db.session.commit()
        usertest = User.query.filter(User.username == 'Testuser').first()
        new_article = Article(title='testtitle',
            body='testbody',
            created='01-01-2015',
            section_name='testname',
            section='testsection',
            user_name=usertest.username,
            user=usertest,
            )
        db.session.add(new_article)
        db.session.commit()
        test = app.test_client(self)
        self.assertTrue(response.status_code == 302)
        testsection = Sections.query.filter(Sections.title == 'title').first()
        self.assertTrue(testsection == None)


if __name__ == '__main__':
    unittest.main()
