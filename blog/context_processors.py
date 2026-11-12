import sys
from .models import Category


def global_context(request):
    """Inject categories and Python version into every template."""
    return {
        'categories': Category.objects.all(),
        'python_version': sys.version.split()[0],
    }
