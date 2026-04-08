"""
Run this once to train and save the intent classifier:
    python train_model.py
"""
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.optim import AdamW
from intents import INTENTS
from train_data import TRAIN_DATA

MODEL_NAME = "indobenchmark/indobert-base-p1"
SAVE_PATH = "intent_model"
EPOCHS = 10
BATCH_SIZE = 8

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


class ChatDataset(Dataset):
    def __init__(self, data):
        self.texts = [x[0] for x in data]
        self.labels = [INTENTS.index(x[1]) for x in data]

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        enc = tokenizer(
            self.texts[idx],
            truncation=True,
            padding="max_length",
            max_length=32,
            return_tensors="pt",
        )
        return {
            "input_ids": enc["input_ids"].squeeze(),
            "attention_mask": enc["attention_mask"].squeeze(),
            "labels": torch.tensor(self.labels[idx]),
        }


def train():
    dataset = ChatDataset(TRAIN_DATA)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=len(INTENTS)
    )
    optimizer = AdamW(model.parameters(), lr=2e-5)

    model.train()
    for epoch in range(EPOCHS):
        total_loss = 0
        for batch in loader:
            optimizer.zero_grad()
            outputs = model(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
                labels=batch["labels"],
            )
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}/{EPOCHS} — Loss: {total_loss:.4f}")

    model.save_pretrained(SAVE_PATH)
    tokenizer.save_pretrained(SAVE_PATH)
    print(f"\nModel saved to ./{SAVE_PATH}/")


if __name__ == "__main__":
    train()
