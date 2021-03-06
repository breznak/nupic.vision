#! /usr/bin/env python
'''
This script trains the spatial pooler (SP) on a set of images that are 
listed in the XML file specified by trainingDataset.  The SP is trained 
for a maximum number of training cycles given by maxTrainingCycles and then its
classification abilities are tested on the images listed in the XML file
specified by testingDataset.
'''

trainingDataset = 'DataSets/OCR/characters/cmr_hex.xml'
maxTrainingCycles = 20
testingDataset = 'DataSets/OCR/characters/cmr_hex.xml'

import dataset_readers as data
import image_encoders as encoder
from nupic.research.spatial_pooler import SpatialPooler
from vision_testbench import VisionTestBench
from classifiers import exactMatch


# Get training images and convert them to vectors.
trainingImages, trainingTags = data.getImagesAndTags(trainingDataset)
trainingVectors = encoder.imagesToVectors(trainingImages)


# Instantiate the python spatial pooler
sp = SpatialPooler(
  inputDimensions = 32**2, # Size of image patch
  columnDimensions = 16, # Number of potential features
  potentialRadius = 10000, # Ensures 100% potential pool
  potentialPct = 1, # Neurons can connect to 100% of input
  globalInhibition = True,
  localAreaDensity = -1, # Using numActiveColumnsPerInhArea 
  #localAreaDensity = 0.02, # one percent of columns active at a time
  #numActiveColumnsPerInhArea = -1, # Using percentage instead
  numActiveColumnsPerInhArea = 1, # Only one feature active at a time
  # All input activity can contribute to feature output
  stimulusThreshold = 0,
  synPermInactiveDec = 0.3,
  synPermActiveInc = 0.3,
  synPermConnected = 0.3, # Connected threshold
  maxBoost = 2,
  seed = 1956, # The seed that Grok uses
  spVerbosity = 1)


# Instantiate the spatial pooler test bench.
tb = VisionTestBench(sp)

# Instantiate the classifier
clf = exactMatch()

# Train the spatial pooler on trainingVectors.
numCycles = tb.train(trainingVectors, trainingTags, clf, maxTrainingCycles)

# View the permanences and connections after training.
tb.showPermsAndConns()
#tb.savePermsAndConns('perms_and_conns.jpg')

# Get testing images and convert them to vectors.
testingImages, testingTags = data.getImagesAndTags(testingDataset)
testingVectors = encoder.imagesToVectors(testingImages)

# Test the spatial pooler on testingVectors.
accuracy = tb.test(testingVectors, testingTags, clf, verbose=1)


