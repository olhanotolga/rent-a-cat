from rentacat import db

db.drop_all()
db.create_all()

from rentacat.models import User, Profile, CatSitter, CatKeeper, Request, Offer

# user_1 = User(username='admin', email='admin@rac.com', password='qwerty')
# db.session.add(user_1)

# user_2 = User(username='olha', email='olha@rac.com', password='12345qwerty')
# db.session.add(user_2)

# user_3 = User(username='third', email='third.user@email.com', password='thirduser')
# db.session.add(user_3)

# user_4 = User(username='ohh', email='test@test.com', password='testtest')
# db.session.add(user_4)

# db.session.commit()

User.query.all()
User.query.first()
# User.query.filter_by(username='olha').all()

# User.query.filter_by(username='olha').first()
# user = User.query.filter_by(username='olha').first()
# user.id

user = User.query.first()
user.user_profile

user_1 = User.query.filter_by(username='olha').first()

# ADDING PROFILES

profile_1 = Profile(name='Rory Bobich', about='Hi, I\'m Rory. I have two cats, Lucky and Ella. Lucky is very sociable, and Ella is a bit shy. We all live in Prenzlauer Berg.', address='Kollwitzstraße 58, 10435 Berlin', phone_number='01762233456', user_id=user.id)

profile_2 = Profile(name='Olha H', about='Hi, I\'m Olha. I have no cats but I love them a lot. I live in Pankow.', address='Florastraße 15, 13187 Berlin', phone_number='01762038486', user_id=user_1.id)

db.session.add(profile_1)
db.session.add(profile_2)
db.session.commit()

# PROFILE CHECKS

user.user_profile
user_1.user_profile

Profile.query.all()

profile = Profile.query.first()
profile.user_id


# delete users
# ! first delete whatever is associated with users!
# db.session.delete(user_1)
# db.session.delete(user_2)
# db.session.commit()

# cat_keeper = CatKeeper(profile_id=Profile.query.filter_by(user_id=1).first().id)
# cat_sitter = CatSitter(profile_id=Profile.query.filter_by(user_id=1).first().id)
# db.session.add(cat_keeper)
# db.session.add(cat_sitter)
# db.session.commit()
