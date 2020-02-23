from django import forms


class ToggleWidget(forms.widgets.CheckboxInput):
    class Media:
        css = {'all': (
            "https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css",)}
        js = ("https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js",)

    def __init__(self, attrs=None, *args, **kwargs):
        attrs = attrs or {}

        default_options = {
            'toggle': 'toggle',
            'offstyle': 'danger'
        }
        options = kwargs.get('options', {})
        default_options.update(options)
        for key, val in default_options.items():
            attrs['data-' + key] = val

        super().__init__(attrs)


class Select2Mixin():
    class Media:
        css = {
            'all': ("https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/css/select2.min.css",)
        }
        js = ("https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/js/select2.min.js",
              'customselect2.js')

    def update_attrs(self, options, attrs):
        attrs = self.fix_class(attrs)
        multiple = options.pop('multiple', False)
        attrs['data-adapt-container-css-class'] = 'true'

        if multiple:
            attrs['multiple'] = 'true'

        for key, val in options.items():
            attrs['data-{}'.format(key)] = val

        return attrs

    def fix_class(self, attrs):
        class_name = attrs.pop('class', '')
        if class_name:
            attrs['class'] = '{} {}'.format(
                class_name, 'custom-select2-widget')
        else:
            attrs['class'] = 'custom-select2-widget'

        return attrs


class Select2Widget(Select2Mixin, forms.widgets.Select):
    def __init__(self, attrs=None, choices=(), *args, **kwargs):
        attrs = attrs or {}
        options = kwargs.pop('options', {})
        new_attrs = self.update_attrs(options, attrs)

        super().__init__(new_attrs)
        self.choices = list(choices)


class Select2MultipleWidget(Select2Mixin, forms.widgets.SelectMultiple):
    def __init__(self, attrs=None, choices=(), *args, **kwargs):

        attrs = attrs or {}
        options = kwargs.pop('options', {})
        new_attrs = self.update_attrs(options, attrs)

        super().__init__(new_attrs)
        self.choices = list(choices)