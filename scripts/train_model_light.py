"""
Lightweight CPU-Optimized Coffee Roast Model Trainer
Faster training for testing and validation before GPU training
"""

import torch
from transformers import (
    AutoImageProcessor,
    AutoModelForImageClassification,
    TrainingArguments,
    Trainer
)
from datasets import load_dataset, Dataset, DatasetDict
from PIL import Image
import json
from pathlib import Path
import numpy as np
from sklearn.metrics import accuracy_score

class LightweightCoffeeTrainer:
    def __init__(self, data_dir='data/processed', 
                 model_name='google/vit-base-patch16-224',
                 output_dir='models/coffee-roast-v1-light',
                 epochs=3,
                 batch_size=8,
                 img_size=128):  # Reduced from 224
        
        self.data_dir = Path(data_dir)
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.epochs = epochs
        self.batch_size = batch_size
        self.img_size = img_size
        
        # Load label mapping
        with open(self.data_dir / 'label_mapping.json') as f:
            label_info = json.load(f)
        
        self.num_labels = label_info['num_labels']
        self.id2label = {int(k): v for k, v in label_info['id2label'].items()}
        self.label2id = label_info['label2id']
        
        print("="*60)
        print("🚀 LIGHTWEIGHT CPU MODEL TRAINING")
        print("="*60)
        print(f"Model: {model_name}")
        print(f"Classes: {list(self.id2label.values())}")
        print(f"Epochs: {epochs} (reduced for CPU)")
        print(f"Batch size: {batch_size}")
        print(f"Image size: 224x224 (ViT standard)")
        print(f"Output: {output_dir}")
        print("="*60)
    
    def load_data(self, max_samples=None):
        """Load train and validation data with optional sample limit"""
        print("\n📂 Loading datasets...")
        
        def load_split(split_name, limit=None):
            split_dir = self.data_dir / split_name
            metadata_file = split_dir / 'metadata.json'
            
            if not metadata_file.exists():
                return None
                
            with open(metadata_file) as f:
                metadata = json.load(f)
            
            # Limit samples for faster training
            if limit:
                metadata = metadata[:limit]
            
            images = []
            labels = []
            
            for item in metadata:
                img_path = split_dir / item['file_name']
                if img_path.exists():
                    images.append(str(img_path))
                    labels.append(item['label'])
            
            return Dataset.from_dict({
                'image': images,
                'label': labels
            })
        
        # Load with limits for CPU training
        train_limit = max_samples if max_samples else 200  # Limit to 200 samples
        val_limit = max_samples // 2 if max_samples else 50
        
        self.dataset = DatasetDict({
            'train': load_split('train', train_limit),
            'validation': load_split('val', val_limit),
        })
        
        print(f"✅ Train: {len(self.dataset['train'])} images (limited for CPU)")
        print(f"✅ Val:   {len(self.dataset['validation'])} images")
        
        return self.dataset
    
    def load_model(self):
        """Load image processor and model"""
        print(f"\n🤖 Loading lightweight model: {self.model_name}")
        
        # Load image processor - keep original size for ViT model
        self.processor = AutoImageProcessor.from_pretrained(self.model_name)
        
        # Load model
        self.model = AutoModelForImageClassification.from_pretrained(
            self.model_name,
            num_labels=self.num_labels,
            id2label=self.id2label,
            label2id=self.label2id,
            ignore_mismatched_sizes=True
        )
        
        print("✅ Model loaded")
        
        # Use CPU
        self.device = torch.device('cpu')
        self.model.to(self.device)
        print("💻 Using CPU (optimized for quick testing)")
    
    def preprocess_data(self):
        """Preprocess images"""
        print("\n🖼️  Preprocessing images...")
        
        def transform(examples):
            # Load and process images
            images = [Image.open(img_path).convert('RGB') 
                     for img_path in examples['image']]
            
            inputs = self.processor(images, return_tensors='pt')
            inputs['label'] = examples['label']
            return inputs
        
        self.dataset = self.dataset.map(
            transform,
            batched=True,
            remove_columns=['image'],
            batch_size=self.batch_size
        )
        
        print("✅ Preprocessing complete")
    
    def compute_metrics(self, eval_pred):
        """Compute accuracy"""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return {'accuracy': accuracy_score(labels, predictions)}
    
    def train(self):
        """Train the model"""
        print("\n🏋️  Starting lightweight training...")
        print(f"Epochs: {self.epochs}")
        print(f"Batch size: {self.batch_size}")
        print(f"\n⏱️  Estimated time: 5-10 minutes on CPU")
        
        # Lightweight training arguments
        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            num_train_epochs=self.epochs,
            per_device_train_batch_size=self.batch_size,
            per_device_eval_batch_size=self.batch_size,
            eval_strategy="epoch",  # Updated parameter name
            save_strategy="epoch",
            learning_rate=5e-5,
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            logging_dir=str(self.output_dir / 'logs'),
            logging_steps=10,
            save_total_limit=2,  # Keep only 2 checkpoints
            remove_unused_columns=False,
            push_to_hub=False,
            report_to="none",  # Disable wandb/tensorboard
            dataloader_num_workers=0,  # Single thread for CPU
            fp16=False,  # No mixed precision on CPU
        )
        
        # Create trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.dataset['train'],
            eval_dataset=self.dataset['validation'],
            compute_metrics=self.compute_metrics,
        )
        
        # Train
        print("\n🔥 Training started...")
        train_result = trainer.train()
        
        # Evaluate
        print("\n📊 Evaluating...")
        metrics = trainer.evaluate()
        
        print("\n" + "="*60)
        print("✅ TRAINING COMPLETE!")
        print("="*60)
        print(f"Final Accuracy: {metrics['eval_accuracy']:.4f}")
        print(f"Training Loss: {train_result.training_loss:.4f}")
        print(f"Model saved to: {self.output_dir}")
        print("="*60)
        
        # Save final model
        trainer.save_model()
        self.processor.save_pretrained(self.output_dir)
        
        print("\n💡 Next steps:")
        print("   1. Review the results above")
        print("   2. If satisfied, use the full train_model.py with GPU")
        print("   3. This lightweight model can be used for quick testing")
        
        return metrics

def main():
    """Main training function"""
    
    print("\n" + "="*60)
    print("🚀 LIGHTWEIGHT MODEL TRAINING FOR CPU")
    print("="*60)
    print("This is a faster, simplified version for testing.")
    print("Use the full train_model.py with GPU for production.")
    print("="*60 + "\n")
    
    # Initialize trainer
    trainer = LightweightCoffeeTrainer(
        epochs=3,           # Reduced from 10
        batch_size=4,       # Further reduced for CPU
        img_size=224,       # Keep ViT standard size
    )
    
    # Load data (limited samples)
    trainer.load_data(max_samples=200)
    
    # Load model
    trainer.load_model()
    
    # Preprocess
    trainer.preprocess_data()
    
    # Train
    metrics = trainer.train()
    
    print("\n✅ All done! Check the results above.")

if __name__ == '__main__':
    main()
