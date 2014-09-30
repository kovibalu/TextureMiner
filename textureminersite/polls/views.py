from django.views import generic

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import AnnotatedImage, SubImage
from viewmodels import AnnotatedImageViewModel, SubImageViewModel
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
        ret = []
        for im in imgs:
            subimgs = SubImage.objects.filter(annotatedimage=im.id)
            minsynthscore = subimgs[0].synth_score
            maxsynthscore = subimgs[len(subimgs) - 1].synth_score
            ret.append((AnnotatedImageViewModel(im),
                        map(lambda sim: SubImageViewModel(sim, minsynthscore=minsynthscore, maxsynthscore=maxsynthscore), subimgs)))
        return ret


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


def cleardatabase(request):
    utils.clearDatabase()
    return HttpResponseRedirect(reverse('polls:index'))
