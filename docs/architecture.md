# System Architecture

This document outlines the machine learning pipeline and system architecture of the AquaScan platform.

## Pipeline Flow

The image ingestion and detection pipeline runs through five specific stages:

1. **Preprocessing**: Validates the input resolution (minimum 200x200px) and converts color profiles to standard RGB. It then applies Contrast Limited Adaptive Histogram Equalization (CLAHE) to boost underwater visibility, followed by fast non-local means denoising (`fastNlMeansDenoisingColored`). Optionally, unsharp masking and glare inpainting filters are applied.
2. **Object Detection (YOLOv8)**: The fine-tuned YOLOv8 model localizes and identifies individual microplastic particles in the water sample. It predicts bounding boxes and assigns them to one of four classes: `fragment`, `fiber`, `pellet`, or `film`.
3. **Density Estimation (CSRNet)**: Uses a dilated CNN backbone based on a VGG-16 front-end to output high-resolution density maps. Summing the density map yields a verification count, which is mapped to equivalent particles per liter.
4. **Severity Classification (XGBoost)**: Takes a 6-feature vector consisting of total particle count, estimated density per liter, and individual class ratio splits, and classifies the pollution level as `low`, `medium`, `high`, or `critical`.
5. **Data Log & Reports**: The results are saved locally to an SQLite database (or uploaded to Supabase) and compiled into a 4-page PDF report.

## Database Integration

The data layer uses a unified Repository pattern that checks for environment configuration at startup. If `SUPABASE_URL` is set, it activates the cloud-synced Supabase client. Otherwise, it defaults to a local SQLite database file at `data/aquascan.db`.
