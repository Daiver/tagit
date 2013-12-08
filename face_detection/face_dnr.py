import cv2, sys, time, os, random, math, pickle
import numpy as np

sample_size = 300
def loadImgToRec(fname): return cv2.resize(cv2.imread(fname, 0), (sample_size, sample_size))

def recognize_person(fname, persons):
    fcs = []
    res = []
    for person in persons:
        fc = cv2.createFisherFaceRecognizer()
        fc.load(person.ClassifierName)
        fcs.append(fc)
        res.append((person, ) + fc.predict(loadImgToRec(fname)))
    return res


def train_fc(person, faces_db_set):
    def train_test_border(some_set, coeff): return int(math.ceil(len(some_set) * coeff))
    data = [
        (x.Mark.id if x.Mark else 0, x.FileName, loadImgToRec(x.FileName))
        for x in faces_db_set
    ]
    person_id = person.id
    samples = map(lambda x: x[2], data)
    labels  = map(lambda x: 1 if x[0] == person_id else 0, data)
    tol = 1
    fc = None
    while tol > 0.05:
        pos_idx = map(lambda x:x[0], filter(lambda x: x[1] == 1, enumerate(labels)))
        neg_idx = map(lambda x:x[0], filter(lambda x: x[1] != 1, enumerate(labels)))
        random.shuffle(pos_idx)
        random.shuffle(neg_idx)
        neg_idx = neg_idx[:int((2 * len(pos_idx)) % len(neg_idx))]
        border_p = train_test_border(pos_idx, 0.2)
        border_n = train_test_border(neg_idx, 0.2)
        train_idx = pos_idx[border_p:] + neg_idx[border_n:]
        test_idx  = pos_idx[:border_p] + neg_idx[:border_n]

        train_samples = [samples[i] for i in train_idx]
        train_labels  = np.array([labels[i] for i in train_idx])
        test_samples  = [samples[i] for i in test_idx]
        test_labels   = [labels[i] for i in test_idx]
        fc = cv2.createFisherFaceRecognizer()
        fc.train(train_samples, train_labels)
        tol = 0.0
        print 'test'
        print [data[i][1] for i in test_idx]
        for i, x in enumerate(test_samples):
            r, t = fc.predict(x), test_labels[i]
            if r[0] != t: tol += 1
            print r, t
        tol /= len(test_labels) 
        print tol
        if tol <= 0.1:
            tol = 0.0
            print 'test on train'
            for i, x in enumerate(samples):
                r, t = fc.predict(x), labels[i]
                if r[0] != t: tol += 1
                print r, t
            tol /= len(labels) + len(train_labels)
            print tol
    fname = os.path.join(os.path.dirname(__file__), 'classifiers', '%d_%s_classifier' % (person.id, person.Name))
    fc.save(fname)
    person.ClassifierName = fname
    person.save()
    #for i, x in enumerate(train_samples):
    #    print fc.predict(x), train_labels[i]


#TRAINSET = "/usr/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml"

face_cascade_path = os.path.join(os.path.dirname(__file__), "frontalface10/haarcascade_frontalface_alt.xml")
#eye_cascade_path = os.path.join(os.path.dirname(__file__), "frontalface10/haarcascade_eye_tree_eyeglasses.xml")

face_detector = cv2.CascadeClassifier(face_cascade_path)
#eye_detector = cv2.CascadeClassifier(face_cascade_path)
#eye_detector = cv2.CascadeClassifier(eye_cascade_path)
DOWNSCALE = 2

def detect_faces(fname, dir_name):
    img = cv2.imread(fname)
    minisize = (img.shape[1]/DOWNSCALE,img.shape[0]/DOWNSCALE)
    miniframe = cv2.resize(img, minisize)
    faces = face_detector.detectMultiScale(miniframe)
    file_name = fname.split(os.path.sep)[-1]
    img2 = img.copy()
    res = []
    for i, f in enumerate(faces):
        x, y, w, h = [ v*DOWNSCALE for v in f ]
        small = img[y:y + h,x:x + w]
        face2 = face_detector.detectMultiScale(small)
        name = os.path.join(dir_name, '_'.join([file_name, str(i), '.png']))
        if len(face2) > 0: 
            face2 = face2[0]
            res.append((name, ((x + face2[0],y + face2[1]), (x + face2[0] + face2[2],y + face2[1] + face2[3]))))
            small = small[face2[1]:face2[3] + face2[1], face2[0]: face2[2] + face2[0]]
            cv2.rectangle(img2, (x + face2[0],y + face2[1]), (x + face2[0] + face2[2],y + face2[1] + face2[3]), (0,255,0), 3)
        else:
            res.append((name, ((x,y), (x+w,y+h))))
            cv2.rectangle(img2, (x,y), (x+w,y+h), (0,255,0), 3)
        cv2.imwrite(name, small)

    cv2.imwrite(fname + '.face_marked.jpg', img2)
    return res
 
if False:
    write_files = len(sys.argv) > 2

    cv2.namedWindow("preview")

    frame = cv2.imread(sys.argv[1])
    minisize = (frame.shape[1]/DOWNSCALE,frame.shape[0]/DOWNSCALE)
    miniframe = cv2.resize(frame, minisize)
    st = time.time()
    faces = face_detector.detectMultiScale(miniframe)
    print 'time ', time.time() - st
    for i, f in enumerate(faces):
        x, y, w, h = [ v*DOWNSCALE for v in f ]
        small = frame[y:y + h,x:x + w]
        eyes = eye_detector.detectMultiScale(small)
        print eyes
        if len(eyes) > 0:
            eye = eyes[0]
            X, Y, W, H = [ v for v in eye ]
            small2 = small[Y:Y + H,X:X + W]
            if write_files: cv2.imwrite(os.path.join(sys.argv[2], sys.argv[1].split('/')[-1] + '_' + str(i) + '.jpg'), small2)
            cv2.imshow(str(i) + 'eye', small2)
            print 'shape', small2.shape
        else:
            print 'shape', small.shape
            if write_files: cv2.imwrite(os.path.join(sys.argv[2], sys.argv[1].split('/')[-1] + '_' + str(i) + '.jpg'), small)
        cv2.imshow(str(i), small)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255))
 
    cv2.imshow("preview", frame)
    key = 90
    while key not in [27, ord('Q'), ord('q')]: # exit on ESC
        key = cv2.waitKey() % 0x100
        print key
