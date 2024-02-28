import os
from flask_admin import Admin
from models import db, User, Planets, Characters, Favorites
from flask_admin.contrib.sqla import ModelView

#vista que incluya la tabla de favoritos
class FavoritesView(User):
    column_list = ('user.id', 'planet_id', 'character_id')

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Stars Wars Admin', template_mode='bootstrap4')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Characters, db.session))
    admin.add_view(ModelView(FavoritesView, db.session))


    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))