from textureminersite import utils

class AnnotatedImageViewModel:
    def __init__(self, ai):
        self.id = ai.id
        self.name = ai.name
        self.path = ai.path
        self.comp_date = ai.comp_date
        self.width = ai.width
        self.height = ai.height
        self.ratio = ai.ratio
        self.resizedwidth = int(ai.width*ai.ratio)
        self.resizedheight = int(ai.height*ai.ratio)


class SubImageViewModel:
    def __init__(self, si, minsynthscore, maxsynthscore):
        self.id = si.id
        self.annotatedimage = si.annotatedimage
        self.col = si.col
        self.row = si.row
        self.width = si.width
        self.height = si.height
        self.synth_score = si.synth_score
        self.sscol = si.col
        self.ssrow = si.row - 3
        self.gmagavg = si.gmagavg
        self.r, self.g, self.b = utils.rgbheatmap(minsynthscore, maxsynthscore, si.synth_score)