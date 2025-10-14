import cv2

# --- TRY CHANGING THIS NUMBER ---
CAMERA_INDEX = 0 
# --------------------------------

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print(f"❌ Error: Could not open camera at index {CAMERA_INDEX}.")
    print("Is it being used by another app (Zoom, Teams)? Is it disabled?")
else:
    print(f"✅ Success! Camera at index {CAMERA_INDEX} is working.")
    
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Camera Test - Press any key to exit", frame)
        cv2.waitKey(0) # Wait until you press a key
    else:
        print("❌ Error: Could not read a frame from the camera.")

# Clean up
cap.release()
cv2.destroyAllWindows()