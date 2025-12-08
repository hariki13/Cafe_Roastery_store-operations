"""
Train the coffee roast classification model
Run: python scripts/train_model. py
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

class SimpleCoffeeTrainer:
    def __init__(self, data_dir='data/processed', 
                 model_name='google/vit-base-patch16-224',
                 output_dir='models/coffee-roast-v1'):
        
        self.data_dir = Path(data_dir)
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load label mapping
        with open(self.data_dir / 'label_mapping.json') as f:
            label_info = json.load(f)
        
        self.num_labels = label_info['num_labels']
        self.id2label = {int(k): v for k, v in label_info['id2label'].items()}
        self.label2id = label_info['label2id']
        
        print("="*60)
        print("COFFEE ROAST MODEL TRAINING")
        print("="*60)
        print(f"Model: {model_name}")
        print(f"Classes: {list(self.id2label.values())}")
        print(f"Output: {output_dir}")
        print("="*60)
    
    def load_data(self):
        """Load train and validation data"""
        print("\n📂 Loading datasets...")
        
        def load_split(split_name):
            split_dir = self.data_dir / split_name
            with open(split_dir / 'metadata.json') as f:
                metadata = json.load(f)
            
            return Dataset.from_dict({
                'image': [str(split_dir / item['file_name']) for item in metadata],
                'label': [item['label'] for item in metadata]
            })
        
        self.dataset = DatasetDict({
            'train': load_split('train'),
            'validation': load_split('val'),
            'test': load_split('test')
        })
        
        print(f"✅ Train: {len(self.dataset['train'])} images")
        print(f"✅ Val:   {len(self.dataset['validation'])} images")
        print(f"✅ Test:  {len(self.dataset['test'])} images")
    
    def setup_model(self):
        """Load model and processor"""
        print(f"\n🤖 Loading model: {self. model_name}")
        
        self.processor = AutoImageProcessor.from_pretrained(self.model_name)
        self.model = AutoModelForImageClassification.from_pretrained(
            self.model_name,
            num_labels=self.num_labels,
            id2label=self.id2label,
            label2id=self.label2id,
            ignore_mismatched_sizes=True
        )
        
        print("✅ Model loaded")
    
    def preprocess_data(self):
        """Preprocess images"""
        print("\n🖼️  Preprocessing images...")
        
        def transform(batch):
            images = [Image.open(path).convert('RGB') for path in batch['image']]
            inputs = self.processor(images, return_tensors='pt')
            inputs['labels'] = batch['label']
            return inputs
        
        self.dataset = self.dataset.map(transform, batched=True, batch_size=32)
        print("✅ Preprocessing complete")
    
    def compute_metrics(self, eval_pred):
        """Calculate accuracy"""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        accuracy = accuracy_score(labels, predictions)
        return {'accuracy': accuracy}
    
    def train(self, num_epochs=10, batch_size=16):
        """Train the model"""
        print("\n🏋️  Starting training...")
        print(f"Epochs: {num_epochs}")
        print(f"Batch size: {batch_size}")
        print("\n⏱️  This may take 15-30 minutes...")
        
        training_args = TrainingArguments(
            output_dir=str(self.output_dir / 'checkpoints'),
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            logging_steps=10,
            remove_unused_columns=False,
            push_to_hub=False,
            report_to="none"
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.dataset['train'],
            eval_dataset=self.dataset['validation'],
            compute_metrics=self.compute_metrics
        )
        
        # Train
        train_result = trainer.train()
        
        # Save model
        final_model_dir = self.output_dir / 'final_model'
        trainer.save_model(str(final_model_dir))
        self.processor.save_pretrained(str(final_model_dir))
        
        print("\n" + "="*60)
        print("✅ TRAINING COMPLETE!")
        print("="*60)
        print(f"Model saved to: {final_model_dir}")
        print("\nNext step: python scripts/test_model.py")
        
        return trainer
    
    def run(self, num_epochs=10, batch_size=16):
        """Run complete training pipeline"""
        self.load_data()
        self.setup_model()
        self.preprocess_data()
        trainer = self.train(num_epochs, batch_size)
        return trainer

if __name__ == "__main__":
    # Check if GPU is available
    if torch.cuda.is_available():
        print(f"🚀 GPU detected: {torch.cuda.get_device_name(0)}")
    else:
        print("💻 Using CPU (training will be slower)")
    
    trainer = SimpleCoffeeTrainer()
    trainer.run(num_epochs=10, batch_size=16)
    