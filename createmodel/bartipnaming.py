import re


def getModelNameFromBaseAndBarWidth(width, baseModelName='ps'):
    modelName = baseModelName + '_w' + str(int(width*1e5))+'_btip'
    return modelName


def getBarWidthFromModelName(modelName):
    width = int(re.findall('\d+', modelName)[0]) * 1e-5
    return width