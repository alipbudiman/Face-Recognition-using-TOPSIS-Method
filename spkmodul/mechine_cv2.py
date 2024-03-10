import cv2
from sklearn.metrics import mean_squared_error

class OpenCV2:
    def __init__(self) -> None:
        pass

    def calculate_similarity(self, image1, image2):
        # Ubah gambar ke grayscale
        image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # Ubah gambar ke ukuran yang sama
        image1_gray = cv2.resize(image1_gray, (500, 500))
        image2_gray = cv2.resize(image2_gray, (500, 500))

        # Hitung Mean Squared Error antara dua gambar
        mse = mean_squared_error(image1_gray, image2_gray)

        # Hitung nilai rata-rata dan standar deviasi dari dua gambar
        mean1, std1 = cv2.meanStdDev(image1_gray)
        mean2, std2 = cv2.meanStdDev(image2_gray)

        return mse, mean1, std1, mean2, std2
