import cv2, sys

def extractData(strs):
    tmp = [
        [x for x in map(int, s.split())]
        for s in strs.split('\n')[:-2]]
    return [ ((x[0], x[1]), (x[2] + x[0], x[1] + x[3]))
        for x in tmp
    ]

img = cv2.imread(sys.argv[1])
fdata = open(sys.argv[2]).read()
for x in extractData(fdata):
    cv2.rectangle(img, x[0], x[1], (255, 0, 0))
cv2.imwrite(sys.argv[3], img)
