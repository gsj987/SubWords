from numpy import array
import numpy as np
import Image  

class PCA():
  def __init__(self, num_components=0):
    self._num_components = num_components
    self.__init_features()

  def __init_features(self):
    if not self.__load_features():
      _crops = []
      for l in map(chr, range(97,123)):
        img = Image.open('data/crops/%s.png' %l).convert('L')
        _crops.append(PCA.load_image(img))
      self.compute(np.array(_crops))
      self.__store_features()
  
  def __load_features(self):
    try:
      f = open('data/feature.npz', 'rb')
      _feature = np.load(f)
      f.close()
      self._eigenvalues = _feature['eigenvalues']
      self._eigenvectors = _feature['eigenvectors']
      self._mean = _feature['mean']
      self._features = _feature['features']

      return True
    except:
      return False

  def __store_features(self):
    f = open('data/feature.npz', 'wb')
    _d = {
      'eigenvectors': self._eigenvectors,
      'eigenvalues': self._eigenvalues,
      'mean': self._mean,
      'features': self._features
    }
    
    np.savez(f,**_d)
    f.close()
  
  @staticmethod
  def load_image(img):
    data = np.array(img.getdata(),
                    np.uint8).reshape(img.size[1], img.size[0])
    return (data - data.mean()) / data.std()
  
  @staticmethod
  def asColumnMatrix(X):
    """
    Creates a column-matrix from multi-dimensional data items in list l.
    
    X [list] List with multi-dimensional data.
    """
    if len(X) == 0:
      return np.array([])
    total = 1
    for i in range(0, np.ndim(X[0])):
      total = total * X[0].shape[i]
    mat = np.empty([total, 0], dtype=X[0].dtype)
    for col in X:
      mat = np.append(mat, col.reshape(-1,1), axis=1) # same as hstack
    return np.asmatrix(mat)

  def compute(self,X):
    # build the column matrix
    XC = PCA.asColumnMatrix(X)
    # set a valid number of components
    if self._num_components <= 0 or (self._num_components > XC.shape[1]-1):
      self._num_components = XC.shape[1]-1
    # center dataset
    self._mean = XC.mean(axis=1).reshape(-1,1)
    XC = XC - self._mean
    # perform an economy size decomposition (may still allocate too much memory for computation)
    self._eigenvectors, self._eigenvalues, variances = np.linalg.svd(XC, full_matrices=False)
    # sort eigenvectors by eigenvalues in descending order
    idx = np.argsort(-self._eigenvalues)
    self._eigenvalues, self._eigenvectors = self._eigenvalues[idx], self._eigenvectors[:,idx]
    # use only num_components
    self._eigenvectors = self._eigenvectors[0:,0:self._num_components].copy()
    self._eigenvalues = self._eigenvalues[0:self._num_components].copy()
    # finally turn singular values into eigenvalues 
    self._eigenvalues = np.power(self._eigenvalues,2) / XC.shape[1]
    # get the features from the given data
    self._features = []
    for x in X:
      xp = self.project(x.reshape(-1,1))
      self._features.append(xp)
    return self._features
  
  def extract(self,X):
    X = np.asarray(X).reshape(-1,1)
    return self.project(X)
    
  def project(self, X):
    X = X - self._mean
    return np.dot(self._eigenvectors.T, X)

  def reconstruct(self, X):
    X = np.dot(self._eigenvectors, X)
    return X + self._mean

  @property
  def num_components(self):
    return self._num_components

  @property
  def eigenvalues(self):
    return self._eigenvalues
    
  @property
  def eigenvectors(self):
    return self._eigenvectors

  @property
  def mean(self):
    return self._mean

  @property
  def features(self):
    return self._features
    
  def __repr__(self):
    return "PCA (num_components=%d)" % (self._num_components)


if __name__ == '__main__':
  sample_data = array(((1,2),(2,7),(2,3),(4,6),(1,1),(2,1))).T
  print sample_data
  _feature = PCA(2)
  
  print _feature.compute(sample_data)
  
