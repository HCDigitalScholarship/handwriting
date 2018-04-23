
from PIL import Image, ImageEnhance
import io
from google.cloud import vision
from google.cloud import language
from oauth2client.client import GoogleCredentials
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("image_directory", help="Location of images to be clipped- it feels sad if there are other files in this directory")
parser.add_argument("output_directory", help="Location where images will be stored")
args = parser.parse_args()

image_folder = args.image_directory
out_folder   = args.output_directory


credentials = GoogleCredentials.get_application_default()

vision_client = vision.Client.from_service_account_json('key.json')

#language_client = language.Client()

for image_name in os.listdir(image_folder):
    with io.open(image_folder+image_name, 'rb') as image_file:
        """
        Check out https://cloud.google.com/vision/docs/fulltext-annotations and
        https://cloud.google.com/vision/docs/detecting-fulltext#vision-document-text-detection-python
        for code/information I used
        """
        
      
        content = image_file.read()
        image = vision_client.image(
            content=content)
        
        document = image.detect_full_text()
        boxes = []

        for page in document.pages:
            for block in page.blocks:
                block_words = []
                for paragraph in block.paragraphs:
                    #block_words.extend(paragraph.words)
                    boxes.append(paragraph.bounding_box)
                #block_symbols = []
                #for word in block_words:
                #    boxes.append(word.bounding_box)
                #    block_symbols.extend(word.symbols)
           
        count = 0 
        SAVE = True
        SHOW = True

        im = Image.open(image_folder+image_name)
        try:
            sharpness = ImageEnhance.Sharpness(im)
            sharpy = sharpness.enhance(4)  
        except ValueError:
            print("Got ValueError when trying to sharpen, img is " + image_name)
            print("Proceeding without sharpening")
            sharpy = im
        
        gray_im = sharpy.convert('L')
        bw_im = gray_im.point(lambda x: 0 if x<80 else 255, '1')        
    
        if SHOW:
            bw_im.show()
        for box in boxes:
            left  = min([box.vertices[i].x for i in range(4)]) - 20
            upper = min([box.vertices[i].y for i in range(4)]) - 20
            right = max([box.vertices[i].x for i in range(4)]) + 20 
            lower = max([box.vertices[i].y for i in range(4)]) + 20
            box = (left, upper, right, lower)
            region = bw_im.crop(box)
            
            if SHOW:
                region.show()
                raw_input("Enter to open another image, Ctrl+C to kill")
            if SAVE:
                img_name = image_name.split('.')[0]
                extension = image_name.split('.')[1]
                region.save(out_folder+"/"+img_name+str(count)+'.'+extension)
                count += 1

