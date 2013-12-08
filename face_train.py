#!/usr/bin/env python2
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tagit.settings")
    import tagit.settings 
    from tagger.models import *
    from face_detection.face_dnr import train_fc
    train_fc(Person.objects.filter(id=2).first(), FaceRecRes.objects.all())

