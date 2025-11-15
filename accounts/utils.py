from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Use this for function-based views
never_cache_page = never_cache

# For class-based views we can use @method_decorator(never_cache)
