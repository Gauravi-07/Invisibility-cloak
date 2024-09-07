import numpy as np
import cv2
import time

def background_create(cap, num_frames=30):
    print("Creating background. Step out of the frame")
    backgrounds = []
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            backgrounds.append(frame)
            print(f"Frame {i+1}/{num_frames} captured")
        else:
            print(f"Warning: Could not read frame {i+1}/{num_frames}")
        time.sleep(0.1)
    if backgrounds:
        return np.median(backgrounds, axis=0).astype(np.uint8)
    else:
        raise ValueError("No frames found")

def masking(frame, lower1, upper1, lower2, upper2):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create two masks for the two color ranges
    mask1 = cv2.inRange(hsv, lower1, upper1)  # Bright red range
    mask2 = cv2.inRange(hsv, lower2, upper2)  # Dark red range

    # Combine both masks
    mask = mask1 + mask2

    # Perform morphological operations to remove noise and refine the mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)

    return mask

def cloak_effect(frame, mask, background):
    mask_inv = cv2.bitwise_not(mask)  # creates inverse of the mask
    fg = cv2.bitwise_and(frame, frame, mask=mask_inv)  # extracts the non-cloak area from current frame using inverse mask
    bg = cv2.bitwise_and(background, background, mask=mask)  # extracts the cloak area from the pre-captured background using the original mask
    return cv2.add(fg, bg)  # combines the cloak and non-cloak area

def main():
    print("Opening camera")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera")
        exit()

    try:
        background = background_create(cap)
    except ValueError as e:
        print(f"Error: {e}")
        cap.release()
        exit()

    # Define color ranges for bright red and dark red in HSV
    lower1 = np.array([0, 120, 70])    # Lower bound for bright red
    upper1 = np.array([10, 255, 255])  # Upper bound for bright red
    lower2 = np.array([170, 120, 70])  # Lower bound for dark red
    upper2 = np.array([180, 255, 255]) # Upper bound for dark red

    print("Starting main loop. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            time.sleep(1)
            continue

        # Create mask for both bright red and dark red
        mask = masking(frame, lower1, upper1, lower2, upper2)
        result = cloak_effect(frame, mask, background)

        cv2.imshow("Cloak", result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
