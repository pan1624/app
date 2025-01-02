import sys
import cv2
import mediapipe as mp
import numpy as np

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points.
    """
    ab = np.array([a[0] - b[0], a[1] - b[1]])
    bc = np.array([c[0] - b[0], c[1] - b[1]])
    cosine_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python calculate_similarity.py <uploaded_video_path> <reference_video_path>")
        sys.exit(1)

    uploaded_video_path = sys.argv[1]
    reference_video_path = sys.argv[2]


mp_pose = mp.solutions.pose

# Video paths
#uploaded_video_path = r"C:\Users\sspan\Desktop\work\app\shoulder_press.mp4"
#reference_video_path = r"C:\Users\sspan\Desktop\work\app\shoulder_press.mp4"

# Open videos
uploaded_cap = cv2.VideoCapture(uploaded_video_path)
reference_cap = cv2.VideoCapture(reference_video_path)

if not uploaded_cap.isOpened() or not reference_cap.isOpened():
    print("Error: Unable to open one or both videos.")
    exit()

frame_count = 0
total_angle_difference = 0

# Mediapipe Pose model
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while uploaded_cap.isOpened() and reference_cap.isOpened():
        ret1, frame1 = reference_cap.read()
        ret2, frame2 = uploaded_cap.read()

        if not ret1 or not ret2:
            break

        # Detect poses
        results1 = pose.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
        results2 = pose.process(cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))

        if results1.pose_landmarks and results2.pose_landmarks:
            landmarks1 = results1.pose_landmarks.landmark
            landmarks2 = results2.pose_landmarks.landmark

            angle_joints = {
                "Left Elbow": (11, 13, 15),
                "Right Elbow": (12, 14, 16),
                "Left Knee": (23, 25, 27),
                "Right Knee": (24, 26, 28)
            }

            frame_angle_differences = []

            for joint_name, (a_id, b_id, c_id) in angle_joints.items():
                a1, b1, c1 = (landmarks1[a_id].x, landmarks1[a_id].y), \
                             (landmarks1[b_id].x, landmarks1[b_id].y), \
                             (landmarks1[c_id].x, landmarks1[c_id].y)
                a2, b2, c2 = (landmarks2[a_id].x, landmarks2[a_id].y), \
                             (landmarks2[b_id].x, landmarks2[b_id].y), \
                             (landmarks2[c_id].x, landmarks2[c_id].y)

                angle1 = calculate_angle(a1, b1, c1)
                angle2 = calculate_angle(a2, b2, c2)

                angle_difference = abs(angle1 - angle2)
                frame_angle_differences.append(angle_difference)

            if frame_angle_differences:
                total_angle_difference += np.mean(frame_angle_differences)
                frame_count += 1

# Release video resources
uploaded_cap.release()
reference_cap.release()

# Calculate final similarity score
average_angle_difference = total_angle_difference / frame_count if frame_count > 0 else None
final_score = max(0, 100 - average_angle_difference) if average_angle_difference else 0

print(f"{final_score:.2f}")

