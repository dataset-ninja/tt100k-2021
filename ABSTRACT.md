The authors have created a large traffic-sign benchmark from 100000 Tencent Street View panoramas, called **Tsinghua Tencent 100K 2021 Dataset**. It provides 100000 images containing 30000 traffic-sign instances. These images cover large variations in illuminance and weather conditions. Each traffic sign in the benchmark is annotated with a class label and bounding box.

Note, similar **Tsinghua Tencent 100K 2021 Dataset** datasets are also available on the [DatasetNinja.com](https://datasetninja.com/):

- [Tsinghua Tencent 100K 2016 Dataset](https://datasetninja.com/tt100k-2016)

## Motivation

Scene understanding is the ultimate goal of computer vision; detecting and classifying objects of various sizes in the scene is an important sub-task. Recently, deep learning methods have shown superior performance for many tasks such as image classification and speech recognition. Traffic signs may be divided into different categories according to function, and in each category they may be further divided into subclasses with similar generic shape and appearance but different details. This suggests traffic sign recognition should be carried out as a two-phase task: detection followed by classification. The detection step uses shared information to suggest bounding boxes that may contain traffic-signs in a specific category, while the classification step uses differences to determine which specific kind of sign is present (if any).  Current methods achieve perfect or near perfect results for detection and classification tasks, with 100% recall and precision for detection and 99.67% precision for classification. While it may appear that these are thus solved problems, unfortunately, this benchmark data is not representative of that encountered in real tasks. 

## Data collection

Presently, Tencent Street Views covers about 300 Chinese cities and the road networks linking them. The original panoramas were captured by 6 SLR cameras and then stitched together. Image processing techniques such as exposure adjustment were also used. Images were captured both from vehicles and shoulder-mounted equipment, at intervals of about 10 m. The nature of the images provides two benefits for our benchmark. Firstly,  the appearances of an instance of a traffic sign in the authors benchmark vary significantly. Secondly, an instance of a traffic sign in successive images helps the participants constructing the
benchmark to correctly determine its classes: partially occluded or blurred traffic signs can be recognized from their occurrences in previous or subsequent shots. To create the benchmark images, the top 25% and bottom 25% of each panorama image was cropped off (as unlikely to contain any signs), and the remainder sliced vertically into 4 sub-images. The authors chose 10 regions from 5 different cities in China (including both downtown regions and suburbs for each city)
and downloaded 100000 panoramas from the Tencent Data Center.

<img src="https://github.com/dataset-ninja/tt100k-2021/assets/120389559/f1768a87-42fe-4592-884f-d81fa074d39d" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">The authors benchmark contains 100000 high resolution images in which all traffic signs are annotated with class label, bounding boxes, and pixel masks. The images are cut from from Tencent Street Views which contain realistic views traffic signs in environments.</span>

## Data annotation

The images collected were next annotated by hand. Traffic signs in China follow international patterns, and can be classified into three categories: warnings (mostly yellow triangles with a black boundary and information), prohibitions (mostly white surrounded by a red circle and also possibly having a diagonal bar), and mandatory (mostly blue circles with white information). Other signs exist that resemble traffic-signs but are in fact not. Such signs are placed in an ‘other’ class of a particular category. During traffic-sign annotation, the authors recorded the bounding box, boundary vertices and class label for the sign. The most complicated cases concern occluded signs.

<img src="https://github.com/dataset-ninja/tt100k-2021/assets/120389559/241aa543-fbe5-4cb8-94f2-1140da44e46f" alt="image" width="500">

<span style="font-size: smaller; font-style: italic;">Signs like traffic signs, but with other meanings.</span>

The authors benchmark has 100000 cropped images after discarding some of the images only containing background. Of these, 10000 contain 30000 traffic signs in total. Although their source images cover much of China, an imbalance still exists between different classes of traffic sign. This is unavoidable: classes such as signs to warn the driver to be cautious on mountain roads appear rarely. The images have resolution 2048×2048 and cover large variations in illuminance and weather conditions.

