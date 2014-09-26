import os
import subprocess as sp
import colorsys
from datetime import datetime

from django.utils import timezone

from polls.models import AnnotatedImage, SubImage


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
                    'features': lines[currind + 6]})

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
            cdate = timezone.make_aware(datetime.fromtimestamp(os.path.getctime(fullfilepath)),
                                        timezone.get_default_timezone())
            # we put it if it's fresher
            if cdate > freshestdate:
                width, height, ratio, results = parseResFile(fullfilepath)
                imgname = parts[0].split('-')[0]
                ai = AnnotatedImage(name=imgname,
                                    path=photosPath + imgname + '.jpg',
                                    comp_date=cdate,
                                    width=width,
                                    height=height,
                                    ratio=ratio)
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
