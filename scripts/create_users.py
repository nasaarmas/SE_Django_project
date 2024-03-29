import json
from django.contrib.auth import get_user_model


User = get_user_model()

with open('scripts/dataset/ex_users.json') as f:
    users = json.load(f)

for user_data in users:
    exists = User.objects.get(email=user_data['email'])
    if not exists:
        user = User(
            email=user_data['email'],
            email_activated=user_data['email_activated'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            gender=user_data['gender'],
            date_of_birth=user_data['date_of_birth'],
            #city=user_data['city'],
            status_type=user_data['status_type'],
            terms_accepted=user_data['terms_accepted'],
            terms_accepted_date=user_data['terms_accepted_date'],
        )
        user.set_password(User.objects.make_random_password())
        user.save()


