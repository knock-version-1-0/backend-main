from rest_framework.routers import SimpleRouter

from django.urls import re_path


class Router(SimpleRouter):
    """
    Rewrite SimpleRouter to inject viewset_factory on viewset
    """

    def register(self, prefix, viewset, basename=None, factory=None):
        if basename is None:
            basename = self.get_default_basename(viewset)
        if factory is None:
            raise TypeError("The factory argument cannot be None.")
        self.registry.append((prefix, viewset, basename, factory))

        # invalidate the urls cache
        if hasattr(self, '_urls'):
            del self._urls

    def get_urls(self):
        """
        Use the registered viewsets to generate a list of URL patterns.
        """
        ret = []

        for prefix, viewset, basename, factory in self.registry:
            lookup = self.get_lookup_regex(viewset)
            routes = self.get_routes(viewset)

            for route in routes:

                # Only actions which actually exist on the viewset will be bound
                mapping = self.get_method_map(viewset, route.mapping)
                if not mapping:
                    continue

                # Build the url pattern
                regex = route.url.format(
                    prefix=prefix,
                    lookup=lookup,
                    trailing_slash=self.trailing_slash
                )

                # If there is no prefix, the first part of the url is probably
                #   controlled by project's urls.py and the router is in an app,
                #   so a slash in the beginning will (A) cause Django to give
                #   warnings and (B) generate URLS that will require using '//'.
                if not prefix and regex[:2] == '^/':
                    regex = '^' + regex[2:]

                initkwargs = route.initkwargs.copy()
                initkwargs.update({
                    'basename': basename,
                    'detail': route.detail,
                    'viewset_factory': factory
                })

                view = viewset.as_view(mapping, **initkwargs)
                name = route.name.format(basename=basename)
                ret.append(re_path(regex, view, name=name))

        return ret
