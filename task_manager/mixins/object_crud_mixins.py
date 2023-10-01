from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import DeleteView
from django.contrib import messages
from task_manager.mixins.login_mixin import UserLoginMixin
from django.views import View


class ObjectCreateView(View):
    success_url = None
    form = None
    template_name = None
    success_message = None

    def get(self, request, *args, **kwargs):
        form = self.form
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class ObjectUpdateView(UserLoginMixin, View):
    success_url = None
    model = None
    form = None
    update_url = None
    success_message = None

    def get(self, request, *args, **kwargs):
        object_id = kwargs.get('pk')
        model_object = get_object_or_404(self.model, pk=object_id)
        form = self.form(instance=model_object)
        return render(request, self.update_url, context={
            'form': form, 'object_id': object_id})

    def post(self, request, *args, **kwargs):
        object_id = kwargs.get('pk')
        model_object = get_object_or_404(self.model, pk=object_id)
        form = self.form(request.POST, instance=model_object)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            return render(
                request,
                self.update_url,
                {'form': form, 'object_id': object_id}
            )


class ObjectDeleteView(UserLoginMixin, DeleteView):
    template_name = None
    success_url = None
    model = None
    error_message = None
    success_message = None

    def post(self, request, *args, **kwargs):
        object_id = kwargs.get('pk')
        self.object = get_object_or_404(self.model, pk=object_id)
        object_tasks = self.object.executed_tasks.all()
        if object_tasks:
            messages.error(self.request, self.error_message, extra_tags='danger')
            return redirect(self.success_url)
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)

    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)
