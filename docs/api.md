# API and Module Reference

This document provides a summary of the core modules and function interfaces within the AquaScan system.

## Module Index

### 1. Preprocessing (`src/preprocessing/`)

- `image_processor.py`:
  - `validate_image(image: PIL.Image) -> tuple[bool, str]`: Checks image size (>= 200x200px), format (RGB/RGBA), and corruption status.
  - `preprocess(image: PIL.Image) -> PIL.Image`: Resizes to 640x640 with black padding, applies CLAHE, and runs OpenCV denoising.
- `glare_removal.py`:
  - `remove_glare(image: PIL.Image) -> PIL.Image`: Locates highlight areas (> 240 gray intensity) and applies Telea inpainting.
- `turbidity_filter.py`:
  - `correct_turbidity(image: PIL.Image) -> PIL.Image`: Performs Gray World white balancing and unsharp masking.

### 2. Inference Engine (`src/detector/`)

- `detector.py`:
  - `Detector(model_path: str = None)`: Detector class. Dynamically falls back to mock mode if weights are missing.
  - `detect(image: PIL.Image) -> DetectionResult`: Main detection inference method.
  - `DetectionResult`: Dataclass containing `particle_count`, `class_counts`, `density_per_liter`, `severity`, `confidence`, `annotated_image`, `bboxes`, and `is_mock`.

### 3. Density Estimator (`src/density/`)

- `density_estimator.py`:
  - `DensityEstimator(weights_path: str = None)`: Loads CSRNet weights.
  - `estimate_density(image: PIL.Image) -> tuple[np.ndarray, float]`: Estimates density map and particles per liter.

### 4. Database Layer (`src/database/`)

- `repository.py`:
  - `Repository()`: Interface class. Auto-routes between `SQLiteClient` and `SupabaseClient`.
  - `save_submission(data: dict) -> str`: Logs the detection run.
  - `get_all_submissions() -> list[dict]`: Retrieves all submissions.
  - `get_submissions_with_gps() -> list[dict]`: Retrieves submissions containing valid GPS.
  - `get_statistics() -> dict`: Summarizes system statistics.
  - `delete_submission(submission_id: str) -> bool`: Deletes a submission by ID.
