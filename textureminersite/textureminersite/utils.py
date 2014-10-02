import os
import subprocess as sp
import colorsys
from datetime import datetime

from django.utils import timezone
from django.forms.models import model_to_dict
from polls.models import AnnotatedImage, SubImage, FeatureVector

opensurfacesRoot = 'd:/Cornell/OpenSurfaces/'
photosPath = 'photos/'
resultsPath = 'synthesizability_code/results/'


def getFileLines(fpath):
    f = open(fpath, 'r')
    lines = f.read().splitlines()
    f.close()

    return lines


def parseResFile(fpath):
    lines = filter(lambda l: len(l) != 0, getFileLines(fpath))
    n = int(lines[0])
    width = int(lines[1])
    height = int(lines[2])
    ratio = float(lines[3])
    res = []
    for i in range(n):
        currind = 7 * i + 4
        res.append({'synscore': float(lines[currind]), 'col': int(lines[currind + 1]), 'row': int(lines[currind + 2]),
                    'width': int(lines[currind + 3]), 'height': int(lines[currind + 4]),
                    'gmagavg': float(lines[currind + 5]),
                    'features': map(lambda w: float(w), filter(lambda w: len(w) != 0, lines[currind + 6].split(' ')))})

    return width, height, ratio, res


def rgbheatmap(minimum, maximum, value):
    strength = (value - minimum) / (maximum - minimum)
    return tuple([int(255 * x) for x in colorsys.hls_to_rgb(0.0, 0.5, strength)])


def callMatLab():
    sp.call(['.~/Desktop/matlab -nojvm -nodisplay -nosplash -r "myfun(10,30)"'])


def refreshAllImages():
    objs = AnnotatedImage.objects.order_by('-comp_date')
    if objs.exists():
        freshestdate = objs[0].comp_date
    else:
        freshestdate = datetime.fromtimestamp(0, timezone.get_default_timezone())

    children = os.listdir(opensurfacesRoot + resultsPath)
    for c in children:
        fullfilepath = opensurfacesRoot + resultsPath + c
        parts = os.path.splitext(c)
        if parts[1] == '.txt':
            mdate = timezone.make_aware(datetime.fromtimestamp(os.path.getmtime(fullfilepath)),
                                        timezone.get_default_timezone())
            print 'Processing {}, date: {}...'.format(c, mdate)
            # we put it if it's fresher
            if mdate > freshestdate:
                width, height, ratio, results = parseResFile(fullfilepath)
                imgname = parts[0].split('-')[0]

                # if we can find it in the database, then we update it, otherwise we create a new entity
                samenameimgs = AnnotatedImage.objects.filter(name=imgname)
                if samenameimgs.exists():
                    ai = samenameimgs[0]
                else:
                    ai = AnnotatedImage()
                    ai.name = imgname

                ai.path = photosPath + imgname + '.jpg'
                ai.comp_date = mdate
                ai.width = width
                ai.height = height
                ai.ratio = ratio
                ai.save()
                for res in results:
                    si = SubImage(annotatedimage=ai,
                                  col=res['col'],
                                  row=res['row'],
                                  width=res['width'],
                                  height=res['height'],
                                  synth_score=res['synscore'],
                                  gmagavg=res['gmagavg'])
                    si.save()
                    fv = FeatureVector(subimage=si,
                                        textureness=res['features'][0],
                                        homogeneity=res['features'][1],
                                        repetitiveness=res['features'][2],
                                        irregularity=res['features'][3])
                    fv.save()


def clearDatabase():
    FeatureVector.objects.all().delete()
    SubImage.objects.all().delete()
    AnnotatedImage.objects.all().delete()

def buildFeatureDictionaryForImage(img):
    imgDic = {}
    subimageList = []
    for si in img.subimage_set.all():
        features = si.featurevector_set.all()
        siDic = model_to_dict(features[0])
        siDic.update(model_to_dict(si))
        subimageList.append(siDic)
    imgDic = model_to_dict(img)
    # get rid of the date because it's not JSON serializable
    # TODO: maybe later we want to use it, convert to timestamp?
    del imgDic['comp_date']
    imgDic.update({'subimagelist':subimageList})

    return imgDic