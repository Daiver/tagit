import cv2, sys

def extractRects(strs):
    tmp = [
        [x for x in map(int, s.split(' '))]
        for s in strs.split('\n')[:-2]
    ]
    return [
        ((x[0], x[1]), (x[2] + x[0], x[3] + x[1])) for x in tmp
    ]

def cutRect(img, p1, p2):
    return img[abs(p1[1]-5):p2[1] + 5, abs(p1[0] - 5): 5 + p2[0]]

if __name__ == '__main__':
    print 'hi'
    img = cv2.imread(sys.argv[1])
    
    rects = extractRects(open('tmp').read())
    for i, x in enumerate(rects): 
        #cv2.rectangle(img, x[0], x[1], (0, 255, 0))
        cv2.imwrite('dump/%s.png' % str(i), cutRect(img, x[0], x[1]))
        #cv2.imshow(str(x), cutRect(img, x[0], x[1]))
        #cv2.waitKey()
    #cv2.imshow('', img)
    #cv2.waitKey()
