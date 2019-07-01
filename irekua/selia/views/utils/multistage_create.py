import json

from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.shortcuts import reverse


class FormPhase:
    initial = {}
    form_class = None
    name = None
    next_phase = None

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy()

    def get_form_class(self):
        return self.form_class

    def get_context_name(self):
        return '{name}_form'.format(name=self.name)

    def get_context_data(self, request, **kwargs):
        context_name = self.get_context_name()
        form = kwargs.get(context_name, self.get_form(request))
        return {context_name: form}

    def get_next_phase(self):
        return self.next_phase

    def get_form(self, request, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs(request))

    def get_next_phase_html_id(self):
        return self.get_next_phase()

    def get_form_kwargs(self, request):
        kwargs = {
            'initial': self.get_initial(),
        }

        if request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': request.POST,
                'files': request.FILES,
            })
        return kwargs

    def get_form_result(self, form):
        return json.dumps(form.cleaned_data)

    def get_success_url(self, request, form):
        query = request.GET.copy()
        query['phase'] = self.get_next_phase()
        query['{}_result'.format(self.name)] = self.get_form_result(form)

        return '{path}?{query}#{id}'.format(
            path=request.path,
            query=query.urlencode(),
            id=self.get_next_phase_html_id())

    def is_valid(self, form):
        return form.is_valid()


class SeliaMultiStageCreateView(TemplateView):
    phases = {}

    def get_current_phase(self, request):
        phase = request.GET.get('phase', 'initial')
        try:
            return self.phases[phase]
        except KeyError:
            raise NotImplementedError('No initial phase was provided')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['next'] = self.request.GET.get('next', None)

        for phase in self.phases.values():
            context.update(phase.get_context_data(self.request, **kwargs))

        return context

    def post(self, request, *args, **kwargs):
        phase = self.get_current_phase(request)

        form = phase.get_form(request)
        if phase.is_valid(form):
            return redirect(phase.get_success_url(request, form))
        else:
            name = phase.get_context_name()
            kwargs = {name: form}
            return self.render_to_response(self.get_context_data(**kwargs))
