import re
import unicodedata

from django.utils.encoding import force_text
from django.utils.safestring import mark_safe


class Slugger:
    @staticmethod
    def slugify(value):
        """
        Custom slugify function:

        Convert to ASCII.
        Convert characters that aren't alphanumerics, underscores,
        or hyphens to hyphens
        Convert to lowercase.
        Strip leading and trailing whitespace.

        Unfortunately it is necessary to create wheel 2.0 in this situation
        because using django's standard slugify() function means that
        '1/2 Foo Street' and '12 Foo Street' both slugify to '12-foo-street'.
        This ensures that
        '1/2 Foo Street' becomes '1-2-foo-street' and
        '12 Foo Street' becomes '12-foo-street'

        This means we can avoid appending an arbitrary number and minimise
        disruption to the public URL schema if a council provides updated data
        """
        value = force_text(value)
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
        value = re.sub(r"[^\w\s-]", "-", value).strip().lower()
        return mark_safe(re.sub(r"[-\s]+", "-", value))
