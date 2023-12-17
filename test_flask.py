from unittest import TestCase

from app import app 
from models import db, User, Post

#Use test db, and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors real, instead of HTML pages w/ error info
app.config['TESTING'] = True

# Don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for view functions for users"""

    def setUp(self):
        """Add sample user"""

        # Clean up any existing users
        User.query.delete()

        user = User(first_name='Test', last_name='Guy', image_url="https://images.pexels.com/photos/3756616/pexels-photo-3756616.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertIn('<h1 class="mb-4">Blogly Recent Posts</h1>', html)
            self.assertEqual(resp.status_code, 200)

    def test_not_found(self):
        with app.test_client() as client:
            resp = client.get(f"/users/100000")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 404)
            self.assertIn("<title>404 - Not Found</title>", html)

#####################USER ROUTE TESTS######################

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Guy', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>Test Guy</h3>', html)

    def test_show_edit_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit a User</h1>', html)

    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/edit', data={'firstName': 'John', 'lastName':'Doe', 'imageUrl':''}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            # Check status code, user information is on page, and flash 
            # messaging is behaving as expected
            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)
            self.assertIn('<p class="alert alert-success text-center py-1">User updated!</p>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<ul>\n    \n</ul>', html)
            self.assertIn('<p class="alert alert-danger text-center py-1">User Deleted!</p>', html)

    def test_show_create_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a User</h1>', html)

    def test_create_user(self):
        with app.test_client() as client:
            resp = client.post('/users/new', data={'firstName': 'John', 'lastName':'Doe', 'imageUrl':''}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Guy', html)
            self.assertIn('John Doe', html)
            self.assertIn('<p class="alert alert-success text-center py-1">New user created!</p>', html)

#####################POSTS ROUTES TESTS########################
class PostViewsTestCase(TestCase):
    """Tests for view functions for users"""

    def setUp(self):
        """Add sample user"""

        # Clean up any existing users
        User.query.delete()
        Post.query.delete()

        user = User(first_name='Test', last_name='Guy', image_url="https://images.pexels.com/photos/3756616/pexels-photo-3756616.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2")

        db.session.add(user)
        db.session.commit()

        p1 = Post(title='Test1', content="Test Guy's test stuff", user_id=user.id)
        p2 = Post(title='Test2', content="Test Guy's second test stuff", user_id=user.id)
        p3 = Post(title='Test3', content="Test Guy's third test stuff", user_id=user.id)

        db.session.add_all([p1, p2, p3])
        db.session.commit()

        self.user_id = user.id
        self.post_id = p1.id

    def tearDown(self):
        db.session.rollback()


    def test_show_new_post_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Add Post for Test Guy</h1>", html)
            self.assertIn('<label for="title" class="form-label">Title</label>', html)

    def test_create_new_post(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/posts/new", data={'title':'newTest', 'content':'This is a new test post for Test Guy', 'user_id':1}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>Test Guy</h3>', html)
            self.assertIn('<p class="alert alert-success text-center py-1">Posted!</p>', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test1', html)
            self.assertIn("<p>Test Guy&#39;s test stuff</p>", html)

    def test_show_post_edit_form(self):
        with app.test_client() as client:
            resp = client.get(f'posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit a Post</h1>', html)

    def test_edit_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/edit', data={'title': 'EditTest', 'content':'This is a test that a post was edited'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('EditTest', html)
            self.assertIn('<p>This is a test that a post was edited</p>', html)
            self.assertIn('<p class="alert alert-success text-center py-1">Post updated!</p>', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p class="alert alert-danger text-center py-1">Post deleted!</p>', html)