
# Mars Rover Project 

A computer vision for robotics project. The project phase 1 aim to do mapping of navigable terrain, obstacles and rock sample location overplotted with the ground truth map.

## Project Phase 1 Overview ScreenShot
![image](https://user-images.githubusercontent.com/67200068/206847519-a7869fac-417e-49b2-92f5-219643ddab5c.png)

## How to run the project (UBUNTU)
1) Download the project directory , go to /Mars-Rover-Project/code , right click then click on open terminal
![image](https://user-images.githubusercontent.com/67200068/206851231-72e22e2d-a7e5-47ec-bfca-08f68e0cdc8f.png)
2)run driver_rover.py by the command **python3 drive_rover.py**
![image](https://user-images.githubusercontent.com/67200068/206850761-906ff188-94ca-4a23-837f-9c314067782d.png)
3)Download Linx_Roversim and run **Roversim.x86_64**
![image](https://user-images.githubusercontent.com/67200068/206851001-32f6d9ad-3fa3-4a78-8544-afe706fe095e.png)
4)choose to ride autonomos mode and enjoy **PHASE 1**
![image](https://user-images.githubusercontent.com/67200068/206851302-b2d9a0df-a1af-43ff-93b6-cb554e8723fa.png)



## Phase 1 Screenshots
The starting screen (Empty World Map)
![image](https://user-images.githubusercontent.com/67200068/206852082-b7841096-4c5c-4fcc-b6f7-b9471e5a6676.png)

As the rover starts to drive, the obstacles which are cpatured by thr rover are red in the world map and the navigable terrain is blue
![image](https://user-images.githubusercontent.com/67200068/206852222-7d294be6-ee3a-4197-a36e-85757babd2d9.png)

When the rover finds a yellow rock ,the rock is plotted in the world map as a white pixel and the number of Located is increased by One
![image](https://user-images.githubusercontent.com/67200068/206852275-97067f5f-35ea-4cd6-90cf-bdee3419f8ca.png)

The Rover Contine to navigate the map untill trying to locate many rocks as possible
![image](https://user-images.githubusercontent.com/67200068/206852311-f5013460-8cc5-49ca-b6d5-a7d91dc14c9e.png)

When the rover finds the a deadend, it automatically rotate and finds another path
![image](https://user-images.githubusercontent.com/67200068/206852468-6df57761-8b47-45e5-9f60-d6027cbe622a.png)


![image](https://user-images.githubusercontent.com/67200068/206852542-d3433882-1f11-44c3-9d96-a5ee0c731d37.png)


