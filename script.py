from dataset import get_all_file_paths
from dataset import get_only_file_by_dataset
from utils import show
from utils import imshow_hstack
from processing import extract_mask
from tqdm import tqdm
import cv2

data_set_path = "data\\planoB\\"

data_set = get_all_file_paths(data_set_path)


files = get_only_file_by_dataset(data_set)

print(f"Number of files: {len(files)} ")

image = 30
for f in tqdm(files[image:image+4]):
    img = cv2.imread(f, 0)
    img_mask, values = extract_mask(img, show_images=False)
    imshow_hstack(img, img_mask)
