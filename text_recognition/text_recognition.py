import subprocess, cv2, os
import numpy as np

def extractRects(strs):
    tmp = [
        [x for x in map(int, s.split(' '))]
        for s in strs.split('\n')[:-2]
    ]
    return [((x[0], x[1]), (x[2] + x[0], x[3] + x[1])) for x in tmp]

def callCommand(com, args):
    p = subprocess.Popen([com, args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.communicate()

def cutRect(img, p1, p2):
    return img[abs(p1[1]-5):p2[1] + 5, abs(p1[0] - 5): 5 + p2[0]]

def callCCVSWT(img_name):
    return extractRects(callCommand(os.path.join(os.path.dirname(__file__), './swtdetect'), img_name)[0])

def makeDumps(img_name, rects, dir_name):
    res = []
    img = cv2.imread(img_name)
    img2 = img.copy()
    file_name = img_name.split(os.path.sep)[-1]
    dat_file = os.path.join(dir_name, file_name + '.data')
    new_file = img_name + '.text_marked.jpg'
    with open(dat_file, 'w') as f:
        for x in rects:
            f.write(str(x) + '\n')
    for i, rect in enumerate(rects):
        to_write = cutRect(img, rect[0], rect[1])
        name = os.path.join(dir_name, '_'.join([file_name, str(i), '.png']))
        '''to_write = cv2.cvtColor(to_write, cv2.cv.CV_BGR2GRAY)
        med = np.mean(to_write)
        med = np.median(to_write)
        to_write[to_write <= med] = 0
        to_write[to_write > 0] = 255'''
        cv2.imwrite(name, to_write)
        res.append((name, i, rect))
        cv2.rectangle(img2, rect[0], rect[1], (0, 0, 255))
        cv2.imwrite(new_file, img2)
    return res

def recognizeByTesseract(img_name):
    out_file_name = img_name[:img_name.rfind('.')]
    callCommand('rm', out_file_name)
    p = subprocess.Popen('tesseract %s %s -l eng -psm 6' % (img_name, out_file_name), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out = p.communicate()
    res = None
    out_file_name += '.txt'
    with open(out_file_name) as f:
        res = f.read()
    return (out_file_name, res)

latin = {}
for i in xrange(65, 65 + 26):
    latin[chr(i)] = 1
    latin[chr(i + 32)] = 1
latin[' '] = 1

def filterText(text):
    if text == None or len(text) == 0: return None
    num_of_latin = 0
    for s in text: 
        if s in latin: num_of_latin += 1
    if num_of_latin < len(text) / 2:
        return None
    return text

def pipline(img_name, dir_name):
    rects = callCCVSWT(img_name)
    dumps = makeDumps(img_name, rects, dir_name)
    res = []
    for x in dumps:
        rec = recognizeByTesseract(x[0])
        rec = (rec[0], filterText(rec[1]))
        if rec[1] != None:
            res.append((x[2], rec[1]))
    return res

if __name__ == '__main__':
    import sys
    print pipline(sys.argv[1])
