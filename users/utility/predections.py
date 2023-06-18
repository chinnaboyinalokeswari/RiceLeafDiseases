import pickle
from PIL import Image
import os
from django.conf import settings
from skimage.io import imread
from skimage.transform import resize
import skimage

def load_image(file):
    dimension=(104, 104)
    image = Image.open(file)
    flat_data = []
    img = skimage.io.imread(file)
    img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
    flat_data.append(img_resized.flatten())
    return image,flat_data

def predict_user_input(file):
    model_path = os.path.join(settings.MEDIA_ROOT, 'model', 'rice_pred.pkl')
    with open(model_path, 'rb') as f:
        clf = pickle.load(f)
    path = os.path.join(settings.MEDIA_ROOT, 'rice_test', file)
    plot, img = load_image(path)
    k = ['Bacterial leaf blight', 'Brown spot', 'Leaf smut']
    p = clf.predict(img)
    s = [str(i) for i in p]
    a = int("".join(s))
    result = k[a]
    print("Predicted Disease is", k[a])
    return result
