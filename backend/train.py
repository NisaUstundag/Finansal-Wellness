import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import torch

# --- 1. Veri Setini Yükleme ve Hazırlama ---
print("Veri seti yükleniyor...")
df = pd.read_csv('dataset.csv', header=None, names=['text', 'label'])

unique_labels = df['label'].unique().tolist()
label2id = {label: i for i, label in enumerate(unique_labels)}
id2label = {i: label for i, label in enumerate(unique_labels)}

df['label'] = df['label'].map(label2id)

hg_dataset = Dataset.from_pandas(df)
print("Veri seti hazırlandı.")

# --- 2. Model ve Tokenizer'ı Yükleme ---
model_name = "savasy/bert-base-turkish-sentiment-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Temel modeli, bizim etiket sayımıza göre yeni bir son katmanla yüklüyoruz
model = AutoModelForSequenceClassification.from_pretrained(
    model_name, 
    num_labels=len(unique_labels),
    ignore_mismatched_sizes=True # --- SORUNU ÇÖZEN SATIR BU ---
)
# Modelin yapılandırmasına etiket-ID eşleşmelerini ekliyoruz
model.config.id2label = id2label
model.config.label2id = label2id

# Metinleri modelin anlayacağı sayılara (token'lara) çeviren bir fonksiyon
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

# Tüm veri setine bu tokenizasyon işlemini uygulayalım
tokenized_dataset = hg_dataset.map(tokenize_function, batched=True)
print("Model ve tokenizer yüklendi ve veri tokenize edildi.")

# --- 3. Eğitim Ayarlarını Belirleme ---
training_args = TrainingArguments(
    output_dir="./finansal_model",
    evaluation_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# --- 4. Eğitimi Başlatma ---
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
)

print("Eğitim başlıyor... Bu işlem birkaç dakika sürebilir.")
trainer.train()
print("Eğitim tamamlandı! Yeni 'uzman' modelin './finansal_model' klasörüne kaydedildi.")