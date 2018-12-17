from django.core.exceptions import ImproperlyConfigured

class WhiteLabelTemplateOverrideMixin(object):
    def get_template_names(self):
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            brand = self.request.brand
            return [
                "{0}/{1}".format(brand, self.template_name),
                self.template_name
            ]
