# Face Recognition using TOPSIS Method

## Dokumentasi Bahasa Indonesia

[Dokumentasi Bahasa Indonesia](documentation/indonesia/README.md)

## TOPSIS Method

[TOPSIS Method, which stands for **Technique for Order of Preference by Similarity to Ideal Solution**, is a decision analysis technique used to select the best alternative from a set of options based on several relevant criteria]((https://dosenit.com/kuliah-it/metode-topsis)). [This method was developed by Hwang and Yoon in 1981 and is often used in the context of multi-criteria decision making](https://nictodev.com/mengenal-metode-topsis-adalah/).

The basic principle of the TOPSIS method is to compare each alternative with the positive ideal solution (best alternative) and the negative ideal solution (worst alternative) in the multi-criteria solution space. [The goal is to determine the alternative that is closest to the positive ideal solution and farthest from the negative ideal solution]((https://dosenit.com/kuliah-it/metode-topsis)).

The steps involved in the TOPSIS method include:
1. Identifying the criteria and alternatives to be evaluated.
2. Assigning weights to each criterion.
3. Constructing a normalized decision matrix.
4. Calculating the distance of each alternative from the positive and negative ideal solutions.
5. Calculating preference scores for each alternative.
6. Ranking alternatives based on preference scores from highest to lowest.

[This method is considered efficient in computation and provides an easily understandable way to measure the relative performance of decision alternatives](https://dosenit.com/kuliah-it/metode-topsis).

## ABOUT THE PROJECT

By utilizing [Flask](https://pypi.org/project/Flask/), [Python Face-recognition](https://pypi.org/project/face-recognition/), [Python Open-CV](https://pypi.org/project/opencv-python/), [Numpy](https://pypi.org/project/numpy/), and other modules, we have developed a web-based application for face recognition and measuring the similarity between images A, B, C, and D. The TOPSIS method will calculate several factors, including:

1. **Minimum Square Error (MSE).**

    The difference between each pixel in image A and the corresponding pixel in image B is calculated, squared, and summed. Then, the total sum is divided by the total number of pixels (width multiplied by height) to obtain the average, or "mean," of the squared errors, which is called Mean Squared Error.

    MSE is one of many metrics that can be used to measure how similar two images are.

2. **Average Standard Deviation.**

    Standard deviation is a measure of how spread out a group of numbers is from their average. In this context, standard deviation is a measure of how spread out the pixel intensities in an image are from the average pixel intensity.

    If the standard deviation between image A and another image is smaller, it means the pixel intensities in both images are spread close to their averages, indicating similar pixel intensity patterns. Therefore, we can say that the images are more "similar" to each other.

3. **Face Distance.**

    In the context of face recognition, "face distance" refers to the measurement of distance between two face encodings. This distance is typically calculated using a metric such as Euclidean distance, which measures the shortest distance between two points in a multi-dimensional space.

    In the Python face_recognition library, the face_distance function is used to calculate the Euclidean distance between known face encodings and unknown face encodings. This distance indicates how similar the faces are. Lower values indicate that the faces are more similar, while higher values indicate that they are less similar.

## PREVIEW

## RUNNING

```
python3 app.py
```

## CONNECTING TO FIREBASE REALTIME DATABASE

Actually, the connection to Firebase has been set up in this program, so you only need to adjust the settings in `system_config.json` in the `config/system_config.json` folder. To connect to Firebase Realtime Database, follow the steps below:

1. **Insert Firebase Private Key File into the Config Folder**.

    You can obtain the private key file directly in the `Settings -> Project Settings -> Service Account` section, then click the `Generate New Private Key` button. After the Private Key file is successfully downloaded, place the Firebase private key file into the config folder.

    Here is the structure:
    ```
    Folder: config
            ↳ system_config.json
            ↳ {{place the Firebase private key file here}}
    ```

2. **Setting system_config.json**.

Next, configure the settings in `system_config.json` in the config folder.

- Set "use_firebase_database" to `true`.
- Set "firebase_database_path" to `config/{{name of the Firebase private key file}}`.
- Set "firebase_db_uri" to your reference URL.

Example configuration below:
```JSON
{
    "use_firebase_database":true,
    "firebase_database_path":"config/spk-alif-firebase-adminsdk-kyjwn-a5042873f7.json",
    "firebase_db_uri":"https://myrealtimedatabase.asia-southeast1.firebasedatabase.app/",
    "firebase_delete_image_time":120
}
```

## FINAL WORDS

Well, that's it. This is for the Decision Support System course assignment, so it's just as it is, because the Thesis Advisor is chasing the deadline haha.

Thanks to:
    - Mr. Weri Sirait M.kom (Lecturer of the Decision Support System course)
    - Fajar Jero (Who accompanied me in working on the Thesis haha)

Best Regards.