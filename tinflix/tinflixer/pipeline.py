from tinflixer.models import Tinflixer
def create_tinflixer(strategy, details, response, user, *args, **kwargs):
    if Tinflixer.objects.filter(user=user).exists():
        #add update user picture, age range
        pass
    else:
        new_profile = Tinflixer(user=user)
        new_profile.save()
    return kwargs