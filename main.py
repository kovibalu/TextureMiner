import os
import subprocess as sp
import django as dj

from PIL import Image

import svgwrite


dirpath = 'd:/Cornell/OpenSurfaces/synthesizability_code/results/'
opensurfacespath = 'd:/Cornell/OpenSurfaces/'
photospath = 'photos/'
svgpath = 'svg/'


def getFileLines(fpath):
    f = open(fpath, 'r')
    lines = f.read().splitlines()
    f.close()

    return lines


def parseResFile(fpath):
    lines = filter(lambda l: len(l) != 0, getFileLines(fpath))
    n = int(lines[0])
    res = []
    for i in range(n):
        currind = 7 * i + 1
        res.append({'synscore': float(lines[currind]), 'col': int(lines[currind + 1]), 'row': int(lines[currind + 2]),
                    'width': int(lines[currind + 3]), 'height': int(lines[currind + 4]),
                    'vari': float(lines[currind + 5]),
                    'features': lines[currind + 6]})

    return res


def writeResultsToSvg(imgname, results):
    impath = '../' + photospath + imgname + '.jpg'
    imgw, imgh = Image.open(impath).size
    # set the viewbox so that we will have a coordinate system based on the image size
    dwg = svgwrite.Drawing(opensurfacespath + svgpath + imgname + '.svg',
                           viewBox='0 0 {} {}'.format(imgw, imgh), width='100%', height='100%')
    dwg.add(dwg.image(href=impath,
                      insert=(0, 0),
                      width=imgw,
                      height=imgh))

    i = 0
    rescount = len(results)
    for res in results:
        dwg.add(dwg.rect(insert=(res['col'], res['row']),
                         size=(res['width'], res['height']),
                         stroke_width="5",
                         stroke="rgb({}, 0, 0)".format(int(255.0*(rescount-i)/rescount)),
                         fill="none"))
        text = dwg.text(text='{:.2f}'.format(res['synscore']),
                        insert=(res['col'], res['row'] - 3),
                        fill="red")
        text.attribs['font-size'] = 30
        dwg.add(text)
        i += 1

    dwg.save()


def callMatLab():
    sp.call(['.~/Desktop/matlab -nojvm -nodisplay -nosplash -r "myfun(10,30)"'])


def main():
    children = os.listdir(dirpath)
    for c in children:
        parts = os.path.splitext(c)
        if parts[1] == '.txt':
            res = parseResFile(dirpath + c)
            writeResultsToSvg(parts[0].split('-')[0], res)

    print 'Django version: {}'.format(dj.get_version())


main()