import os
import json
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split

def generate_synthetic_data(num_samples: int = 2000) -> tuple[np.ndarray, np.ndarray]:
    """Generates synthetic dataset for training the severity classifier.
    
    Generates features: [count, density, frag_ratio, fiber_ratio, pellet_ratio, film_ratio]
    and maps them to labels [0: low, 1: medium, 2: high, 3: critical] using heuristic rules.
    """
    print(f"[Train] Generating {num_samples} synthetic training samples...")
    X = []
    y = []
    
    for _ in range(num_samples):
        # Sample count and density
        count = np.random.randint(0, 200)
        density = count * 12.5 + np.random.uniform(-10.0, 10.0)
        density = max(0.0, density)
        
        # Class distribution ratios
        ratios = np.random.dirichlet(np.ones(4))
        
        features = [
            float(count),
            float(density),
            ratios[0], # fragment
            ratios[1], # fiber
            ratios[2], # pellet
            ratios[3]  # film
        ]
        
        # Rule-based labelling matching the severity classifier heuristics
        if count < 10 and density < 10:
            label = 0 # low
        elif count < 10:
            if density < 50:
                label = 0
            elif density < 100:
                label = 1 # medium
            else:
                label = 2 # high
        elif 10 <= count <= 50:
            label = 1 # medium
        elif 51 <= count <= 100:
            label = 2 # high
        else:
            label = 3 # critical
            
        X.append(features)
        y.append(label)
        
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)

def train_and_save():
    """Trains the XGBoost classifier and saves it to models/weights/severity_xgb.json."""
    print("[Train] Commencing Severity Classifier Training Pipeline...")
    
    # 1. Generate data
    X, y = generate_synthetic_data(3000)
    
    # 2. Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"[Train] Split data: Train={len(X_train)} samples, Validation={len(X_val)} samples.")
    
    # 3. Initialize model
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        objective='multi:softprob',
        num_class=4,
        random_state=42
    )
    
    # 4. Train
    print("[Train] Fitting XGBoost model...")
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=False
    )
    
    # 5. Save model
    output_dir = "models/weights"
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, "severity_xgb.json")
    
    print(f"[Train] Saving trained XGBoost model to {model_path}...")
    model.save_model(model_path)
    
    # Validate accuracy
    train_acc = np.mean(model.predict(X_train) == y_train)
    val_acc = np.mean(model.predict(X_val) == y_val)
    print(f"[Train] Training complete. Train Accuracy: {train_acc:.4f}, Val Accuracy: {val_acc:.4f}")
    print("[Train] Pipeline completed successfully.")

if __name__ == "__main__":
    train_and_save()
