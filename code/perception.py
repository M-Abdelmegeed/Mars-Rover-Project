import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.image as mpimg
import scipy

# Identify pixels above the threshold
# Threshold of RGB > 160 does a nice job of identifying ground pixels only
def color_thresh(img, rgb_thresh=(150, 150, 150)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] > rgb_thresh[0]) \
                & (img[:,:,0] <=255) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,1] <= 255) \
                & (img[:,:,2] > rgb_thresh[2]) \
                & (img[:,:,2] <=255)
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select

# Define a function to convert from image coords to rover coords
def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
    x_pixel = -(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[1]/2 ).astype(np.float)
    return x_pixel, y_pixel


# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle) 
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

# Define a function to map rover space pixels to world space
def rotate_pix(xpix, ypix, yaw):
    # Convert yaw to radians
    yaw_rad = yaw * np.pi / 180
    xpix_rotated = (xpix * np.cos(yaw_rad)) - (ypix * np.sin(yaw_rad))
                            
    ypix_rotated = (xpix * np.sin(yaw_rad)) + (ypix * np.cos(yaw_rad))
    # Return the result  
    return xpix_rotated, ypix_rotated

def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale): 
    # Apply a scaling and a translation
    xpix_translated = (xpix_rot / scale) + xpos
    ypix_translated = (ypix_rot / scale) + ypos
    # Return the result  
    return xpix_translated, ypix_translated


# Define a function to apply rotation and translation (and clipping)
# Once you define the two functions above this function should work
def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
    # Apply rotation
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    # Apply translation
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    # Perform rotation, translation and clipping all at once
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
    # Return the result
    return x_pix_world, y_pix_world

# Define a function to perform a perspective transform
def perspect_transform(img, src, dst):

       
    # circle = np.zeros((150, 150), dtype="uint8")
    # circle_mask=cv2.circle(circle, (75, 140), 75, 255, -1)
    # circle_mask=cv2.resize(circle_mask,(img.shape[1], img.shape[0]))
    # img1=cv2.bitwise_and(img,img,mask=circle_mask)
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    mask = cv2.warpPerspective(np.ones_like(img[:,:,0]), M, (img.shape[1], img.shape[0]))
    

    
    return warped,mask



def find_rocks(img, levels=(130,140,30)): #RGB Threshold values for the rock
    rockpix = (( img[:,:,0]>levels[0]) \
                & (img[:,:,1] < levels[1]) \
                & (img[:,:,2] < levels[2]))
    
    color_select=np.zeros_like(img[:,:,0])
    color_select[rockpix]=1
    
    return color_select 



################## Getting color threshold values by clustering ################
example_rock = '../calibration_images/example_rock1.jpg'
rock_img=mpimg.imread(example_rock)
magnified_rock=rock_img[75:125,140:175]
rock=magnified_rock
magnified_rock=magnified_rock.reshape((magnified_rock.shape[1]*magnified_rock.shape[0],3))
kmeans=KMeans(n_clusters=4)
s=kmeans.fit(magnified_rock)
labels=kmeans.labels_
labels=list(labels)
centroid=kmeans.cluster_centers_
percent=[]
for i in range(len(centroid)):
  j=labels.count(i)
  j=j/(len(labels))
  percent.append(j)

######################## Computing Threshold Values ###########################
red_thresh=(centroid[2][0]-15)
green_thresh=(centroid[2][1]+centroid[3][1])/2
blue_thresh=(centroid[2][2]+centroid[3][2])/2


##############################################################################


# Apply the above functions in succession and update the Rover state accordingly
def perception_step(Rover):
    # Perform perception steps to update Rover()
    # TODO: 
    # NOTE: camera image is coming to you in Rover.img
    image=Rover.img
    dst_size = 5 
