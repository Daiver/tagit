import cv2, sys, time, os

#TRAINSET = "/usr/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml"

if len(sys.argv) < 2:
    print "file not specified"
 
else:
    write_files = len(sys.argv) > 2
    face_cascade_path = "frontalface10/haarcascade_frontalface_alt.xml"
    eye_cascade_path = "frontalface10/haarcascade_eye_tree_eyeglasses.xml"
    DOWNSCALE = 4

    cv2.namedWindow("preview")
    face_detector = cv2.CascadeClassifier(face_cascade_path)
    eye_detector = cv2.CascadeClassifier(face_cascade_path)

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
        #cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255))
 
    cv2.imshow("preview", frame)
    key = 90
    while key not in [27, ord('Q'), ord('q')]: # exit on ESC
        key = cv2.waitKey() % 0x100
        print key
