import os
import subprocess as sp
import colorsys
from datetime import datetime

from PIL import Image
import svgwrite
from django.utils import timezone

from polls.models import AnnotatedImage, SubImage


opensurfacesRoot = 'd:/Cornell/OpenSurfaces/'
photosPath = 'photos/'
resultsPath = 'synthesizability_code/results/'
max_img_res = 2000


def getFileLines(fpath):
    f = open(fpath, 'r')
    lines = f.read().splitlines()
    f.close()

    return lines


def parseResFile(fpath):
    lines = filter(lambda l: len(l) != 0, getFileLines(fpath))
    n = int(lines[0])
    ratio = float(lines[1])
    res = []
    for i in range(n):
        currind = 7 * i + 2
        res.append({'synscore': float(lines[currind]), 'col': int(lines[currind + 1]), 'row': int(lines[currind + 2]),
                    'width': int(lines[currind + 3]), 'height': int(lines[currind + 4]),
                    'gmagavg': float(lines[currind + 5]),
                    'features': lines[currind + 6]})

    return ratio, res


def rgbheatmap(minimum, maximum, value):
    strength = (value - minimum) / (maximum - minimum)
    return colorsys.hls_to_rgb(0.0, 0.5, strength)


def writeResultsToSvg(imid):
    img = AnnotatedImage.objects.get(pk=imid)
    imgw, imgh = Image.open(opensurfacesRoot + img.path).size
    resizeratio = float(max_img_res) / max(imgh, imgw)
    subimgs = SubImage.objects.filter(annotatedimage=imid)
    resizedw = int(imgw * resizeratio)
    resizedh = int(imgh * resizeratio)

    # set the viewbox so that we will have a coordinate system based on the image size
    dwg = svgwrite.Drawing('',
                           viewBox='0 0 {} {}'.format(resizedw, resizedh),
                           width='100%',
                           height='100%')
    # TODO correct paths somehow...
    dwg.add(dwg.image(href='/static/polls/' + img.path,
                      insert=(0, 0),
                      width=resizedw,
                      height=resizedh))

    rescount = len(subimgs)
    minsynthscore = subimgs[0].synth_score
    maxsynthscore = subimgs[rescount - 1].synth_score
    for si in subimgs:
        r, g, b = rgbheatmap(minsynthscore, maxsynthscore, si.synth_score)
        dwg.add(dwg.rect(insert=(si.col, si.row),
                         size=(si.width, si.height),
                         stroke_width="5",
                         stroke="rgb({}, {}, {})".format(int(r * 255), int(g * 255), int(b * 255)),
                         fill="none"))
        text = dwg.text(text='{:.2f}'.format(si.synth_score),
                        insert=(si.col, si.row - 3),
                        fill="red")
        text.attribs['font-size'] = 30
        dwg.add(text)

    return dwg.tostring()


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
                ratio, results = parseResFile(fullfilepath)
                imgname = parts[0].split('-')[0]
                ai = AnnotatedImage(name=imgname,
                                    path=photosPath + imgname + '.jpg',
                                    comp_date=cdate,
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
