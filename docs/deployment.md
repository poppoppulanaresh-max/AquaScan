# Deployment & Public Sharing Guide

This guide details how to run the AquaScan application locally, build and run it inside a Docker container, host it on GitHub, and deploy it publicly for free using **Streamlit Community Cloud** or **Hugging Face Spaces**.

---

## 1. Local Deployment

To run the application locally on your laptop:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BlueGuard-AI/AquaScan.git
   cd AquaScan
   ```
2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**:
   ```bash
   streamlit run app/main.py
   ```

---

## 2. Docker Containerization

To run the application inside an isolated Docker container:

1. **Build the Docker Image**:
   ```bash
   docker build -t aquascan:v1 .
   ```
2. **Run the Container**:
   ```bash
   docker run -p 8501:8501 aquascan:v1
   ```
3. Access the container in your browser at `http://localhost:8501`.

---

## 3. Hosting on GitHub

To put your project on GitHub so anyone can read the code and you can link it to cloud hosting:

1. **Initialize Git**:
   If not already initialized, run this in the project root:
   ```bash
   git init
   ```
2. **Handle Large Model Weights**:
   The `models/weights/best.pt` file is ~6MB. Since it is small, it can be pushed directly. If your model gets larger than 100MB, you should use **Git LFS** or upload it to Google Drive / OneDrive and fetch it at app runtime. For the current 6MB weights:
   ```bash
   git add models/weights/best.pt models/weights/severity_xgb.json
   ```
3. **Commit Code**:
   ```bash
   git add .
   # Verify you don't commit large temp files or databases (SQLite is ignored via standard .gitignore, but make sure data/aquascan.db is excluded if you want a clean database on cloud)
   git commit -m "Initial commit of AquaScan platform"
   ```
4. **Create a GitHub Repo**:
   - Go to [github.com](https://github.com/) and create a new public repository (do not add README, .gitignore, or license).
   - Copy the repository URL (e.g., `https://github.com/yourusername/aquascan.git`).
5. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/yourusername/aquascan.git
   git branch -M main
   git push -u origin main
   ```

---

## 4. Deploying to Streamlit Community Cloud (Recommended)

Streamlit Community Cloud is completely free and automatically redeploys your app every time you push code updates to GitHub.

### Step-by-Step Instructions:

1. **Sign Up / Log In**:
   - Go to [share.streamlit.io](https://share.streamlit.io/).
   - Log in using your **GitHub account**.
2. **Deploy a New App**:
   - Click the **"New app"** button.
3. **Configure the App**:
   - **Repository**: Choose your newly created GitHub repository (`yourusername/aquascan`).
   - **Branch**: Set to `main` (or the branch you pushed your code to).
   - **Main file path**: Set to `app/app.py`.
   - **App URL** (Optional): Choose a custom URL suffix (e.g., `aquascan-guntur`).
4. **Deploy**:
   - Click **"Deploy!"**.
   - The platform will spin up a container, install dependencies from `requirements.txt`, and launch your app.
   - Once completed, you will receive a public, permanent URL like `https://aquascan-guntur.streamlit.app/`.

---

## 5. Deploying to Hugging Face Spaces (Alternative)

Hugging Face Spaces is another excellent free platform that runs your app using the pre-configured `Dockerfile`.

### Step-by-Step Instructions:

1. **Sign Up / Log In**:
   - Go to [huggingface.co](https://huggingface.co/) and log in.
2. **Create a New Space**:
   - Go to Spaces page -> Click **"Create new Space"**.
   - **Space Name**: Enter `aquascan`.
   - **SDK**: Select **Docker** (since we have a custom `Dockerfile` with OpenCV and system tools).
   - **Space Hardware**: Select the free **CPU basic** runtime.
   - **Visibility**: Set to **Public**.
3. **Push Code to Space**:
   - Hugging Face will create a Git repository for your Space.
   - Clone it, copy your project files into it, commit, and push.
   - *Alternative*: You can configure a GitHub Action (we provided one at `.github/workflows/deploy.yml`) to automatically push changes from GitHub to Hugging Face Spaces!
4. The Space will build the Docker container and display the application at `https://huggingface.co/spaces/yourusername/aquascan`.
