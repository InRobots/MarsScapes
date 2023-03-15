# MarsScapes
We release MarsScapes, the first panorama dataset for Martian terrain understanding. The dataset contains 195 panoramas of Mars surface with fine-grained annotations for semantic and instance segmentation, facilitating high-level scene understanding of Martian landforms and further enhancing the navigability of rovers over rough terrains in large areas. Note: Limited by the file size, we temporarily submit the first half of MarsScapes (i.e. from 122_1 to 527_1) as a representative subset. All samples will be provided after our paper is accepted.

## Definitions of various terrains on Mars
To characterize all landforms on Mars and label all pixels without omission, we define nine categories, including soil, sand, gravel, bedrock, rocks, tracks, shadows, background and unknown. We give specific descriptions and examples of each category in the [supplementary.pdf](https://github.com/InRobots/MarsScapes/files/7965342/supplementary.pdf).

## Data collection and annotation
The raw Mars images are courtesy of NASA/JPL-Caltech. You can read the full use policy [here](https://www.jpl.nasa.gov/jpl-image-use-policy). We pick out 3379 images that meet our criteria and employ PtGui software to splice them into 195 panoramas.

we adopt [PixelAnnotationTool](https://github.com/abreheret/PixelAnnotationTool), a manual annotation tool that uses watershed algorithm in OpenCV, which reduces part of our workload by automatically separating two adjacent terrains with high contrast. To store the annotation data in a desirable JSON format, we rewrite the [create_poly_json.py](https://github.com/InRobots/MarsScapes/blob/main/create_poly_json.py) file of the software.

## Dataset structure
The data file structure of MarsScapes and the JSON format of a sample are shown in the following figure.

<div align=center>
<img src="https://github.com/InRobots/MarsScapes/blob/main/IMG/structure.png" width="500px">
</div>

The _image_ folder contains 195 panoramic RGB images, whose widths range from 1230 to 12062 pixels and heights from 472 to 1649 pixels. Each image is stored with the naming convention _<Sol_num>.png_, where _Sol_ denotes the number of days Curiosity has traveled on Mars and _num_ represents the number of panoramas.

In the _semantic_ folder, _<Sol\_num>\_color.png_ is the visualization of semantic annotations for 9 categories and it is converted into a single-channel _<Sol\_num>\_semanticId.png_ for semantic segmentation research. Different from the semantic annotation of terrain classes, all instances of the same class are distinguished in _<Sol\_num>\_instanceId.png_, which can be used in instance segmentation research. In addition, _<Sol\_num>\_polygon.json_ provides a human-readable text format for annotations. Here we show panorama images, semantic segmentation annotations and instance segmentation annotations of three samples in MarsScapes.

Sample 137_1
![137_1](https://github.com/InRobots/MarsScapes/blob/main/IMG/137_1.png)
![137_1_color](https://github.com/InRobots/MarsScapes/blob/main/IMG/137_1_color.png)
![137_1_instanceId](https://github.com/InRobots/MarsScapes/blob/main/IMG/137_1_instanceId.png)

Sample 439_2
![439_2](https://github.com/InRobots/MarsScapes/blob/main/IMG/439_2.png)
![439_2_color](https://github.com/InRobots/MarsScapes/blob/main/IMG/439_2_color.png)
![439_2_instanceId](https://github.com/InRobots/MarsScapes/blob/main/IMG/439_2_instanceId.png)

Sample 747_1
![747_1](https://github.com/InRobots/MarsScapes/blob/main/IMG/747_1.png)
![747_1_color](https://github.com/InRobots/MarsScapes/blob/main/IMG/747_1_color.png)
![747_1_instanceId](https://github.com/InRobots/MarsScapes/blob/main/IMG/747_1_instanceId.png)

The _processed_ folder contains pre-processed images for evaluating supervised learning and UDA methods. The panorama samples of MarsScapes facilitate data augmentation to obtain a more diverse terrain distribution, which is crucial for promoting UDA performance. Referring to the [SkyScapes](https://openaccess.thecvf.com/content_ICCV_2019/html/Azimi_SkyScapes__Fine-Grained_Semantic_Understanding_of_Aerial_Scenes_ICCV_2019_paper.html) dataset, we crop panoramas and corresponding annotation images into 512 × 512 sub-images with 50\% overlap between adjacent patches in both the horizontal and vertical directions. After flipping horizontally, we obtain 13618 images for the source domain and 7184 for the target domain.

## Commentary on MarsScapes
To evaluate the data volume of our MarsScapes dataset, we compare it with [SkyScapes](https://openaccess.thecvf.com/content_ICCV_2019/html/Azimi_SkyScapes__Fine-Grained_Semantic_Understanding_of_Aerial_Scenes_ICCV_2019_paper.html), a panoramic image dataset of urban infrastructure, shown in the following table.

|**Dataset** | **Classes** | **Panoramic images** | **Sub-images for evaluating** | **Image size** | **Annotated pixels** |
|:-:|:-:|:-:|:-:|:-:|:-:|
| SkyScapes | 31 | 16 | 17640 | 5616×3744 | 3.36×10<sup>8</sup> |
| MarsScapes | 9 | 195 | 20802 | Widths:1230∼12062 Heights: 472∼1649 | 3.92×10<sup>8</sup> |

In terms of the number of annotated pixels, the two datasets have similar data volume. Processed by the same methods mentioned above, SkyScapes contains 17640 images and MarsScapes 20802 images for evaluating. Although the Martian terrain is not as diverse as the urban infrastructure of SkyScapes, the annotation of MarsScapes requires more labor for the following reasons:

1) SkyScapes is a dataset collected in structured environment, where the boundary of an instance can be described by regular line segments. Under unstructured environment like Mars surface, however, the boundary of a terrain is mostly irregular and blurred;

2) Most semantic segmentation datasets are collected on the Earth, where most objects can be distinguished by color and shape. On Mars, however, the colors of the various terrains are so similar that labeling is mainly based on inconspicuous texture, such that the annotations of MarsScapes requires manual efforts instead of the assistance of annotation software;

3) The classification of an unstructured terrain relies on its relationships with neighboring areas, which requires us to comply with more complex annotating standards.

In conclusion, MarsScapes provides enough samples with fine-grained annotations for training learning-based methods, thus contributing to autonomous navigation of rovers on Mars.
