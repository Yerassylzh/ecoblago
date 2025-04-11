from django.http import HttpResponseNotAllowed


def check_change_allowed(view_method):
    def wrapper(self, *args, **kwargs):
        if not self.context.get("change_allowed", False):
            return HttpResponseNotAllowed("You are not allowed to perform this action")
        return view_method(self, *args, **kwargs)
    return wrapper
