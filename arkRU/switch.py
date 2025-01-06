from django.conf import settings
from django.utils import translation
from django.shortcuts import redirect

def switch_language(request, lang_code):
    if lang_code in dict(settings.LANGUAGES).keys():
        translation.activate(lang_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
    return redirect(request.META.get('HTTP_REFERER', '/'))