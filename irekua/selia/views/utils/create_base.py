from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse


class SeliaCreateView(CreateView, SingleObjectMixin):
    no_permission_template = 'selia/no_permission.html'
    success_url = 'selia:home'

    def has_view_permission(self):
        return True

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def get_success_url_args(self):
        return []

    def get_chain(self):
        if 'chain' in self.request.GET:
            return self.request.GET.get('chain', None)
        else:
            return ''

    def get_new_chain(self):
        chain = self.get_chain()
        if chain != "":
            chain_arr = chain.split('|')
        else:
            chain_arr = []

        chain_str = ''
        next_url = ''
        if len(chain_arr) != 0:
            next_url = chain_arr[-1]
            chain_arr.pop(-1)
            if len(chain_arr) != 0:
                chain_str = "|".join(chain_arr)

        return chain_str, next_url

    def get_back_url(self):
        if 'back' in self.request.GET:
            chain_str = self.get_chain()
            return self.request.GET['back']+"?&chain="+chain_str
        else:
            chain_str, next_url = self.get_new_chain()

            if next_url == '':
                return self.get_success_url()
                
            return next_url+"?&chain="+chain_str

    def handle_finish_create(self,new_object=None):
        #next_url = self.request.GET.get('next', None)
        chain_str, next_url = self.get_new_chain()

        if next_url == '':
            return redirect(self.get_success_url())

        if new_object is not None:
            redirect_url = next_url+"?&chain="+chain_str+"&created_object="+str(new_object.pk)
        else:
            redirect_url = next_url+"?&chain="+chain_str

        return redirect(redirect_url)

    def get_success_url(self):
        return reverse(self.success_url, args=self.get_success_url_args())

    def post(self, *args, **kwargs):
        print(self.request.POST)
        return self.handle_create()

    def get(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

        if 'finalize' in self.request.GET:
            return self.handle_finish_create()

        return super().get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['chain'] = self.get_chain()
        context['back'] = self.get_back_url()

        return context