# Set a bottom offset to account for the fact that the bottom of the image 
# is not the position of the rover but a bit in front of it
# this is just a rough guess, feel free to change it!
    bottom_offset = 4
    # 1) Define source and destination points for perspective transform
    source = np.float32([[14, 140],
                         [300, 140],
                         [200, 95],
                         [120, 95]])
    destination = np.float32([[image.shape[1]/2 - dst_size, image.shape[0] - bottom_offset],
                    [image.shape[1]/2 + dst_size, image.shape[0] - bottom_offset],
                    [image.shape[1]/2 + dst_size, image.shape[0] - 2*dst_size - bottom_offset], 
                    [image.shape[1]/2 - dst_size, image.shape[0] - 2*dst_size - bottom_offset],
                    ])
    # 2) Apply perspective transform
    warped, mask1 = perspect_transform(image, source, destination)



    # circle = np.ones((150, 150), dtype="uint8")
    # circle_mask=cv2.circle(circle, (75, 170), 75, 255, -1)
    # circle_mask=cv2.resize(circle_mask,(Rover.img.shape[1], Rover.img.shape[0]))

   
    circle = np.zeros((150, 150), dtype="uint8")
    circle_mask=cv2.circle(circle, (75, 190), 90, 255, -1)
    circle_mask=cv2.resize(circle_mask,(image.shape[1], image.shape[0]))
    warped=cv2.bitwise_and(warped,warped,mask=circle_mask)
    mask1=cv2.bitwise_and(mask1,mask1,mask=circle_mask)
    
    
    

    
    # 3) Apply color threshold to identify navigable terrain/obstacles/rock samples
    threshed = color_thresh(warped)


    # rec_mask = np.zeros(image.shape[:2], dtype="uint8")
    # cv2.rectangle(rec_mask, (80, 160), (220, 110), 255, -1)
    # rec_mask=cv2.resize(rec_mask,(image.shape[1], image.shape[0]))
    # threshed=cv2.bitwise_and(threshed,threshed,mask=rec_mask)


    if threshed.any():
        threshed=scipy.ndimage.binary_erosion(threshed, structure=np.ones((4,4))).astype(threshed.dtype)


    
    obs_map= np.absolute(np.float32(threshed)-1)*mask1
    # 4) Update Rover.vision_image (this will be displayed on left side of screen)
        # Example: Rover.vision_image[:,:,0] = obstacle color-thresholded binary image
        #          Rover.vision_image[:,:,1] = rock_sample color-thresholded binary image
        #          Rover.vision_image[:,:,2] = navigable terrain color-thresholded binary image


    Rover.vision_image[:,:,2]=threshed * 255
    Rover.vision_image[:,:,0]=obs_map * 255

    # 5) Convert map image pixel values to rover-centric coords
    xpix, ypix = rover_coords(threshed)
    # 6) Convert rover-centric pixel values to world coordinates
    world_size = Rover.worldmap.shape[0]
    scale = 2*dst_size
    # xpos = Rover.xpos[Rover.count]
    # ypos = Rover.ypos[Rover.count]
    
    x_world, y_world = pix_to_world(xpix, ypix, Rover.pos[0], Rover.pos[1],
                                   Rover.yaw, world_size, scale)
    obsxpix, obsypix = rover_coords(obs_map)
    obs_x_world, obs_y_world = pix_to_world(obsxpix, obsypix, Rover.pos[0] ,Rover.pos[1],
                                   Rover.yaw, world_size, scale)


    # 7) Update Rover worldmap (to be displayed on right side of screen)
        # Example: Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1
        #          Rover.worldmap[rock_y_world, rock_x_world, 1] += 1
        #          Rover.worldmap[navigable_y_world, navigable_x_world, 2] += 1






        # Update world map if we are not tilted more than 0.5 degrees
    if (Rover.pitch < 0.2 or Rover.pitch > 359.8) and (Rover.roll < 0.2 or Rover.roll > 359.8) and Rover.mode != 'found' and Rover.vel != 0 :

        Rover.worldmap[y_world, x_world, 2] =50 # Coloring the blue channel for the navigable road
        Rover.worldmap[obs_y_world, obs_x_world, 0]=25 # Coloring the red channel for the obstacles

    # 8) Convert rover-centric pixel positions to polar coordinates
    dist, angles=to_polar_coords(xpix,ypix)
    # Update Rover pixel distances and angles
        # Rover.nav_dists = rover_centric_pixel_distances
        # Rover.nav_angles = rover_centric_angles







    Rover.nav_angles=angles
    Rover.nav_dists=dist




    #################   Finding Rocks    ##############################
    rock_map= find_rocks(warped, levels=(red_thresh,green_thresh,blue_thresh)) #Using threshold values computed
    if rock_map.any():
        rock_x, rock_y = rover_coords(rock_map)
        rock_x_world, rock_y_world = pix_to_world(rock_x, rock_y, Rover.pos[0], Rover.pos[1],
                                   Rover.yaw, world_size, scale)
        rock_dist,rock_ang = to_polar_coords(rock_x,rock_y)
        rock_idx=np.argmin(rock_dist)
        rock_xcen=rock_x_world[rock_idx]
        rock_ycen=rock_y_world[rock_idx]
        
        #print(rock_ang)

        #print("Rover.sample_pos: ",Rover.samples_pos)
        #print("Rover.samples_pos test: ", rock_x_world, rock_y_world)

        Rover.samples_dists=rock_dist
        Rover.samples_angles=rock_ang
        # print(rock_dist)
        # print(rock_ang)
        
       
        Rover.worldmap[rock_ycen,rock_xcen,1]=255
        Rover.vision_image[:,:,1]=rock_map*255
        Rover.worldmap[rock_y_world, rock_x_world, 0] += 1
        Rover.mode='found'

        #Rover.nav_angles=rock_ang
        #Rover.nav_dists=rock_dists-5



    else:
        Rover.vision_image[:,:,1]=0
        if Rover.mode=='found':
            Rover.mode='stop'
        

      
    





    return Rover


    ###