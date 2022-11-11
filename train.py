import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, DataCollatorWithPadding, Trainer
import argparse
from datasets import load_dataset
import evaluate
import wandb
import time

SEED = 42

f1_metric = evaluate.load('f1')
acc_metric = evaluate.load('accuracy')


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    f1_res = f1_metric.compute(predictions=predictions, references=labels)
    acc_res = acc_metric.compute(predictions=predictions, references=labels)
    wandb.log({"f1": f1_res["f1"], "accuracy": acc_res["accuracy"]})

    return {"f1": f1_res["f1"], "accuracy": acc_res["accuracy"]}


def main(args: dict):
    tokenizer = AutoTokenizer.from_pretrained(args['model'])
    model = AutoModelForSequenceClassification.from_pretrained(args['model'], num_labels=2)

    dataset = load_dataset('json', data_files=args['dataset_path'])['train']
    dataset = dataset.map(
        lambda examples: tokenizer(examples['text'], max_length=512, truncation=True),
        batched=True
    )
    datasets = dataset.train_test_split(test_size=args['test_split_size'], seed=SEED, shuffle=True)

    training_arguments = TrainingArguments(
        f'{args["model"]}_{args["lr"]}',
        evaluation_strategy='epoch',
        learning_rate=args['lr'],
        per_device_train_batch_size=args['batch_size'],
        per_device_eval_batch_size=args['batch_size'],
        num_train_epochs=args['epochs'],
        weight_decay=1e-5,
        save_strategy='epoch',
        group_by_length=True,
    )

    data_collator = DataCollatorWithPadding(tokenizer, padding=True, pad_to_multiple_of=8)

    trainer = Trainer(
        model,
        training_arguments,
        train_dataset=datasets['train'],
        eval_dataset=datasets['test'],
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    trainer.train()
    trainer.evaluate()

    trainer.save_model(h)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, type=str)
    parser.add_argument('--dataset_path', required=True, type=str)
    parser.add_argument('--lr', required=True, type=float)
    parser.add_argument('--epochs', required=True, type=int)
    parser.add_argument('--test_split_size', required=False, type=float, default=0.25)
    parser.add_argument('--batch_size', required=False, type=int, default=4)
    args = vars(parser.parse_args())

    h = str(time.time_ns())
    wandb.init(project='ads', entity='aitakaitov', tags=[h], config=args)

    main(args)
