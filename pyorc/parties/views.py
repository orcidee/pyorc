from datetime import datetime

from django.views.generic import DetailView, ListView

from pyorc.parties.models import Party


class PartyDetailView(DetailView):
    """
    Class based view => https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/
    """

    model = Party


class PartyListView(ListView):
    """
    Class based view => https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/#listview
    """

    model = Party

    def get_queryset(self):
        """
        Get parties of this year
        """
        return super().get_queryset().filter(year=datetime.now().year)
