# Optical Flow Obstacle Avoidance for UAV

## Problem Statement

## Abstract

## Plan of Action
1. [Understanding Optical Flow](#understanding-optical-flow)

    - [Motion Field](#motion-field)
    - [Optical Flow Constraint Equation](#equation)
    - [Sparse Optical Flow](#sparse)
    - [Dense Optical Flow](#dense)

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

<a name="motion-field"></a>
### 1.1 Motion Field
Consider a point in a scene that is moving in a certain direction in three-dimensional space. This movement is projected onto the image plane, resulting in a motion on the image known as the ```motion field``` for that point. However, measuring this motion field directly is often not possible. What we can measure instead is the motion of brightness patterns in the image, which is referred to as ```optical flow```. Optical flow provides insights into how the brightness patterns within the image change and move, but it is an approximation of the actual motion field.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/097737fa-3c43-4df3-9fa7-e1ff6cde96d1" width="600" height="250"/>
  <p><b> Fig 2. Ouchi Pattern (left) and Donguri Wave Illusion (right).</b></p>
</div>

Figure above shows examples of when the motion field is not equal to the optical flow. The images are static but when when we move our eyes arounf the image, the latter seem to be moving. We have an optical flow in our visual system but their is **no** motion field!

<a name="equation"></a>
### 1.2 Optical Flow Constraint Equation

Let's say we have two images of a scene taken in quick succession: a yellow car moving on a road. Now focus our attention on a single point within this window: side-view mirror of the car. We assume that the position of the point is ![CodeCogsEqn (9)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/9fc23ee6-5ba8-43d2-b1a1-d8539d0b800e).
Now, at time ![CodeCogsEqn (11)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/f805c821-8701-429c-bdf5-246033377c29), that point has moved to a new location: ![CodeCogsEqn (10)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/83e14c2f-d1bd-4383-a769-7c679a364079)
So the ```displacement``` of the point ![CodeCogsEqn (9)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/31734bf1-797d-472a-984f-8779c6d7e847) can be said to be ![CodeCogsEqn (21)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/cb1df29e-4098-449d-8e0c-a8071f4d3f37).

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/efb948a1-1da6-4eba-a2ad-091d9e74e914" width="1000" height="250"/>
  <p><b> Fig 3. Displacement of an object over a short interval of time. </b></p>
</div>


If we divide by ![CodeCogsEqn (13)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/a3b030ad-be47-4de0-b3fd-1b6b6fbd1ac3), then we essentially have the ```speed``` of the point in the ```X``` and ```Y``` directions and that we will call you ![CodeCogsEqn (14)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/f13451c6-f60b-4f93-b490-fde05f41f266). That is the **optical flow** corresponding to the point.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/3597eb4b-bddb-46de-9469-2f515468ba14"/>
</div>

In order to solve this problem we need to make some assumptions:

1. The brightness of an image point remains constant over time. That is, intensity at new location in time equals intensity at old location in time.


<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/dbf036c9-680b-4392-8457-81d527e98cbd"/>
</div>


2. The displacement ![CodeCogsEqn (17)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/8f36c761-f743-4f39-8628-d7fe9091e114) and time step ![CodeCogsEqn (18)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/f3d2f9bc-5881-4f08-aa65-0a281105978d) are small. This allow us to come up with a  linear approximation. Using Taylor Series expansion:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/15f1cad9-c16b-4e21-8fc1-884c578dd7e4"/>
</div>

Note that we ignore the higher order terms as ![CodeCogsEqn (30)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/7a9d2c1c-c73b-4a7e-a1c0-c5c23ca8c052) are already very small:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/ba75a593-c924-489a-9925-2fd2fbb3d0d9"/>
</div>

When we subtract the two equations above, we end up with the equation below: 

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/9b7677a9-2e68-4b8d-825d-7cfa023d8fd6"/>
</div>

We divide by ![CodeCogsEqn (27)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/ca593dd6-f180-4f6c-a1c8-d16b61c425fb) and take limit as ![CodeCogsEqn (28)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/2749a6ee-5ca4-4843-bef6-d632bfa5f4e5):

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/d5b2d179-d022-4b82-bf72-0af88d73c26d"/>
</div>

We now have a linear constraint equation:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/6a4d5b52-5160-4dd8-90b3-65fafdc68b71"/>
</div>

where:

- ![CodeCogsEqn (29)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/96dbd7fb-e632-40b1-a6e3-73b142c27987): Optical Flow

- ![CodeCogsEqn (31)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/8a9dfdf7-6105-4774-936a-db0005982fcd): Spatial gradient

- ![CodeCogsEqn (32)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/c6ae2339-59a7-4111-ad49-820be730e7f8): Temporal gradient

- The three gradients are easy to calculate using derivative operators. The optical flow vector ![CodeCogsEqn (29)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/96dbd7fb-e632-40b1-a6e3-73b142c27987) is what we are searching for.

- This equation shows that if we have a flow vector and we apply it to the changes in the image over space, it will be completely balanced out by the changes in the image over time. This makes sense because we're assuming that the brightness of the image won't change.

You might notice that we can't solve the optical flow equation directly for the variables ```u``` and ```v``` because we only have **one equation** but **two unknowns**.

The geometric interpretation of the equation above is such that for any point ```(x,y)``` in the image, its potical flow ```(u,v)``` lies on the line:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/37c4eef5-9c2e-4bc3-9e86-9304a8b2c05f"/>
</div>

We know ```(u,v)``` lies on the line but we do not know exactly where. However, out Optical Flow can be split up into 2 components ![CodeCogsEqn (42)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/eef12a49-99ca-4c15-850d-5dd9df0ab18d) which is the **Normal Flow** and ![CodeCogsEqn (43)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/0c4ca216-1eb2-40ff-a99d-10b293a6bba3) which is the **Parallel Flow**. 

We can easily computer the Normal Flow from just the Constraint line using the direction of the normal flow and the magnitude of it:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/4961768b-4fda-45cd-8931-0ed8f0122089"/>
</div>

However, we **cannot** determine ![CodeCogsEqn (45)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/013cc552-7d55-4c81-810c-71701eb7d347), the optical flow compnent parallel to he constraint line.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/a408ee47-53a8-43b2-b986-bfd7cf2e3c5d" width="300" height="250"/>
</div>

#### 1.2.1 Aperture Problem

It seems that the inherent limitations of the optical flow problem are not exclusive to the algorithms being developed. They also apply to us humans. An excellent example is the ```Aperture Problem``` 

It's important to note that we don't observe the complete image of just one object. Our image contains multiple objects, and each local region within the image can have a potentially different flow. Therefore, it becomes necessary for us to focus on a small local patch, which we will refer to as our aperture.

<div align="center">
  <img src="https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/5d2809ce-9806-4c7d-9aa6-f7c2f7cceb37" width="250" /> 
  <img src="https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/6fb0bdeb-6ea6-4ef6-9ad0-d1237e30d573" width="250" />
  <img src="https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/fffdc418-cce1-46a9-b60e-51d5c45c436c" width="250" />
  <p><b> Fig 4. The line moves downward diagonally (left). However, through the aperture, it seems to move upward diagonally (middle). We can only tell the motion locally in the direction perpendicular to the edge.</b></p>
</div>

<div align="center">
    <p>Image Source: <a href="https://datahacker.rs/">Data Hacker</a></p>
</div>

Therefore, what both you and I perceive is the normal flow, which represents the motion of the line we are observing perpendicular to the line itself. We are unable to directly measure the actual flow. Thus, locally, we can only estimate the **normal flow**, as shown in this demonstration. This challenge in estimating the optical flow is commonly known as the **aperture problem**.

<a name="sparse"></a>
### 1.3 Sparse Optical Flow
So far, we have seen that the optical flow estimation problem is an under constraint problem. Sparse optical flow algorithms work by selecting a specific set of pixels, typically consisting of interesting **features** such as **edges** and **corners**, to track their corresponding velocity vectors representing motion. These chosen features are then passed through the optical flow function from one frame to the next, ensuring that the same points are consistently tracked across frames. 

We're going to assume that for each pixel, the motion field and hence the optical flow is constant within a small neighborhood ```W``` around that pixel neighborhood. By considering a neighborhood of pixels around each pixel, we enhance the accuracy of optical flow estimation. This approach leads us to the ```Lucas-Kanade method```, a technique widely used for estimating optical flow. Other various implementations of sparse optical flow methods exist, including the well-known ```Horn-Schunck``` method, the ```Buxton-Buxton``` method, and more.

Suppose we have a point ```(k,l)``` in our window ```W```:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/cae71126-dfd3-48ba-a8b5-057312326a58" width="400" height="250"/>
  <p><b> Fig 5. Aplying Lucas-Kanade method for sparse optical flow. </b></p>
</div>

If our window ```W``` is of size ```nxn```, we have ![CodeCogsEqn (48)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/9b0e9678-f24a-45a5-9900-b40a3b4adb43) points. Hence, in matrix form we have:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/66569f0f-c29f-411d-8e81-95658ff5f2f3" />
</div>

Notce that we now have ![CodeCogsEqn (55)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/08d0517b-5761-446a-a0d7-3a85445594f5) equations and 2 unknowns! We can solve for ```u``` as such:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/2e1ad727-d653-43d6-b33f-eee6d42f5287" />
</div>


For this method to work we need, ![CodeCogsEqn (52)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/0ab48769-70aa-48df-b604-7d1fee5953cb) to be invertible and ![CodeCogsEqn (52)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/54de2a3a-2785-4b84-bdf8-1f15af1ebe68) to be well-conditioned.

Below are some examples when this method will output poor results:

1. Equations for all pixels in window are more or less the same.
2. Prominent gradient in one direction.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/92199196-bd47-4fd2-925e-dead816c8d45" width="600" height="450"/>
</div>

#### 1.3.1 Coarse-to-Fine Estimation

Now let's examine a scenario where two images are captured in rapid succession. Due to the proximity of the car to the camera, its motion will be significant, possibly spanning several pixels based on perspective projection. In such a case, we cannot assume that the changes in ```x``` and ```y``` coordinates will be small. The Taylor series approximation, which relies on linearity, is **no longer applicable** for the image and brightness variations. Consequently, the simple linear optical flow constraint equation is **no longer valid**.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/5c8eb16b-c027-4ccb-b5d5-4e1c4017289b" width="400" height="350"/>
  <p><b> Fig 8. Pyramidal Lucas-Kanade (LK) Optical Flow is an algorithm that estimates the movement of sparse feature points between frames. </b></p>
</div>
<div align="center">
    <p>Image Source: <a href="https://www.researchgate.net/figure/Fig-5-Lucas-Kanade-with-pyramid_fig1_282913643">OPTICAL FLOW FOR MOTION DETECTION WITH MOVING BACKGORUND</a></p>
</div>

To address the challenge of an under-constrained optical flow problem, we can compute ```lower resolution``` versions of the images by ```downsampling``` them. This downsampling process involves ```averaging pixel values``` within small windows to create new low-resolution images. As we move to lower resolutions, the ```magnitude of motion decreases```, allowing the optical flow constraint equation to become **valid** again. By iteratively downsampling and adjusting the scale of motion, we can reach a resolution where the optical flow constraint equation holds **true**, enabling accurate estimation of optical flow.

Below are the steps of Coarse-to-Fine Estimation algorithm using Lucas-Kanade:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/dce17590-5b20-42e5-adbf-a7a7cd1fbc9f" width="500" height="450"/>
</div>


Note: ```In general, moving objects that are closer to the camera will display more apparent motion than distant objects that are moving at the same speed due to motion parallax.```

#### 1.3.1 Lucas-Kanade Implementation
Sparse optical flow algorithms select a subset of feature points, such as **corners**, in the image and track their motion vectors between frames. The ```Shi-Tomasi corner``` detector is commonly used to identify these feature points. Below is an example why we chose Shi-Tomasi orver Harris Corner detection algorithm.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/903baf34-ee6f-4d5e-b3ee-3915baed7334" width="400" height="350"/>
  <p><b> Fig 8. Harris v/s Shi-Tomasi Corner Detection. </b></p>
</div>
<div align="center">
    <p>Image Source: <a href="https://datahacker.rs/](https://medium.com/pixel-wise/detect-those-corners-aba0f034078b">Medium</a></p>
</div>

We first need to initialize the parameters for Shi-Tomasi. We chose to select ```100``` points with a quality level threshold of ```0.3``` and the minimum euclidean distance allowed between detected corners to be ```7```.

```python
# Shi-Tomasi Parameters
shitomasi_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7)
```
In Lucas-Kanade parameters we have a windows size of ```15 x 15``` which refer to the size of the window or neighborhood used for computing the optical flow and ```2``` for the maximum pyramid level used for the multi-resolution approach.

```python
# Lucas Kanade Parameters
lk_params = dict(winSize=(15,15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
```
We will read the first frame of our video in grayscale and get the best features or corners using the ```goodFeaturesToTrack``` function which is an implementation of the Shi-Tomasi corner detector. 

```python
# Get first frame
frame_gray_init = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Get features from Shitomasi
edges = cv2.goodFeaturesToTrack(frame_gray_init, mask=None, **shitomasi_params)
```

Then we need to use these points (edges) detected and feed them into the ```calcOpticalFlowPyrLK``` function and track them (new_edges). The function detects and tracks feature points in the subsequent image frame based on their initial positions in the previous frame.

```python
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    new_edges, status, error = cv2.calcOpticalFlowPyrLK(frame_gray_init, frame_gray, edges, None, **lk_params)
```

When we get the coordinates of a corner in the previous and next frame, we can calculate its displacement. Using this information we can create a condition whereby we track only moving feaures or visualize them in another color as in the example below.
```python
    # Go through each matched feature, and draw it on the second image
    for new, old in zip(good_new, good_old):
        a, b = new.ravel() # Current corner coordinates
        c, d = old.ravel() # Previous corner coordinates

        displacement_x = a - c
        displacement_y = b - d
```

Only moving corners are red while static ones are yellow: 


https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/a1f15766-e0a3-4753-bbaf-5162ecf429e1



<a name="dense"></a>
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
1. https://nanonets.com/blog/optical-flow/
2. https://www.youtube.com/watch?v=lnXFcmLB7sM&list=PL2zRqk16wsdoYzrWStffqBAoUY8XdvatV&ab_channel=FirstPrinciplesofComputerVision
3. https://nanonets.com/blog/optical-flow/#optical-flow-using-deep-learning
4. https://www.mathworks.com/matlabcentral/fileexchange/94095-obstacle-avoidance-with-camera-sensor-using-simulink
5. https://medium.com/swlh/what-is-optical-flow-and-why-does-it-matter-in-deep-learning
6. https://towardsdatascience.com/a-brief-review-of-flownet-dca6bd574de0
7. https://zainmehdiblog.wordpress.com/vision-based-obstacle-avoidance/
8. https://github.com/philferriere/tfoptflow/blob/master/README.md
9. https://datahacker.rs/calculating-sparse-optical-flow-using-lucas-kanade-method/
10. https://learnopencv.com/optical-flow-using-deep-learning-raft/
11. https://pub.towardsai.net/eccv-2020-best-paper-award-a-new-architecture-for-optical-flow-3298c8a40dc7
12. https://learnopencv.com/optical-flow-in-opencv/
13. https://prgaero.github.io/2019/proj/p4b/#rviz
14. http://prg.cs.umd.edu/enae788m
15. https://www.coursera.org/learn/robotics-perception/lecture/DgSNW/3d-velocities-from-optical-flow
16. 
