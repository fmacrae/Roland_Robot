#! /bin/bash
~/caffe/examples/cpp_classification/classification.bin   ~/caffe/models/bvlc_reference_caffenet/deploy.prototxt   ~/caffe/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel   ~/caffe/data/ilsvrc12/imagenet_mean.binaryproto   ~/caffe/data/ilsvrc12/synset_words.txt    $1 $2

