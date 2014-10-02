from django.views import generic

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import AnnotatedImage, SubImage
from viewmodels import AnnotatedImageViewModel, SubImageViewModel, getViewModelsFromImage
from textureminersite import utils
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import simplejson


# Create your views here.
# def index(request):
# latest_image_list = AnnotatedImage.objects.order_by('-comp_date')[:5]
# context = {'latest_image_list': latest_image_list}
# return render(request, 'polls/index.html', context)

def indexView(request):
    image_list = AnnotatedImage.objects.order_by('-comp_date')
    paginator = Paginator(image_list, 5)  # Show 5 images per page

    page = request.GET.get('page')
    try:
        imgs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        imgs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        imgs = paginator.page(paginator.num_pages)

    return render_to_response('polls/index.html', {"latest_image_list": map(lambda im : getViewModelsFromImage(im), imgs),
                              "paged_imgs" : imgs})

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
