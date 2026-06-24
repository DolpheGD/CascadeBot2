from bot.config import HF_TOKEN
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch 

#load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "KoalaAI/Text-Moderation",
    token=HF_TOKEN
)

model = AutoModelForSequenceClassification.from_pretrained(
    "KoalaAI/Text-Moderation",
    token=HF_TOKEN
)


def classify_message(text):
    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad(): # no training, just inference
        outputs = model(**inputs)

    probabilities = outputs.logits.softmax(dim=-1).squeeze()

    id2label = model.config.id2label

    results = {id2label[idx]: prob.item() for idx, prob in enumerate(probabilities)}

    return dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    