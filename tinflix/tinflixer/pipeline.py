from tinflixer.models import Tinflixer


def create_tinflixer(backend, details, response,
                     user, *args, **kwargs):
    if not Tinflixer.objects.filter(user=user).exists():
        #add update user picture, age range
        print details
        print response
        new_profile = Tinflixer(user=user, new=True)
        new_profile.save()
    obj = Tinflixer.objects.get(user=user)
    obj.high_age = response['age_range']['max']
    obj.low_age = response['age_range']['min']
    obj.picture = response['picture']['data']['url']
    if not obj.new:
        obj.email = details['email']
        obj.about_me = 'Hello!'
        obj.last_name = details['last_name']
        obj.first_name = details['first_name']
    obj.save()
    return kwargs