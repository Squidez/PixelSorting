# Packages Importation
from tqdm import tqdm
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def get_sorted_pix_index(pix_list,min,max,descending):
    """
    Parameters
    ---
    pix_list: (list) a list of pixels
    min: (0-255) value of the minimum threshold (default: 64)
    max: (0-255) value of the minimum threshold (default: 192)
    descending: (bool) to sort the pixels by descending order (default: False)\n
    ----
    Output
    ---
    returns a list of the pixel index sorted by their value
    """
    #liste of the index of the pixels to sort
    pix_to_sort = [i for i,pix in enumerate(pix_list) if min<pix<max]

    # Empty lists to store the segments of pix to sort
    segments_lists = []
    segment = []

    # compares every element of pix_to_sort to see if they follow each other
    # returns a list of each segment
    for i in range(len(pix_to_sort)):
        if i == 0 or pix_to_sort[i] == pix_to_sort[i-1] + 1:
            segment.append(pix_to_sort[i])
        else:
            # Appends the segment to the segments list
            segments_lists.append(segment)
            segment = [pix_to_sort[i]]

    # Appends the last segment to the segments list
    if segment:
        segments_lists.append(segment)

    # Initialize the index list
    index_list = [i for i,pix in enumerate(pix_list)]
    # Initialize a dict of the pixels (index: pixel value)
    pix_dict = {i:pix for i,pix in enumerate(pix_list)} 

    for segment in segments_lists:

        if len(segment)>1:

            # Pixel dict of the segment
            segment_dict = {i: pix_dict[i] for i in segment}
            # Sorts the dict according to the pixel value 
            segment_dict = {i: pix for i, pix in sorted\
                            (segment_dict.items(),
                             key=lambda item: item[1], 
                             reverse=descending)}
            
            # replace the segment with the indexes sorted by value
            start = segment[0]
            stop = segment[-1]+1
            index_list[start:stop] = segment_dict.keys()

    return index_list

def pixel_sorter(img_path,
                 min = 64, # 25%
                 max = 192, # 75%
                 mode = 'lumi',
                 vertical=False,
                 descending=False,):
    """
    Parameters
    ---
    img_path: (str) path of the image to pixel sort
    min: (0-255) value of the minimum threshold (default: 64)
    max: (0-255) value of the minimum threshold (default: 192)
    mode: ('lumi','red','green','blue','hue','sat') determines the mode of sorting (default: lumi)
    vertical: (bool) to sort the pixels vertically (default: False)
    descending: (bool) to sort the pixels by descending order (default: False)\n
    ---
    Output
    ---
    Return an image array with sorted pixels.\n
    ---
    Modes
    ---
    lumi: sort by luminescence
    red, green, blue: sort by intensity of selected color
    hue: sort by intensity of hue
    sat: sort by intensity of saturation
    """

    # loads the image
    img = Image.open(img_path).convert('RGB')

    # Just to avoid working with to big images and have shorter processing times
    width, height = img.size
    if height>1920 or width>1920:
        img.thumbnail((1920,1920))

    # Initialize the image array
    img_array = np.array(img)

    # returns a B&W array of the image
    if mode == 'lumi':

        sort_array = np.array(img.convert('L'))

    # returns an array of the selected color chanel of the image
    if mode in ('red','green','blue'):
        i = ('red','green','blue').index(mode)
        sort_array = img_array[:,:,i]

    # returns an array the hue or saturation value of the image
    if mode in ('hue','sat'):
        i = ('hue', 'sat').index(mode)
        sort_array = np.array(img.convert('HSV'))
        sort_array = sort_array[:,:,i]

    # Transposes the arrays (acts like an image rotation) to sort the pixels vertically
    if vertical == True:

        img_array = np.transpose(img_array, (1,0,2))
        sort_array = sort_array.T

    # Initialize the output array
    output_array = np.zeros_like(img_array)

    # Sorts the pixels for each line in the array and saves the output
    for i,line in tqdm(enumerate(img_array),
                        desc='Sorting',
                        unit='line'):

        sorted_index = get_sorted_pix_index(sort_array[i],min,max,descending)
        output_array[i] = img_array[i][sorted_index]

    # transpose the output back to it's original shape
    if vertical == True:
        output_array=np.transpose(output_array, (1,0,2))

    return output_array
