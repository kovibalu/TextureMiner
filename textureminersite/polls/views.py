from django.views import generic

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import AnnotatedImage
from textureminersite import utils


# Create your views here.
# def index(request):
# latest_image_list = AnnotatedImage.objects.order_by('-comp_date')[:5]
# context = {'latest_image_list': latest_image_list}
# return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_image_list'

    def get_queryset(self):
        imgs = AnnotatedImage.objects.order_by('-comp_date')[:20]
        svgs = []
        for im in imgs:
            svgs.append((im.id, im.name, utils.writeResultsToSvg(im.id)))
        return svgs


class DetailView(generic.DetailView):
    model = AnnotatedImage
    context_object_name = 'image'
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = AnnotatedImage
    context_object_name = 'image'
    template_name = 'polls/results.html'


def refresh(request):
    utils.refreshAllImages()
    return HttpResponseRedirect(reverse('polls:index'))
