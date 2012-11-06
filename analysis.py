import Image
from scipy.spatial.distance import euclidean
from parse import crop_and_perprocessing
from pca import PCA



class Analyzer:
  __crops = []
  __featrue = PCA(2)

  def __init__(self):
    self.__load_crops()

  def __load_crops(self): 
    self.__crops = self.__featrue.features

  @staticmethod
  def __compare(im1, im2):
    return euclidean(im1, im2)

  def __analyze(self, img):
    _data = PCA.load_image(img)
    data = self.__featrue.extract(_data)
    min = 65536
    l = None
    _l = 97
    for _d in self.__crops: 
      _m = Analyzer.__compare(_d, data) 
      if _m < min:
        min = _m
        l = chr(_l) 
      _l+=1
    return l

  def analyze_letters(self, img): 
    letters = []
    crops = crop_and_perprocessing(img)
    for crop in crops:
      letters.append(self.__analyze(crop.resize((16,16))))
    
    return letters

if __name__ == '__main__':
  sample = Image.open('data/samples/IMG_3012.PNG')
  analyzer = Analyzer()
  print analyzer.analyze_letters(sample)
