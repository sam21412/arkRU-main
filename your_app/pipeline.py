def save_steam_id(backend, user, response, *args, **kwargs):
    if backend.name == 'steam':
        user.steam_id = response.identity_url.split('/')[-1]
        user.save()

