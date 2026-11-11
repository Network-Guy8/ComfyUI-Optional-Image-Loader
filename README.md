# ComfyUI Optional Image Loader (Auto Resize)

A lightweight ComfyUI custom node that optionally loads an image and automatically downsizes oversized references by megapixel count. No placeholder image is generated when **None** is selected.

## Features

- **None** option returns Python `None` rather than a dummy image.
- Automatically downsizes images above a configurable megapixel limit (default **4 MP**).
- Maintains the source aspect ratio using Lanczos resampling.
- Never enlarges images and never modifies the source file.
- Compatible with existing workflows using the internal node type `OptionalLoadLastFrame` and output name `last_frame`.
- Supports PNG, JPEG, WebP, BMP and TIFF in the dropdown (subject to Pillow support).

## Installation

1. Place this repository folder in `ComfyUI/custom_nodes/`.
2. Restart ComfyUI and refresh the browser.
3. Search for **Optional Image Loader (Auto Resize)** in the node menu.

If you previously installed `ComfyUI-Optional-Load-Last-Frame`, **replace or disable the old installation** before installing this repository. Running both copies creates a duplicate node identifier and may lead to unpredictable loading behavior. Back up the old `__init__.py` first.

ComfyUI normally provides the Python dependencies (`torch`, `numpy`, `Pillow`, `folder_paths`). No separate pip install is expected in a standard ComfyUI environment.

## Settings

| Input | Default | Meaning |
| --- | --- | --- |
| `image` | `None` | Image to load, or no image |
| `auto_resize` | `true` | Enable downscaling of oversized images |
| `max_megapixels` | `4.0` | Maximum image area in millions of pixels (0.1–20 MP) |

**Output:** `last_frame` (`IMAGE` socket). If `image` is `None`, the runtime value is Python `None`.

Example: a 3417 × 5197 (~17.8 MP) reference becomes approximately 1621 × 2466 (~4 MP), with its aspect ratio retained.

## Important compatibility note

ComfyUI still considers the output socket connected when `None` is selected. **Downstream nodes must explicitly support Python `None` values**; many ordinary image-processing nodes do not. This node does not dynamically disconnect links or guarantee compatibility with all image inputs. Use a suitable optional-input filter or batching node where needed.

The preview may show the original image dimensions even when the runtime image is resized. Check the ComfyUI console for a resize message.

## Existing workflows

The internal node identifier remains `OptionalLoadLastFrame`, and the output is still named `last_frame`, to minimize changes to saved workflows. The additional controls have defaults. The display name is now **Optional Image Loader (Auto Resize)**.

## License

MIT — see [LICENSE](LICENSE).
