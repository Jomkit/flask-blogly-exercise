from unittest import TestCase

from app import app
from models import db, User

#Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model for Users"""

    def setUp(self):
        """Clean up any existing Users."""
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_get_full_name(self):
        user = User(first_name='Test', last_name='Guy')
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.full_name, "Test Guy")