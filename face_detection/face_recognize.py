import cv2, numpy as np, csv, sys

sample_size = 300

def read_data(fname, index):
    samples = []
    labels = []
    with open(fname) as f:
        reader = csv.reader(f, delimiter=';')
        data = [x for x in reader]
        samples = [cv2.resize(cv2.imread(x[0], 0), (sample_size, sample_size)) for x in data]
        labels  = np.array([index if int(x[1]) == index else 0 for x in data])
    return samples, labels

samples, labels = read_data(sys.argv[1], 4)
print labels
fc = cv2.createFisherFaceRecognizer()
fc.train(samples[:-3], labels[:-3])

for i,x in enumerate(samples):
    print fc.predict(samples[i]), labels[i]
