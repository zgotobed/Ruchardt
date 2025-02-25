import cv2
import csv

# Input and output video paths
input_video_path = "../Videos/IMG_5327.mp4"  # Change this to your actual video file
output_video_path = "../Videos/OutputFeb25Rusty_run3.mp4"  # MP4 output
csv_file_path = "../CSV Files/coordinates_Feb25Rusty_run3.csv"  # CSV file to save the coordinates

# Open the video file
cap = cv2.VideoCapture(input_video_path)

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Use "mp4v" for MP4 output

# Define the cropping region dimensions
crop_y_start = 800
crop_y_end = frame_height - 200 # To go until the end of the frame
crop_x_start = 200
crop_x_end = 1000

# Validate cropping bounds
if crop_x_start < 0 or crop_y_start < 0 or crop_x_end > frame_width or crop_y_end > frame_height:
    raise ValueError(f"Cropping bounds are out of the frame dimensions! "
                     f"Frame size: ({frame_width}x{frame_height}), "
                     f"Crop region: x({crop_x_start}-{crop_x_end}), y({crop_y_start}-{crop_y_end})")


# Create a VideoWriter object with the correct output size
output_width = crop_x_end - crop_x_start
output_height = crop_y_end - crop_y_start
out = cv2.VideoWriter(output_video_path, fourcc, fps, (output_width, output_height))

# Set minimum and maximum contour area to filter noise
MIN_CONTOUR_AREA = 500  # Adjust as needed
MAX_CONTOUR_AREA = 10000000  # Adjust based on expected pendulum size


with open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    
    # Write the header to the CSV file
    writer.writerow(['Time', 'x', 'y'])
    # Process each frame
    counter = 0
    while cap.isOpened():
        counter += 1
        print(counter)
        ret, frame = cap.read()
        
        if not ret:
            break  # End of video

        # Crop the frame based on defined coordinates
        cropped = frame[crop_y_start:crop_y_end, crop_x_start:crop_x_end]
        if(counter == 2):
            cv2.imwrite('cropped3.jpg',cropped)
        # Convert to grayscale
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to smooth out noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply thresholding
        _, thresh = cv2.threshold(blurred,210, 255, cv2.THRESH_BINARY)
        cv2.imshow("text",thresh)
        cv2.waitKey(1)
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Filter contours based on area
        valid_contours = [
            c for c in contours if MIN_CONTOUR_AREA < cv2.contourArea(c) < MAX_CONTOUR_AREA
        ]
        # print(len(valid_contours))

        for contour in valid_contours:
            
            # Calculate moments of the contour
            moments = cv2.moments(contour)

            # Calculate the centroid (midpoint)
            if moments["m00"] != 0:  # Prevent division by zero
                cx = moments["m10"] / moments["m00"]
                cy = moments["m01"] / moments["m00"]

                # Draw the midpoint on the frame
                # print("printing dot")
                cv2.circle(cropped, (int(cx), int(cy)), 5, (0, 0, 255), -1)  # Red dot for centroid
                writer.writerow([counter / fps, cx, cy])  # Use frame number divided by fps to get time in seconds

            else:
                print("invalid contour moment")
        # Draw contours on the cropped frame
        cv2.drawContours(cropped, valid_contours, -1, (0, 255, 0), 2)  # Green color
        # cv2.imshow("frame", cropped)
        # cv2.waitKey(0)
        # Write the processed frame to the output video
        out.write(cropped)

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
