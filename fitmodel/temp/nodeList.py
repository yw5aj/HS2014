import re

str1 = """
p.splitMeshEdge(edge=p2[132576])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[133121])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[133057])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[133024])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[132865])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[133184])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[133216])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[133248])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[133281])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[133408])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[133440])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[133473])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[133569])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[133824])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[133600])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[133633])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[133664])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[133729])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[133952])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[133984])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[134048])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[134081])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[134209])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[134240])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[134561])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[134497])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[134432])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[134625])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[134688])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[134720])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[134753])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[134881])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[134944])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[134913])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[135009])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[132577])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[132768])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[154241])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[154784])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[138497])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[132993])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[132896])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[155008])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[155040])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[155104])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[155168])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[155264])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[155296])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[155360])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[155456])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[155520])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[155584])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[155616])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[155680])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[155776])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[155840])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[155872])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[155936])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[156000])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[134400])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[154305])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[156128])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[156224])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[156256])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[156320])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[156384])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[156480])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[156512])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[156576])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[156672])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[156704])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[156768])
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.splitMeshEdge(edge=p2[156864])
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.splitMeshEdge(edge=p1[154561])    """

re.findall(r'\d{6}', str1)




str2 = """
p.collapseMeshEdge(edge=p2[153024], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[154144], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[154754], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[154786], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[138496], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[132992], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[154786], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[154850], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[154882], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[154914], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[154914], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[154978], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155010], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155010], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155042], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155074], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155138], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155170], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155170], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155202], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155266], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155298], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155330], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155330], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[134370], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155362], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155362], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155426], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155458], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155490], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155490], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155554], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155586], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155586], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155650], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155682], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[155682], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p1 = p.elemEdges
p.collapseMeshEdge(edge=p1[155746], collapseMethod=REVERSE)
p = mdb.models['PlaneStrain'].parts['finger']
p2 = p.elemEdges
p.collapseMeshEdge(edge=p2[154400], collapseMethod=REVERSE) """

re.findall(r'\d{6}', str2)