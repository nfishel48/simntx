from allauth.account.adapter import DefaultAccountAdapter


class UserProfileAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        user = super(UserProfileAdapter, self).save_user(request, user, form, commit=commit)

        print(form.cleaned_data)

        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()