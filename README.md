# Installation:

to get the demo running, install modal and set up api key. 


Create a new conda environment

```bash
conda create -n modal python=3.10
conda activate modal
```

Install modal using pip 

```bash
pip install modal
```

Run the setup to add the api key 


```bash
modal setup
```


# Running the Demo:

To load a video, open the depht.py file and add the name of the video you want to upload. then run the following command. This loads the video in the storage of the modal app.

```python
modal run depth.py
```

To run the demo, run the following command:

```python
modal serve depth.py
```

Modal creates api endpoints for 
- trigger_inference
- measure_inference_time

copy the endpoint link and use wget to trigger the endpoints, for example.


```bash
wget -O test.mp4 https://cliche1998--depth-anything-v2-inference-model-trigge-718bc6-dev.modal.run
```

```bash
wget -O test.html https://cliche1998--depth-anything-v2-inference-model-measur-eeb0e2-dev.modal.run
```

# 1. Pick a Model

## Ml-Depth-Pro

Inference Time - 142.95 seconds
Model Size - 1.77 GB

## Depth-Anything-V2

Depth Anything VITs - 
Inference Time - 8.98 seconds
Model Size - 94.62 MB

Depth Anything VITb - 
Inference Time - 13.95 seconds
Model Size - 371.90 MB


Depth Anything VITl - 
Inference Time - 32.95 seconds
Model Size - 1.25 GB


**Depth Anything** is still the best model to use as the inference time is much faster and it has a smaller model footprint. 

# 2. Host the model inference on Modal

## Side-by-Side Video Comparison


<div style="display: flex; justify-content: space-around;">
    <div>
        <h4>Original Video</h4>
        <video controls width="400">
            <source src="videos/cliff_jumping.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    <div>
        <h4>Depth Map Video</h4>
        <video controls width="400">
            <source src="cliff_jumping_depth.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
</div>

The output video might need be played on VLC or a dedicated media player

# 3. Inference Time on different GPUs

To choose the GPU, change the GPU_FLAG in depth.py. Here are the results of the inference time on the cliff_jumping.mp4 video

T4 - 34.47 seconds

L4 - 29.68 seconds

A10G - 19.16 seconds

A100 -18.44 seconds

L40S - 14.89 seconds

H100 - 14.47 seconds

# 4. Evaluation & Documentation

The Depth-Anything V2 paper proposes an evaluation benchmark for this task: DA-2K. It contains 1,000 diverse high resolution images and 2,000 precise pair-wise relative depth annotations. It covers a variety of scenes like Indoor, Outdoor, Transparent, Aerial, Near/Far etc. This presents a better evaluation metric as it is relatively noise free, covers different types of instances and has high resolution images. The relative depth map was created by using different depth estimation models to vote on the relative depth between pixels, and in cases where it was challenging to identify, htey were manually annotated. This would work if we use relative depth estimation. If absolute depth estimation is done, then it can be comapred against RGBD data or lidar data fused with RGB. 

