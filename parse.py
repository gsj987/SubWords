import Image

def threshold(im):
  ph, pw = im.size
  pix = im.load()
  last = None
  last = pix[0,0]

  for x in range(0, ph):
    for y in range(0, pw):
      if  abs(pix[x,y] - last)>50:
        cursor = 0
      else:
        cursor = 255
      pix[x,y] = cursor
  return im

def crop_and_perprocessing(im):
  im = im.convert('L')
  ph, pw = 128, 128

  im = im.crop((0, 320, 640, 960))
  crops = []
  for dh in range(0,5):
    for dw in range(0,5):
      ci = im.crop((dh*ph, dw*pw, dh*ph+ph, dw*pw+pw))
      crops.append(threshold(ci))

  return crops

if __name__ == '__main__':
  crops = crop_and_perprocessing(Image.open('samples/IMG_3007.PNG'))
  for i in range(len(crops)):
    crops[i].save('crops/img_%d.png' %i)
