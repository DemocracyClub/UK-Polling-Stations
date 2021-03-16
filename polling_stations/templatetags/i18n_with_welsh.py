from django.template import Library
from django.templatetags import i18n
from django.utils.translation import get_language

from polling_stations.i18n.cy import MUTATIONS, WelshMutationContextHelper

register = Library()

# Start with everything in the original i18n module
register.filters.update(i18n.register.filters)
register.tags.update(i18n.register.tags)


class BlockTranslateNodeWithWelsh(i18n.BlockTranslateNode):
    """A {% blocktrans %} tag which adds extra vars for Welsh mutations.

    For a `{% blocktrans %}Contact {{ council }} today!{% endblocktrans %}` block,
    this adds `council_aspirate` etc variables to the context before deferring to the
    superclass implementation. The new context variables are only added where the
    original object supports providing Welsh mutations, as decided by
    `WelshMutationContextHelper`.

    For active languages that aren't Welsh, we immediately defer to the superclass
    implementation, so there is minimal performance penalty.

    Unfortunately this implementation isn't lazy, and all mutations are calculated
    """

    def render(self, context, nested=False):
        # Short-circuit if the current language isn't Welsh
        if get_language() != "cy":
            return super().render(context, nested)

        # Find which variables are used within the block
        _, vars = self.render_token_list(self.singular, with_mutations=False)
        # Add additional variables for each of them for all the mutations
        context.update(
            {
                f"{var}_{mutation}": WelshMutationContextHelper(context, var, mutation)
                for var in vars
                for mutation in MUTATIONS
            }
        )
        result = super().render(context, nested)
        context.pop()  # This balances the context.update(…) above
        return result

    def render_token_list(self, tokens, with_mutations=True):
        singular, vars = super().render_token_list(tokens)
        if with_mutations:
            vars += [f"{var}_{mutation}" for var in vars for mutation in MUTATIONS]
        return singular, vars


def do_block_translate(parser, token):
    # This preserves the original template-parsing behaviour, but substitutes our
    # functionality for the template node that gets returned.
    node = i18n.do_block_translate(parser, token)
    node.__class__ = BlockTranslateNodeWithWelsh
    return node


# Forwards compatibility: Django 3.1 deprecates trans and blocktrans in favour of
# translate and blocktranslate. We'll only override those that are exposed by the
# underlying i18n module, so we can keep in lockstep. When blocktrans is finally
# removed we can replace this with a `@register.tag("blocktrans")` decorator on
# `do_block_translate`.
for _tag_name in ("blocktrans", "blocktranslate"):
    if _tag_name in register.tags:
        register.tag(_tag_name, do_block_translate)
