---
license: other
license_name: bria-rmbg-2.0
license_link: https://creativecommons.org/licenses/by-nc/4.0/deed.en
pipeline_tag: image-segmentation
tags:
- remove background
- background
- background-removal
- Pytorch
- vision
- legal liability
- transformers
- transformers.js
extra_gated_description: >-
  Bria AI Model weights are open source for non commercial use only, per the
  provided [license](https://creativecommons.org/licenses/by-nc/4.0/deed.en).
extra_gated_heading: Fill in this form to immediatly access the model for non commercial use
extra_gated_fields:
  Name: text
  Email: text
  Company/Org name: text
  Company Website URL: text
  Discord user: text
  I agree to BRIA’s Privacy policy, Terms & conditions, and acknowledge Non commercial use to be Personal use / Academy / Non profit (direct or indirect): checkbox
---

# BRIA Background Removal v2.0 Model Card
<p align="center"><img src="https://platform.bria.ai/assets/Bria-logo-BdHFpNGW.svg" alt="BRIA Logo" width="200" /></p>

<!-- RMBG Card wrapper -->
<div class="rmbg-card" style="position: relative; border-radius: 12px; overflow: hidden;">

  <!-- FIBO Promo Banner (Top) -->
  <a
    href="https://huggingface.co/briaai/FIBO"
    target="_blank"
    rel="noopener"
    aria-label="Explore FIBO on Hugging Face"
    style="
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      background: linear-gradient(90deg, #fff6b7 0%, #fde047 100%);
      color: #1f2937;
      text-decoration: none;
      font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      font-weight: 600;
      font-size: 13px;
      padding: 10px 0;
      border-bottom: 1px solid rgba(0,0,0,0.08);
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      z-index: 10;
    ">
    <img
      src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg"
      alt="Hugging Face"
      width="18"
      height="18"
      style="display:block"
    />
    <span>✨ Discover <strong>FIBO</strong> on Hugging Face</span>
  </a>

  <!-- ... your RMBG content below ... -->
<p align="center">
         💜 <a href="https://go.bria.ai/46gzn20"><b>Bria AI</b></a>&nbsp&nbsp | &nbsp&nbsp🤗 <a href="https://huggingface.co/briaai/">Hugging Face</a> &nbsp&nbsp | &nbsp&nbsp 📑 <a href="https://blog.bria.ai/">Blog</a> &nbsp&nbsp 
<br>
🖥️ <a href="https://huggingface.co/spaces/briaai/BRIA-RMBG-2.0">Demo</a>&nbsp&nbsp| &nbsp&nbsp <a href="https://github.com/Bria-AI/RMBG-2.0">Github</a>&nbsp&nbsp
</p>

RMBG v2.0 is our new state-of-the-art background removal model significantly improves RMBG v1.4. The model is designed to effectively separate foreground from background in a range of
categories and image types. This model has been trained on a carefully selected dataset, which includes:
general stock images, e-commerce, gaming, and advertising content, making it suitable for commercial use cases powering enterprise content creation at scale. 
The accuracy, efficiency, and versatility currently rival leading source-available models. 
It is ideal where content safety, legally licensed datasets, and bias mitigation are paramount. 

**[→ Try the API Sandbox (no signup required)](https://catalog.bria.ai/image-editing/remove-background/sandbox)**

Developed by BRIA AI, RMBG v2.0 is available as a source-available model for non-commercial use.

### Get Access

Bria RMBG2.0 is availabe everywhere you build, either as source-code and weights, ComfyUI nodes or API endpoints.


-


#####
### Model Description

**For production / commercial deployment**, use the Bria API — same RMBG-2.0 quality, fully licensed, zero infrastructure:

| Use                   | Self-Hosted (HF Weights) | Bria API    |
| :-------------------- |:-------------------------| :---------- |
| Quality               | ✅ RMBG-2.0              | ✅ RMBG-2.0 |
| Commercial License    | ❌ Requires agreement    | ✅ Included |
| GPU Infrastructure    | ❌ You manage            | ✅ Managed  |
| Legally Licensed Data | ✅ Yes                   | ✅ Yes      |
| Setup Time            | Hours                    | Minutes     |

**[→ Try the API Sandbox](https://catalog.bria.ai/image-editing/remove-background/sandbox)** — test it live, no signup required.



## Model Details
- **Developed by:** [BRIA AI](https://bria.ai/)
- **Model type:** Background Removal 
- **License:** [Creative Commons Attribution–Non-Commercial (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/deed.en)
  - The model is released under a CC BY-NC 4.0 license for non-commercial use.
  - Commercial use is subject to a commercial agreement with BRIA. Available [here](https://share-eu1.hsforms.com/2sj9FVZTGSFmFRibDLhr_ZAf4e04)

 **API Endpoint**: [Sandbox](https://catalog.bria.ai/image-editing/remove-background/sandbox)
- **ComfyUI**: [Use it in workflows](https://github.com/Bria-AI/ComfyUI-BRIA-API)
- **GitHub**: [github.com/Bria-AI/RMBG-2.0](https://github.com/Bria-AI/RMBG-2.0)

 **Purchase:** To purchase a Self-Hosted (HF Weights) commercial license [Click Here](https://share-eu1.hsforms.com/2sj9FVZTGSFmFRibDLhr_ZAf4e04).

For more information, please visit our [website](https://catalog.bria.ai/image-editing/remove-background/sandbox).

Join our [Discord community](https://discord.gg/Nxe9YW9zHS) for more information, tutorials, tools, and to connect with other users!

[CLICK HERE FOR A DEMO](https://huggingface.co/spaces/briaai/BRIA-RMBG-2.0)

[fal.ai](https://fal.ai/models/fal-ai/bria/background/remove), [Replicate](https://replicate.com/bria/remove-background)

![examples](t4.png)

- **Model Description:** BRIA RMBG-2.0 is a dichotomous image segmentation model trained exclusively on a professional-grade dataset. The model output includes a single-channel 8-bit grayscale alpha matte, where each pixel value indicates the opacity level of the corresponding pixel in the original image. This non-binary output approach offers developers the flexibility to define custom thresholds for foreground-background separation, catering to varied use cases requirements and enhancing integration into complex pipelines.
- **BRIA:** Resources for more information: [BRIA AI](https://bria.ai/)



## Training data
Bria-RMBG model was trained with over 15,000 high-quality, high-resolution, manually labeled (pixel-wise accuracy), fully licensed images.
Our benchmark included balanced gender, balanced ethnicity, and people with different types of disabilities.
For clarity, we provide our data distribution according to different categories, demonstrating our model’s versatility.

### Distribution of images:

| Category | Distribution |
| -----------------------------------| -----------------------------------:|
| Objects only | 45.11% |
| People with objects/animals | 25.24% |
| People only | 17.35% |
| people/objects/animals with text | 8.52% |
| Text only | 2.52% |
| Animals only | 1.89% |

| Category | Distribution |
| -----------------------------------| -----------------------------------------:|
| Photorealistic | 87.70% |
| Non-Photorealistic | 12.30% |


| Category | Distribution |
| -----------------------------------| -----------------------------------:|
| Non Solid Background | 52.05% |
| Solid Background | 47.95% 


| Category | Distribution |
| -----------------------------------| -----------------------------------:|
| Single main foreground object | 51.42% |
| Multiple objects in the foreground | 48.58% |


## Qualitative Evaluation
Open source models comparison
![diagram](diagram1.png)
![examples](collage5.png)

### Architecture
RMBG-2.0 is developed on the [BiRefNet](https://github.com/ZhengPeng7/BiRefNet) architecture enhanced with our proprietary dataset and training scheme. This training data significantly improves the model’s accuracy and effectiveness for background-removal task.<br>
If you use this model in your research, please cite:

```
@article{BiRefNet,
  title={Bilateral Reference for High-Resolution Dichotomous Image Segmentation},
  author={Zheng, Peng and Gao, Dehong and Fan, Deng-Ping and Liu, Li and Laaksonen, Jorma and Ouyang, Wanli and Sebe, Nicu},
  journal={CAAI Artificial Intelligence Research},
  year={2024}
}
```

#### Requirements
```bash
torch
torchvision
pillow
kornia
transformers
```

### Usage

<!-- This section is for the model use without fine-tuning or plugging into a larger ecosystem/app. -->


```python
from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True).eval().to(device)

# Data settings
image_size = (1024, 1024)
transform_image = transforms.Compose([
    transforms.Resize(image_size),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

image = Image.open(input_image_path)
input_images = transform_image(image).unsqueeze(0).to(device)

# Prediction
with torch.no_grad():
    preds = model(input_images)[-1].sigmoid().cpu()
pred = preds[0].squeeze()
pred_pil = transforms.ToPILImage()(pred)
mask = pred_pil.resize(image.size)
image.putalpha(mask)

image.save("no_bg_image.png")
```


</div>
