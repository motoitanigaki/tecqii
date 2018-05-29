from django.views.generic import ListView, DetailView
from django.db.models import Q
from tecqii.models import Tag, User, Item, UserTagRelation


class UserListView(ListView):
    model = User
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('tag'):
            context['tag'] = self.request.GET.get('tag')
        if self.request.GET.get('sns'):
            context['sns'] = self.request.GET.get('sns')
        if self.request.GET.get('location'):
            context['location'] = self.request.GET.get('location')
        if self.request.GET.get('keyword'):
            context['keyword'] = self.request.GET.get('keyword')

        return context

    def get_queryset(self):
        query = User.objects.all().order_by('contribution_count').reverse()
        if self.request.GET.get('tag'):
            user_tag_relation = UserTagRelation.objects.filter(tag__tag_id__in=self.request.GET.getlist('tag'))
            # query = query.filter(usertagrelation__tag__tag_id__iregex=r'(' + '|'.join(self.request.GET.getlist('tag')) + ')')
            # query = query.filter(tag__in=self.request.GET.getlist('tag'))
            query = query.filter(usertagrelation__tag__tag_id__iexact=self.request.GET.get('tag'))

        # filter by sns
        if self.request.GET.get('sns') == 'AN':
            query = query.exclude(twitter_screen_name='',github_login_name='',facebook_id='',linkedin_id='')
        elif self.request.GET.get('sns') == 'TW':
            query = query.exclude(twitter_screen_name='')
        elif self.request.GET.get('sns') == 'GH':
            query = query.exclude(github_login_name= '')
        elif self.request.GET.get('sns') == 'FB':
            query = query.exclude(facebook_id= '')
        elif self.request.GET.get('sns') == 'LI':
            query = query.exclude(linkedin_id= '')

        # filter by location
        if self.request.GET.get('location') == 'AV':
            query = query.exclude(location='')

        # filter by keyword
        if self.request.GET.get('keyword'):
            keyword = self.request.GET.get('keyword')
            query = query.filter(
                Q(user_id__icontains=keyword)|
                Q(name__icontains=keyword)|
                Q(description__icontains=keyword)|
                Q(organization__icontains=keyword)|
                Q(location__icontains=keyword)
            )

        return query