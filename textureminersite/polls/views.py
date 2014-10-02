from django.views import generic

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import AnnotatedImage, SubImage
from viewmodels import AnnotatedImageViewModel, SubImageViewModel, getViewModelsFromImage
from textureminersite import utils
from django.shortcuts import render_to_response
import simplejson


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
        ret = []
        for im in imgs:
            ret.append(getViewModelsFromImage(im))
        return ret


def detailView(request, im_id):
    im = AnnotatedImage.objects.get(pk=im_id)
    imvm, sivms = getViewModelsFromImage(im)
    js_data = simplejson.dumps(utils.buildFeatureDictionaryForImage(im))
    return render_to_response('polls/detail.html', {'imvm': imvm, 'sivms': sivms, 'js_data': js_data})

class ResultsView(generic.DetailView):
    model = AnnotatedImage
    context_object_name = 'image'
    template_name = 'polls/results.html'


def refresh(request):
    utils.refreshAllImages()
    return HttpResponseRedirect(reverse('polls:index'))


def cleardatabase(request):
    utils.clearDatabase()
    return HttpResponseRedirect(reverse('polls:index'))
