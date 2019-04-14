import knn_classifier
import numpy as np
prediction = 'n.a.'
prediction = knn_classifier.main('training.data', np.array([255,255,255]))

print('pred', prediction)
