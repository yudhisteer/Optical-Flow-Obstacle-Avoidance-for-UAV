# Optical Flow Obstacle Avoidance for UAV

## Problem Statement

## Abstract

## Plan of Action
1. [Understanding Optical Flow](#understanding-optical-flow)
    - Motion Field
    - Optical Flow Constraint Equation
    - Sparse Optical Flow
    - Dense Optical Flow  

2. [FlowNet: Learning Optical Flow with Convolutional Networks](#flownet)

3. [RAFT: Recurrent All-Pairs Field Transforms for Optical Flow](#raft)

4. [Obstacle Detection with RAFT](#obstacle-detection)

---------------------

<a name="understanding-optical-flow"></a>
## 1. Understanding Optical Flow
Optical flow is a method used to analyze the apparent motion of objects in a sequence of images or video. It involves tracking the movement of ```individual pixels``` or small regions over time, providing insights into how objects are moving within a scene. While images capture the ```spatial``` aspects of a scene, videos add the ```temporal``` dimension, enabling the perception of motion and dynamic changes.

When comparing two images, our objective is to determine the corresponding locations of points in the first image within the second image. This mapping of points is referred to as the ```motion field```. By analyzing how **brightness patterns** in the first image relate to their positions in the second image, we can approximate the motion field. This involves tracking the ```displacement of brightness patterns``` to infer the underlying ```motion of points``` between the images. Optical flow provides an approximation of the underlying motion field based on the observed ```shifts in brightness patterns between consecutive frames```.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/867a227e-0b8a-4b40-bb6e-01c9fe792b0e" width="600" height="300"/>
  <p><b> Fig 1. Flow map where the direction of the arrow indicates the motion's direction, while the length of the arrow represents the speed or magnitude of the motion.</b></p>
</div>

Each pixel in the image has an optical flow vector representing the ```motion of brightness patterns``` at that point. The vector's ```length``` indicates the ```speed``` of motion, and its ```direction``` indicates the specific ```direction``` of motion on the image plane. In an ideal scenario, optical flow perfectly matches the motion field, accurately representing object movement. However, in practice, optical flow and the motion field are not always identical due to **occlusions** and **complex motion patterns**, leading to incomplete and less accurate motion information.

It's important to note that the motion of points between the images depends on the depth of the points, as this influences their perceived motion.

### 1.1 Motion Field
Consider a point in a scene that is moving in a certain direction in three-dimensional space. This movement is projected onto the image plane, resulting in a motion on the image known as the ```motion field``` for that point. However, measuring this motion field directly is often not possible. What we can measure instead is the motion of brightness patterns in the image, which is referred to as ```optical flow```. Optical flow provides insights into how the brightness patterns within the image change and move, but it is an approximation of the actual motion field.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/097737fa-3c43-4df3-9fa7-e1ff6cde96d1" width="600" height="250"/>
  <p><b> Fig 2. Ouchi Pattern (left) and Donguri Wave Illusion (right).</b></p>
</div>

Figure above shows examples of when the motion field is not equal to the optical flow. The images are static but when when we move our eyes arounf the image, the latter seem to be moving. We have an optical flow in our visual system but their is **no** motion field!


### 1.2 Optical Flow Constraint Equation

Let's say we have two images of a scene taken in quick succession: a yellow car moving on a road. Now focus our attention on a single point within this window: side-view mirror of the car. We assume that the position of the point is ![CodeCogsEqn (9)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/9fc23ee6-5ba8-43d2-b1a1-d8539d0b800e).
Now, at time ![CodeCogsEqn (11)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/f805c821-8701-429c-bdf5-246033377c29), that point has moved to a new location: ![CodeCogsEqn (10)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/83e14c2f-d1bd-4383-a769-7c679a364079)
So the ```displacement``` of the point ![CodeCogsEqn (9)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/31734bf1-797d-472a-984f-8779c6d7e847) can be said to be ![CodeCogsEqn (10)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/3d7a05cd-e2b2-4835-8ada-db36582f795b).

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/efb948a1-1da6-4eba-a2ad-091d9e74e914" width="1000" height="250"/>
  <p><b> Fig 3. Displacement of an object over a short interval of time. </b></p>
</div>


If we divide by ![CodeCogsEqn (13)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/a3b030ad-be47-4de0-b3fd-1b6b6fbd1ac3), then we essentially have the ```speed``` of the point in the ```X``` and ```Y``` directions and that we will call you ![CodeCogsEqn (14)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/f13451c6-f60b-4f93-b490-fde05f41f266). That is the **optical flow** corresponding to the point.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/3597eb4b-bddb-46de-9469-2f515468ba14"/>
</div>






### 1.3 Sparse Optical Flow
We cannot directly determine the optical flow for each pixel by solely analyzing its brightness changes. However, we can utilize an approach known as an optical flow-constrained equation. This equation helps us restrict and solve the optical flow problem by imposing constraints on the optical flow values at each pixel. By considering a neighborhood of pixels around each pixel, we enhance the accuracy of optical flow estimation. This approach leads us to the ```Lucas-Kanade method```, a technique widely used for estimating optical flow.


### 1.4 Dense Optical Flow














--------------------

<a name="flownet"></a>
## 2. FlowNet: Learning Optical Flow with Convolutional Networks



<a name="raft"></a>
## 3. RAFT: Recurrent All-Pairs Field Transforms for Optical Flow







https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/cb59221d-cbf3-425b-80d5-5c8b554c031c







<a name="obstacle-detection"></a>
## 4. Obstacle Detection with RAFT









## References
1. https://www.youtube.com/watch?v=lnXFcmLB7sM&list=PL2zRqk16wsdoYzrWStffqBAoUY8XdvatV&ab_channel=FirstPrinciplesofComputerVision
2. https://nanonets.com/blog/optical-flow/#optical-flow-using-deep-learning
3. https://www.mathworks.com/matlabcentral/fileexchange/94095-obstacle-avoidance-with-camera-sensor-using-simulink
4. https://medium.com/swlh/what-is-optical-flow-and-why-does-it-matter-in-deep-learning
5. https://towardsdatascience.com/a-brief-review-of-flownet-dca6bd574de0
6. https://zainmehdiblog.wordpress.com/vision-based-obstacle-avoidance/
7. https://github.com/philferriere/tfoptflow/blob/master/README.md
8. https://learnopencv.com/optical-flow-using-deep-learning-raft/
9. https://pub.towardsai.net/eccv-2020-best-paper-award-a-new-architecture-for-optical-flow-3298c8a40dc7
10. https://learnopencv.com/optical-flow-in-opencv/
11. https://prgaero.github.io/2019/proj/p4b/#rviz
12. http://prg.cs.umd.edu/enae788m
13. https://www.coursera.org/learn/robotics-perception/lecture/DgSNW/3d-velocities-from-optical-flow
14. 
