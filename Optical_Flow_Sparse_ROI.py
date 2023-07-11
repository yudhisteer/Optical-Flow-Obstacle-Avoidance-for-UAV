import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


# Get the current directory
current_directory = os.getcwd()
print(current_directory)

# Go back to the parent directory
parent_directory = os.path.dirname(current_directory)
print(parent_directory)

# Set input and output directory
video_path = os.path.join(parent_directory, 'Data', 'walk_4.mp4')
output_video_path = os.path.join(parent_directory, 'Output', 'walk_4_of.mp4')
print(video_path)


# Open the video file
cap = cv2.VideoCapture(video_path)

# Shi-Tomasi Parameters
shitomasi_params = dict(maxCorners=100, qualityLevel=0.5, minDistance=7)

# Lucas-Kanade Parameters
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Read the first frame
ret, frame = cap.read()

# Convert the first frame to grayscale
frame_gray_init = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Get features from Shi-Tomasi
edges = cv2.goodFeaturesToTrack(frame_gray_init, mask=None, **shitomasi_params)

# Create an empty mask
mask = np.zeros_like(frame)

# Define obstacle detection parameters
displacement_threshold = 5

# Get the frame dimensions
frame_height, frame_width = frame.shape[:2]

# Calculate the middle coordinates of the frame
middle_x = frame_width // 2
middle_y = frame_height // 2

# Define the size of the ROI
roi_width = 200
roi_height = 200

# Calculate the top-left and bottom-right coordinates of the ROI
roi_x1 = middle_x - (roi_width // 2)
roi_y1 = middle_y - (roi_height // 2)
roi_x2 = roi_x1 + roi_width
roi_y2 = roi_y1 + roi_height

# Define the region of interest [x1, y1, x2, y2]
region_of_interest = [roi_x1-180, roi_y1-150, roi_x2-40, roi_y2+250]

# Initialize lists to store the average displacements
avg_displacement_x_list = []
avg_displacement_y_list = []

displacement_x_list = []
displacement_y_list = []

frame_number = 0

while True:
    # Read the frame from the video
    ret, frame = cap.read()

    # Break the loop if there are no more frames to read
    if not ret:
        break

    frame_number += 1

    # Print the frame number at the top of the frame
    cv2.putText(frame, f"Frame: {frame_number}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Draw the region of interest
    cv2.rectangle(frame, (region_of_interest[0], region_of_interest[1]), (region_of_interest[2], region_of_interest[3]), (0, 0, 0), 2)

    # Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate optical flow using Lucas-Kanade
    new_edges, status, errors = cv2.calcOpticalFlowPyrLK(frame_gray_init, frame_gray, edges, None, **lk_params)

    # Store the matched features (status=1 means a match)
    good_old = edges[status == 1]
    good_new = new_edges[status == 1]

    # Obstacle detection
    obstacle_detected = False

    for new, old in zip(good_new, good_old):
        x1, y1 = new.ravel()  # Current corner coordinates
        x2, y2 = old.ravel()  # Previous corner coordinates


        displacement_x = x1 - x2
        displacement_y = y1 - y2
        print(displacement_x)
        print(displacement_y)

        # Check if displacement exceeds threshold
        if abs(displacement_x) > displacement_threshold or abs(displacement_y) > displacement_threshold:
            # Potential obstacle detected
            obstacle_detected = True
            mask = cv2.arrowedLine(mask, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            frame = cv2.circle(frame, (int(x1), int(y1)), 3, (0, 255, 0), thickness=-1)

            # Save the average displacements
            displacement_x_list.append(displacement_x)
            displacement_y_list.append(displacement_y)

    # Check if multiple corners within the region of interest show consistent motion towards the camera
    # Get the corners that are in the ROI
    roi_corners = good_new[
        (good_new[:, 0] >= region_of_interest[0]) &
        (good_new[:, 1] >= region_of_interest[1]) &
        (good_new[:, 0] <= region_of_interest[2]) &
        (good_new[:, 1] <= region_of_interest[3])
    ]

    # Check if we have enough corners to perform analysis | Min = 2
    if len(roi_corners) > 2:

        # overall motion of the corners within the ROI.
        #roi_corners[:, 0] = x-coord | roi_corners[0, 0] = first x-coor
        avg_displacement_x = np.mean(roi_corners[:, 0]) - roi_corners[0, 0]
        avg_displacement_y = np.mean(roi_corners[:, 1]) - roi_corners[0, 1]

        # Calculate the average displacement in x and y directions
        avg_displacement_x = np.mean(roi_corners[:, 0] - roi_corners[0, 0])
        avg_displacement_y = np.mean(roi_corners[:, 1] - roi_corners[0, 1])

        # Check if there is any significant motion in the ROI
        if abs(avg_displacement_x) > displacement_threshold or abs(avg_displacement_y) > displacement_threshold:
            # Consistent motion towards or away from the camera in the region of interest
            obstacle_detected = True
            for corner in roi_corners:
                x1, y1 = corner.ravel()
                frame = cv2.circle(frame, (int(x1), int(y1)), 3, (0, 0, 0), thickness=-1)

        # Save the average displacements
        avg_displacement_x_list.append(avg_displacement_x)
        avg_displacement_y_list.append(avg_displacement_y)


    # Overlay the optical flow tracks on the original frame
    output = cv2.add(frame, mask)

    # Display the frame with obstacle detection
    cv2.imshow('Obstacle Detection', output)

    # Wait for the 'q' key to be pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    # Update the previous frame and edges
    frame_gray_init = frame_gray.copy()
    edges = good_new.reshape(-1, 1, 2)

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()

# Plot the average displacements
plt.plot(displacement_x_list, label='Displacement X')
plt.plot(displacement_y_list, label='Displacement Y')
#plt.plot(avg_displacement_x_list, label='Average Displacement X')
#plt.plot(avg_displacement_y_list, label='Average Displacement Y')
plt.xlabel('Frame')
plt.ylabel('Average Displacement')
plt.legend()
plt.show()
