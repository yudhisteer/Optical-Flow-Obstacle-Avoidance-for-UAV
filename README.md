# Optical Flow Obstacle Avoidance for UAV

## Problem Statement

In the realm of complex urban deliveries, designing a ```sense-and-avoid``` system for UAVs that can effectively track **moving objects** poses a significant challenge. Existing object detection models, while powerful, have limitations in detecting **all** types of objects in motion. Real-world scenarios present **unpredictable** moving objects such as children playing frisbee, running pets, or flying kites and so on, that can potentially jeopardize UAV navigation.

To address this challenge, a sense-and-avoid system capable of detecting **any** object in **motion** would revolutionize UAV deliveries in bustling city environments. By accurately tracking moving objects, the system would enhance ```safety```, ```efficiency```, and ```adaptability```. It would enable effective ```collision avoidance```, ensuring the safety of the UAV and the surrounding environment. Additionally, it would provide real-time information for optimal flight ```path planning```, enabling seamless navigation in dynamic and unpredictable urban scenarios.

With our innovative approach, we aim to develop an **unsupervised sense-and-avoid system** for UAVs. By leveraging distinctive ```motion characteristics```, our system eliminates the need for extensive **labeling** of object classes. This unsupervised method offers significant advantages, particularly in complex urban environments where encounters with **unknown objects** are likely. Our system's adaptability enables it to effectively detect and respond to **diverse scenarios** and mitigate the risk of encountering objects that were not present in our training data.

## Abstract
In our study, we conducted a comprehensive analysis of ```optical flow``` techniques and their suitability for obstacle detection and avoidance in UAV applications. Specifically, we investigated the pros and cons of sparse and dense optical flow approaches. ```Sparse optical flow```, known for its **computational efficiency** and **quick processing**, was found to be a viable option for **real-time obstacle detection**. However, it exhibited **lower accuracy** in capturing fine-grained motion details.

On the other hand, ```dense optical flow``` exhibited **superior performance** in terms of accuracy, capturing **detailed motion** information in the scene. However, it came at the cost of increased **computational complexity** and **processing time**. Despite these trade-offs, we discovered that both sparse and dense optical flow techniques hold great promise in detecting moving objects when combined with ```"low-cost"``` image analysis methods.

