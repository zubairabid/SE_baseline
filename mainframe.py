# Pre-decide this somehow, and image.png (picture of page) ends up on
# ./tmp/image.png

from imagesegmentation import outline 
from ocr import ocr
from textsimilarity import textsim

path_to_file = './tmp/image.png'

# segments = outline.get_segments(path_to_file)
segments = [1,]

for segment in segments:
    path_to_segment = './tmp/'+str(segment)+'.png' # use os.path.join
    segment_text = ocr.get_text(path_to_segment)

    segment_similariy = textsim.get_simscore(segment, segment_text)
    print(segment_text)
    print("Correctness score of ", segment_similariy)

