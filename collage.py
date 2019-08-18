def collageFinal():
  frame = makeEmptyPicture(700, 515)
  original = makePicture(pickAFile())
  grayScale(original)
  mirrorVertical(original)
  
def grayScale(original):
  pic = original
  for p in (getPixels(pic)):
    average = (getRed(p) + getGreen(p) + getBlue(p))/3
    newColor = makeColor(average, average, average)
    setColor(p, newColor)
  show(pic)
  
def mirrorVertical(original):
  picture = original
  width = getWidth(picture)
  mirror = width / 2
  height = getHeight(picture)
  for y in range(0, height):
    for x in range(width-1, mirror, -1):
      right = getPixel(picture, x, y)
      left = getPixel(picture, width - x - 1, y)
      c = getColor(right)
      setColor(left, c)
  show(picture)
  
collageFinal()