Below is a video showcasing ```"The Horse in Motion"``` from 1878, captured by **Eadweard Muybridge**. In this groundbreaking study, Muybridge utilized a series of **multiple photographs** to showcase the progressive motion of a galloping horse. (Video source: [Sallie Gardner at a Gallop](https://www.youtube.com/watch?v=IEqccPhsqgA&ab_channel=silentfilmhouse))

https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/2f784426-73b6-4681-9b02-cbd9bc7e8783


## Plan of Action
1. [Understanding Optical Flow](#understanding-optical-flow)

2. [Motion Field](#motion-field)

3. [Optical Flow Constraint Equation](#equation)

4. [Sparse Optical Flow](#sparse)

5. [Dense Optical Flow](#dense)

6. [Obstacle Avoidance](#obs)

7. [Further Improvements](#further)





---------------------

<a name="understanding-optical-flow"></a>
## 1. Understanding Optical Flow
Optical flow is a method used to analyze the **apparent** motion of objects in a sequence of images or video. It is of paramount importance that we put emphasis on the work "apparent" as we are not analyzing the direct physical motion characteristics of an object itself.

The concept of "apparent motion" can be traced back in ```Gestalt phychology``` which explores how humans **perceive** and **interpret** ```visual stimuli```. It emphasizes that ```the whole is different from the sum of its parts``` and focuses on the organization and grouping of visual elements to form meaningful perceptual experiences. 

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/2f18facc-c9b4-48d1-9215-b442da3cc411" width="400" height="500"/>
  <p><b> Fig 1. Illustration of several grouping principles. Common fate is a principle of Gestalt psychology that refers to the perceptual grouping of objects based on their shared motion or direction. </b></p>
</div>
<div align="center">
    <p>Image Source: <a href="https://www.researchgate.net/figure/Illustration-of-several-grouping-principles-Adapted-from-Perceptual-Organization-in_fig1_230587594">A Century of Gestalt Psychology in Visual Perception</a></p>
</div>


It involves tracking the movement of ```individual pixels``` or small regions over time, providing insights into how objects are moving within a scene. While images capture the ```spatial``` aspects of a scene, videos add the ```temporal``` dimension, enabling the perception of motion and dynamic changes.

When comparing two images, our objective is to determine the corresponding locations of points in the first image within the second image. This mapping of points is referred to as the ```motion field```. By analyzing how **brightness patterns** in the first image relate to their positions in the second image, we can approximate the motion field. This involves tracking the ```displacement of brightness patterns``` to infer the underlying ```motion of points``` between the images. Optical flow provides an approximation of the underlying motion field based on the observed ```shifts in brightness patterns between consecutive frames```.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/867a227e-0b8a-4b40-bb6e-01c9fe792b0e" width="600" height="300"/>
  <p><b> Fig 2. Flow map where the direction of the arrow indicates the motion's direction, while the length of the arrow represents the speed or magnitude of the motion.</b></p>
</div>
<div align="center">
    <p>Image Source: <a href="https://www.researchgate.net/figure/Optic-flow-vectors-for_fig4_266064740">Optical Flow</a></p>
</div>


Each pixel in the image has an optical flow vector representing the ```motion of brightness patterns``` at that point. The vector's ```length``` indicates the ```speed``` of motion, and its ```direction``` indicates the specific ```direction``` of motion on the image plane. In an ideal scenario, optical flow perfectly matches the motion field, accurately representing object movement. However, in practice, optical flow and the motion field are not always identical due to **occlusions** and **complex motion patterns**, leading to incomplete and less accurate motion information. It's important to note that the motion of points between the images depends on the depth of the points, as this influences their perceived motion.

-------------------

<a name="motion-field"></a>
## 2. Motion Field
Consider a point in a scene that is moving in a certain direction in three-dimensional space. This movement is projected onto the image plane, resulting in a motion on the image known as the ```motion field``` for that point. However, measuring this motion field directly is often not possible. What we can measure instead is the motion of brightness patterns in the image, which is referred to as ```optical flow```. Optical flow provides insights into how the brightness patterns within the image change and move, but it is an approximation of the actual motion field.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/097737fa-3c43-4df3-9fa7-e1ff6cde96d1" width="600" height="250"/>
  <p><b> Fig 3. Ouchi Pattern (left) and Donguri Wave Illusion (right).</b></p>
</div>
<div align="center">
    <p>Image Source: <a href="https://www.ritsumei.ac.jp/~akitaoka/wave-e.html">Waves</a></p>
</div>


Figure above shows examples of when the motion field is not equal to the optical flow. The images are static but when when we move our eyes around the image, the latter seems to be moving. We have an optical flow in our visual system but their is **no** motion field!

Another example is the simulation below, whereby you can see the cube moving and we can see the optical flow with the green lines however, no optical flow is detected for the sphere which is rotating twice as fast as the cube.

https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/ac1b3844-be3a-4238-aeba-fac08f39926d

In the example below, we see the cube and the cylinder moving and we can also see their optical flows. However, notice tha the front of the cylinder has higher opical flow vectors since it is closer to the camera. Secondly, we have no optical flow for the top surface of the cylinder although it is rotating at the same angular speed. However, we cannot see it as there is no **"apparent motion"**, no contrast, no patterns, no texture is moving.

https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/4928f4e9-516e-49c8-8c6e-6663d1b08d46


-----------------------

<a name="equation"></a>
## 3. Optical Flow Constraint Equation

Let's say we have two images of a scene taken in quick succession: a yellow car moving on a road. Now focus our attention on a single point within this window: side-view mirror of the car. We assume that the position of the point is ![CodeCogsEqn (9)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/9fc23ee6-5ba8-43d2-b1a1-d8539d0b800e).
Now, at time ![CodeCogsEqn (11)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/f805c821-8701-429c-bdf5-246033377c29), that point has moved to a new location: ![CodeCogsEqn (10)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/83e14c2f-d1bd-4383-a769-7c679a364079)
So the ```displacement``` of the point ![CodeCogsEqn (9)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/31734bf1-797d-472a-984f-8779c6d7e847) can be said to be ![CodeCogsEqn (21)](https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/cb1df29e-4098-449d-8e0c-a8071f4d3f37).

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/efb948a1-1da6-4eba-a2ad-091d9e74e914" width="1000" height="250"/>
  <p><b> Fig 4. Displacement of an object over a short interval of time. </b></p>
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

### 3.1 Aperture Problem

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

------------------

## 4. Sparse Optical Flow
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

### 4.1 Coarse-to-Fine Estimation

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

### 4.2 Lucas-Kanade Implementation
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

Using a certain threshold, moving corners are red while static ones are yellow: 

https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/a1f15766-e0a3-4753-bbaf-5162ecf429e1

---------------------

<a name="dense"></a>
## 5. Dense Optical Flow
In sparse optical flow, we computed the optical flow only for a set of features. In dense optical flow, we will conside all pixels in our frame. The computation will be slower but we will get more accurate results.

The main concept of this method involves approximating the neighboring pixels of each pixel using a polynomial function. Recall that in the Lucas-Kanade method, we previously used a linear approximation which relied on a ```first-order Taylor's expansion```. Now, we aim to improve the accuracy of the approximation by incorporating ```second-order values```.Several method are available such as:

- **Dense Pyramid Lucas-Kanade** 
- **Farneback**
- **Robust Local Optical Flow (RLOF)**

The output of the dense optical flow algorithm can be visualized using the HSV color scheme. By employing the ```cv2.cartToPolar``` function, we can convert the displacement coordinates ```(dx, dy)``` of each pixel into polar coordinates, representing the **magnitude** and **angle** for that pixel. In this visualization scheme, we map the **angle** to the **Hue** channel and the **magnitude** to the **Value** channel, while keeping the **Saturation** channel **constant**. Hence, object which moves faster will appear to be brighter and depending on the direction they are moving, they will have different colors based on the color wheel below:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/3c72677b-90f4-4e74-9f6e-b63883075064" width="300" height="300"/>
  <p><b> Fig 8. HSV color scheme </b></p>
</div>
<div align="center">
    <p>Image Source: <a href="https://www.researchgate.net/figure/The-optical-flow-field-color-coding-Smaller-vectors-are-lighter-and-color-represents-the_fig1_266149545">Variational-Bayes Optical Flow</a></p>
</div>


Below is an example of the Farneback algorithm:

```python
    # Farneback function
    flow = cv2.calcOpticalFlowFarneback(frame_gray_init, frame_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
```

We calculate the magnitude and angle of each vectors and map them to the Hue and Value channel of the HSV color scheme. 

```python
    # Get magnitude and angle of vector
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1]) #x #y

    # Hue
    hsv[..., 0] = (angle * 180 / (np.pi / 2))

    # Value: Intensity
    hsv[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
```


Below is an example of me running towards the camera. The Dense Lucas-Kanade algorithm outperforms the other two algorithms. While Farneback captures the outline of the shirt, Dense Lucas-Kanade provides a more detailed representation of the entire object. Although RLOF exhibits some noise in the output, it still demonstrates a notable optical flow mapping.

https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/ddc40869-df2f-432f-9b98-8eb14220ffcf

This video of me running away from the camera seems to show more or less the same results as the one above.

https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/8bd773f4-c6ef-48d8-9952-fdc66cf9f387

In the presence of an obstacle, the Dense Lucas-Kanade and RLOF algorithms show noticeable noise in scenes with no motion. However, the Farneback algorithm produces significantly less noise, enabling a clear outline of the obstacle even with minimal movement. For videos with small motions, RLOF and Dense Lucas-Kanade may not be suitable, while Farneback performs better.

https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/2753c2f7-8d7f-4e2d-8ddb-e0179717c21b

In a video where a drone is moving towards and away from a tree, recorded under challenging lighting conditions with numerous shadows, Dense Lucas-Kanade algorithm appears to perform better. It accurately captures the motion, especially when the drone is approaching the tree at high speed. On the other hand, Farneback algorithm exhibits a granular output that can be considered redundant. RLOF algorithm demonstrates poor performance under these conditions.

https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/a0cfa56f-e937-4063-80b6-7b0b84971e5d

Please note that I have not conducted a thorough analysis to benchmark these algorithms. My comments and observations are solely based on visual examination of the results. To accurately assess their performance, further testing and analysis would be required to quantify their effectiveness.

-----------------

## 6. Obstacle Avoidance
Now, we need to utilize the output from the Lucas-Kanade method in order to devise an **Obstacle Avoiding Algorithm**. We will test our solution on the DJI Tello drone. We will first assume a simple scenario whereby the drone is approaching an obstacle head front. Based on some criteria, we want our drone to turn either ```left``` or ```right```. However, notice that we also have an **unwanted object** in our background which may perturbed our system.

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/3f868d90-adcd-4954-9cd4-8a27e21b5638" width="700" height="350"/>
  <p><b> Fig 8. The obstacle the drone will need to avoid plus an unwanted object in the background. </b></p>
</div>

### 6.1 Obstacle Avoidance with Sparse Optical Flow

We try to implement the algorithm step by step:

1. In my first try, I tried to display the ```important features``` on a mask. We can see the outline of the obstacle but also some features were extracted from the object in the background. 

2. In the second iteration, I divided the mask into two - the ```vertical line```. Here, I wrote a condition on the steering such that if we have more features on the right than on the left then turn left else turn right. However, notice that the object in the background can still **bias** the system.

3. In the 3rd try, I created a ```Region of Interest (ROI)``` - black rectangle - such that we only want to detect features within our ROI. Now, the object in the background is no longer a problem.

4. Finally, I modified the code such that only the features in the ROI will be displayed. I am also calculating the ```sum of vector magnitudes``` in both halves. Below is the code:

```python
            # Iterate through each trajectory
            for trajectory in trajectories:
                # Get the x and y coordinates of the current and previous points
                x, y = trajectory[-1]
                prev_x, prev_y = trajectory[-2]

                # Check if the current point is within the ROI
                if roi_x <= x <= roi_x + roi_width and roi_y <= y <= roi_y + roi_height:
                    # Calculate the magnitude of the optical flow vector
                    magnitude = np.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)

                    # Check if the current point is on the left or right side
                    if x < midpoint:
                        total_magnitude_left += magnitude
                    else:
                        total_magnitude_right += magnitude
```


<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/443d8bdc-146c-4161-9238-5eb33e4d652d" width="650" height="500"/>
  <p><b> Fig 8. Pyramidal Lucas-Kanade (LK) Optical Flow is an algorithm that estimates the movement of sparse feature points between frames. </b></p>
</div>

In summary: the scenario involves a figure divided into **two quadrants**, each with its own direction for flow vectors. This observation is useful for obstacle avoidance. To extract features, a black rectangle representing a predefined patch within the image is focused on. The purpose of this patch is to detect obstacles directly **in front of** the drone, disregarding objects outside this line of sight. The vertical black line divides the patch into left and right sections. By calculating the ```sum of vector magnitudes``` in both halves, the presence and magnitude of obstacles in each direction can be determined.

Now, we need  to test it in real-time on our drone.  Below are some insights:

- **Sparse Feature Detection**: Lucas-Kanade relies on ```sparse feature detection```. It tracks a limited number of specific points or corners in the image. When dealing with complex scenes such as the tree outside in the video, it results in incomplete or inaccurate obstacle detection.

- **Limited Robustness to Illumination Changes**: The algorithms can be sensitive to changes in ```lighting conditions```. Illumination variations can affect the accuracy of feature detection and tracking, leading to unreliable results in different lighting conditions. 

- **Difficulty in Handling Large Displacements**: The Lucas-Kanade method assumes that the ```motion between frames is small```, which limits its effectiveness in scenarios with large displacements. When objects move significantly between frames, the assumption of small motion breaks down, and the accuracy of the method decreases. 

https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/0292d1bf-d519-44e9-887a-fd72e02230fb

- **Lack of Robustness to Textureless Regions**: When detecting corners or features in the image, they may struggle in ```textureless``` or ```low-texture regions``` where distinctive features are sparse or non-existent. 

- **Computational Complexity**: The Lucas-Kanade method involves iterative calculations to estimate the motion vectors, which can be ```computationally expensive```. In real-time applications, this computational complexity can limit the system's ability to process frames in a timely manner, affecting the overall performance of the obstacle avoidance system.

Overall, while Lucas-Kanade and Shi-Tomasi algorithms provide valuable techniques for optical flow-based obstacle avoidance, their limitations should be considered when applying them to real-world scenarios.


### 6.2 Obstacle Avoidance with Dense Optical Flow
The output that we get from Dense optical flow algorithm are the magnitude and angle of the vectors which we mapped to the value and hue of the HSV color sceheme respectively. Objects that move faster will be brighter hence, have a high intensity value. Objects that are close to the camera will also appear to move faster due to motion parallax hence, we can use this information too. From the color scheme above, we can see that "green" and "orange-yellow" will be mapped to objects that will be moving towards the camera. We will use these information in order to design our obstacle avoidance algorithm.

Dense optical flow is already computationally expensive hence, I did not want to use CNN or other Deep Learning methods to check for obstacles. I want to rely on ```image analysis``` in order to detect the obstacles in each frame. Based on the detection, we will be able to devise the control for the drone in order to avoid the obstacle.

1. To extract important ```intensity``` information and disregard hue, I converted the image to **grayscale**.

2. To reduce ```noise``` and emphasize ```important features```, I applied a **Gaussian blur** to the image.

3. Using **Otsu's thresholding** method, I separated the image into ```foreground``` and ```background```.

4. By **dilating** the thresholded image, I expanded the white region to ```highlight the foreground```.

5. I utilized c**onnected components** to label and extract ```connected regions``` in the binary image.

6. After identifying the connected regions, I **filtered** out small regions based on their ```area```.

7. Finally, a **bounding box** was drawn around the regions whose area met the specified ```threshold```.


```python
def plot_image_threshold(gray_image, method, threshold=150):

    # apply gaussian blur
    gray_image = cv2.GaussianBlur(gray_image, (7, 7), 0)

    if method == cv2.threshold:
        if threshold != 0:
            # apply binary thresholding
            T, img_thresh = method(gray_image, threshold, 255, cv2.THRESH_BINARY) # THRESH_BINARY_INV
            print(T)
        else:
            # apply binary thresholding
            T, img_thresh = method(gray_image, threshold, 255, cv2.THRESH_BINARY| cv2.THRESH_OTSU) # THRESH_OTSU # THRESH_BINARY # THRESH_BINARY_INV
            print(T)
    else:
        # apply adaptiveThreshold thresholding
        img_thresh = method(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, threshold, 10) # ADAPTIVE_THRESH_MEAN_C # ADAPTIVE_THRESH_GAUSSIAN_C

    # Apply mask to remove background
    # img_thresh = cv2.bitwise_and(gray_image, gray_image, mask=img_thresh) # original image with no background
    return img_thresh
```

```python
def plot_image_dilation(img_thresh):
    ## apply a series of dilations
    #img_dilated = cv2.erode(img_thresh.copy(), np.ones((10, 10), np.uint8), iterations=2)
    img_dilated = cv2.dilate(img_thresh.copy(), np.ones((10, 10), np.uint8), iterations=4)

    return img_dilated
```

Below are the results of the image analysis on a one frame:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/5f7a510c-1a54-4ce0-b7be-76000ed88603" />
</div>

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/0be4995c-97eb-4ef0-b3cc-03afd46c9c70" />
</div>


```python
def plot_image_connected(img_dilated, image):
    # Perform connected component analysis
    output = cv2.connectedComponentsWithStats(img_dilated, 4, cv2.CV_32S)
    (num_labels, labels, stats, centroids) = output

    # Create a copy of the original image to draw rectangles on
    img_with_rectangles = np.copy(img_dilated)
    img_copy = np.copy(image)

    # Iterate over each component (excluding background label 0)
    for label in range(1, num_labels):
        # Get the statistics for the current component
        left = stats[label, cv2.CC_STAT_LEFT]
        top = stats[label, cv2.CC_STAT_TOP]
        width = stats[label, cv2.CC_STAT_WIDTH]
        height = stats[label, cv2.CC_STAT_HEIGHT]
        area = stats[label, cv2.CC_STAT_AREA]
        print("Area: ", area)

        # Area to keep
        keepArea = 100000 < area < 300000

        # If True
        if keepArea:
            print("[INFO] keeping connected component '{}'".format(label))
            # Draw a rectangle around the current component
            cv2.rectangle(img_with_rectangles, (left, top), (left + width, top + height), (255, 255, 255), 2)
            cv2.rectangle(img_copy, (left, top), (left + width, top + height), (255, 255, 255), 2)

    return img_copy
```

Using the bounding box coordinates from the connected components process, I superimpose it on my original flow map:

<div align="center">
  <img src= "https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/38e65eda-6e92-4d60-b0b8-0a12a0395946" width="750" height="400"/>
  <p><b> Fig 8. Pyramidal Lucas-Kanade (LK) Optical Flow is an algorithm that estimates the movement of sparse feature points between frames. </b></p>
</div>

Here's the image analysis process on the whole video of a **moving obstacle**:

https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/8855a08b-ca15-42b2-8dfc-ccd76435ac6c

In the first few frames we have no detection but when the intensity of the flow map is more apparent, it does a pretty good job at identifying the obejct in motion in the frame.

I also tested it on a video of the drone flying towards the tree (**static obstacle**) using the Dense Lucas-Kanade and Farneback method. We have a lot of instance whereby the ground is being detected and this is because the ground being closer to the camera has a higher speed hence, higher intentisy. These are counted as false positives.

https://github.com/yudhisteer/Optical-Flow-Obstacle-Avoidance-for-UAV/assets/59663734/51c76939-5afc-4cb2-8e0a-017b4d5c2fc3

But when the drone approaches the tree, we successfully detect the obstacle and can draw a bounding box to it. Although, in a real-case scenario, we might want to detect the obstacle earlier. I believe this method, though computationally expensive, is a good system to track moving obstacles and not static ones. 





-----------------

## 7. Further Improvements



-------------

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
16. https://www.kaggle.com/code/daigohirooka/optical-flow-estimation-using-raft
17. https://pyimagesearch.com/2021/05/12/adaptive-thresholding-with-opencv-cv2-adaptivethreshold/
18. https://pyimagesearch.com/2021/04/28/opencv-morphological-operations/
19. https://pyimagesearch.com/2021/04/28/opencv-morphological-operations/
