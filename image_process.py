import os

# specify the directory containing the images
image_dir = 'C:\\Users\\PF-Enterprises\\Documents\\Output'

# iterate through the files in the directory
for filename in os.listdir(image_dir):
    # check if the file is an image (you can modify this condition as needed)
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # construct the new filename with the "_Unspecified" suffix
        new_filename = os.path.splitext(filename)[0] + '_Unspecified' + os.path.splitext(filename)[1]
        # rename the file
        os.rename(os.path.join(image_dir, filename), os.path.join(image_dir, new_filename))
