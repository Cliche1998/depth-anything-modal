import modal
from pathlib import Path
app = modal.App("depth-anything-v2-inference")
import os
model_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
    'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
}

### ENCODER FLAG
encoder = 'vits' 

### GPU FLAG
gpu = 'L4'

### VIDEO NAME
video_name = "videos/cliff_jumping.mp4"


video_vol = modal.Volume.from_name("model-inputs", create_if_missing=True)
output_vol = modal.Volume.from_name("model-outputs", create_if_missing=True)
cache_vol = modal.Volume.from_name("model-cache", create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.10")
    .apt_install(
        "git","wget","ffmpeg")
    .run_commands([
        "git clone https://github.com/DepthAnything/Depth-Anything-V2 /depth",
        "python -m pip install -r /depth/requirements.txt",
        "python -m pip install matplotlib",
        "python -m pip install transformers",
        "python -m pip install Pillow",
        "python -m pip install ffmpeg-python==0.2.0",
        "python -m pip install xformers",
        "python -m pip install fastapi[standard]"
    ])
    
)


@app.cls(
    image=image.env({"HF_HUB_CACHE": '/cache'}),
    volumes={"/root/videos": video_vol, '/cache': cache_vol, "/root/output": output_vol},
    gpu=gpu,
    timeout=1000,
)

class Model():

    @modal.enter()
    def initialize_model(self):

        import sys
        import torch
        import os
        os.makedirs("/cache", exist_ok=True)
        model_path = f"/cache/depth_anything_v2_{encoder}.pth"
        if not os.path.exists(model_path):
            import urllib.request
            url = f"https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_{encoder}.pth?download=true"
            print(f"Downloading model from {url} to {model_path}")
            urllib.request.urlretrieve(url, model_path)
        sys.path.insert(0, "/depth")
        
        from depth_anything_v2.dpt import DepthAnythingV2
        DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'


        self.model = DepthAnythingV2(**model_configs[encoder])
        self.model.load_state_dict(torch.load(f'/cache/depth_anything_v2_{encoder}.pth', map_location='cpu'))
        self.model = self.model.to(DEVICE).eval()

    
    def generate_video_depth(self,video="/root/videos/input.mp4"):

        import numpy as np
        import cv2
        import matplotlib
        import os
        from fastapi import FastAPI
        from fastapi.responses import FileResponse

        cmap = matplotlib.colormaps.get_cmap('Spectral_r')

        output_path = '/root/output/output.mp4'

        video = Path(video)
        if not os.path.exists(video):
            raise FileNotFoundError(f"Input video file not found at {video}")
        
        raw_video = cv2.VideoCapture(video)
        frame_width, frame_height = int(raw_video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(raw_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = int(raw_video.get(cv2.CAP_PROP_FPS))
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, (frame_width, frame_height))
        print('going to read video')

        while raw_video.isOpened():

            ret, raw_frame = raw_video.read()
            if not ret:
                break 
            
            depth = self.model.infer_image(raw_frame)
            
            depth = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
            depth = depth.astype(np.uint8)
            
            
            depth = (cmap(depth)[:, :, :3] * 255)[:, :, ::-1].astype(np.uint8)

            out.write(depth)
        raw_video.release()
        out.release()

    
    @modal.fastapi_endpoint()
    async def trigger_inference(self):

        from fastapi import FastAPI
        from starlette.background import BackgroundTask
        from fastapi.responses import FileResponse
        output_path = '/root/output/output.mp4'
        self.generate_video_depth()

        if os.path.exists(output_path):
            response = FileResponse(
                "/root/output/output.mp4",
                media_type="video/mp4",
                filename="output.mp4",
                background=BackgroundTask(lambda: os.remove("/root/output/output.mp4"))
            )
            return response
        else:
            print(f"Failed to save output video at {output_path}")

    
    @modal.fastapi_endpoint()
    async def measure_inference_time(self):
        import time

        output_path = '/root/output/output.mp4'
        
        start_time = time.time()
        self.generate_video_depth()
        end_time = time.time()
        
        inference_time = end_time - start_time
        
        if os.path.exists(output_path):
            return {"status": "success", "inference_time": inference_time, "message": "Inference completed successfully."}
        else:
            return {"status": "error", "inference_time": inference_time, "message": "Inference failed or output not found."}


@app.local_entrypoint()    
    
def main():
    input_video=Path(__file__).parent / video_name
    
    with video_vol.batch_upload(force=True) as batch:
        batch.put_file(input_video, "input.mp4")
    print(f"added {video_name} to volume")
    return f"added {video_name} to volume"

    







