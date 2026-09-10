import cv2
import cv2.aruco as aruco
import numpy as np

MARKER_ROLES = {
    0: "Standby",
    1: "Ambil",
    2: "Lepas",
    3: "Putar CW",
    4: "Putar CCW"
}

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Tidak dapat mengakses kamera.")
        return

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    aruco_params = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, aruco_params)

    print("Mencari ArUco Marker... Tekan 'q' di jendela visual untuk keluar.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame kamera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = detector.detectMarkers(gray)

        if ids is not None:
            aruco.drawDetectedMarkers(frame, corners, ids)
            
            for i in range(len(ids)):
                marker_id = int(ids[i])
                role_text = MARKER_ROLES.get(marker_id, f"ID {marker_id} - Tidak Dikenal")
                
                print(f"[LOG] Marker Terdeteksi: {role_text}")
                
                c = corners[i][0]
                top_left = (int(c[0][0]), int(c[0][1]))
                
                cv2.putText(
                    frame, 
                    role_text, 
                    (top_left[0], top_left[1] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, 
                    (0, 255, 0), 
                    2
                )

        cv2.imshow("HEROES GMRT ABU Robocon 2027 - ArUco Detector", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
