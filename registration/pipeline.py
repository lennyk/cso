from requests import request, HTTPError
from registration.models import Registrant
from django.core.files.base import ContentFile


def create_or_update_registrant(strategy, user, response, details, is_new=False, *args, **kwargs):
    registrant = Registrant.objects.get_or_create(user=user)[0]

    registrant_photo_url = None
    registrant_photo_url_params = None

    if strategy.backend.name == 'facebook':
        registrant_photo_url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        registrant_photo_url_params = {'type': 'square'}

    if registrant_photo_url:
        try:
            response = request('GET', registrant_photo_url, params=registrant_photo_url_params)
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            registrant.avatar.image.save('{0}_avatar.jpg'.format(user.username), ContentFile(response.content))
