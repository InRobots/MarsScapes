# MarsScapes
We release MarsScapes, the first panoramic image dataset for unstructured terrain understanding on Mars. The dataset provides fine-grained annotations of eight terrain categories to encompass all pixels without omission. It contains 195 panoramas of Martian surface for semantic and instance segmentation, facilitating high-level semantic understanding of Martian landforms and further enhancing the navigability of rovers over rough terrains in large areas.

## Definitions of various terrains on Mars
To characterize all landforms on Mars and label all pixels without omission, we define eight categories. The following figure illustrates a sample of each category, including big rock (marked with a yellow polygon), bedrock (green), sand (pink), soil (in the whole (d)), gravel (red), steep slope (azure), sky (grey), and unknown classes (brown). We give specific descriptions and more examples of each category in the [supplementary.pdf](https://github.com/InRobots/MarsScapes/files/7965342/supplementary.pdf).

![definition](https://user-images.githubusercontent.com/33188908/151687950-12db66f5-ef5f-4c62-8298-bdaf850d1b27.png)
<img src="https://user-images.githubusercontent.com/33188908/151687950-12db66f5-ef5f-4c62-8298-bdaf850d1b27.png" width="600px">

## Data collection and annotation
The raw mars images are courtesy of NASA/JPL-Caltech. You can read the full use policy [here](https://www.jpl.nasa.gov/jpl-image-use-policy). We picked out 3379 images that met our criteria and employed PtGui software to splice them into 195 panoramas.

we adopt [PixelAnnotationTool](https://github.com/abreheret/PixelAnnotationTool), a pseudo manual annotation tool that uses watershed algorithm in OpenCV, which reduces part of our workload by automatically separating two adjacent terrains with high contrast. To store the annotation data in a desirable JSON format, we rewrite the [create_poly_json.py](https://github.com/InRobots/MarsScapes/blob/main/create_poly_json.py) file of the software.

## Dataset structure
The data file structure of MarsScapes is shown in the following figure.

<img src="https://user-images.githubusercontent.com/33188908/151687981-648783f0-fe0d-4f9a-aca0-c0f922d97c61.png" width="250px">

The _image_ folder contains 195 panoramic RGB images, whose widths range from 1230 to 12062 pixels and heights from 472 to 1649 pixels. Each image is stored with the naming convention _<Sol_num>.png_, where _Sol_ denotes the number of days Curiosity has traveled on Mars and _num_ represents the number of panoramas.

In the _semantic_ folder, _<Sol_num>_color.png_ is the visualization of semantic annotations for 8 categories and it is converted into a single-channel _<Sol_num>_semanticId.png_ for semantic segmentation research. Different from the semantic annotation of each terrain type, individual instances of the same terrain are labeled in _<Sol_num>_instanceId.png_, which can be used in instance segmentation research. In addition, _<Sol_num>_polygon.json_ provides a human-readable text format for annotations. Here we show panorama images, semantic segmentation annotations and instance segmentation annotations of three samples in MarsScapes.

Sample 137_1
![137_1](https://user-images.githubusercontent.com/33188908/151661264-eaf2bf85-1568-4f12-8543-20ee5f5198a6.png)
![137_1_color](https://user-images.githubusercontent.com/33188908/151661273-dda936f1-2877-4cd0-bb7b-d9300c861763.png)
![137_1_instanceId](https://user-images.githubusercontent.com/33188908/151661278-434f5e3e-4c85-4b29-8288-b4338a9a6236.png)

Sample 439_2
![439_2](https://user-images.githubusercontent.com/33188908/151661318-ee7ee532-4912-4f43-a872-e1968f5b54c7.png)
![439_2_color](https://user-images.githubusercontent.com/33188908/151661329-19526811-de25-4ee8-b1d9-0d46e1b9109b.png)
![439_2_instanceId](https://user-images.githubusercontent.com/33188908/151661333-14c93e3c-4767-493b-86c6-d829ce99a3ab.png)

Sample 551_1
![551_1](https://user-images.githubusercontent.com/33188908/151661347-22942ef3-a62e-4762-a6af-0e1a94fc62d7.png)
![551_1_color](https://user-images.githubusercontent.com/33188908/151661355-3965cc5a-1364-489e-8944-1e82d4e88131.png)
![551_1_instanceId](https://user-images.githubusercontent.com/33188908/151661362-ede80fff-1b52-4b29-bd10-6d9746cd43eb.png)

The _processed_ folder contains pre-processed images for training learning-based methods. Referring to [SkyScapes](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/viewer.html?pdfurl=https%3A%2F%2Fopenaccess.thecvf.com%2Fcontent_ICCV_2019%2Fpapers%2FAzimi_SkyScapes__Fine-Grained_Semantic_Understanding_of_Aerial_Scenes_ICCV_2019_paper.pdf&clen=9005566&chunk=true) dataset, we crop panoramas and corresponding annotation images into 512 × 512 sub-images with 50\% overlap between adjacent patches in both the horizontal and vertical directions. After flipping horizontally, we obtain 10404 samples and divide them into a group of 6243 for training, 2081 for validation and 2080 for testing.


## 
To evaluate the data volume of our MarsScapes dataset, we compare it with SkyScapes [1], a panoramic image dataset of urban infrastructure, shown in the following table.

|**Dataset** | **Classes** | **Panoramic images** | **Sub-images for training** | **Image size** | **Annotated pixels** |
|:-:|:-:|:-:|:-:|:-:|:-:|
| SkyScapes | 31 | 16 | 8820 | 5616×3744 | 3.36×10<sup>8</sup> |
| MarsScapes | 18 | 195 | 10404 | Widths:1230∼12062 Heights: 472∼1649 | 3.92×10<sup>8</sup> |




