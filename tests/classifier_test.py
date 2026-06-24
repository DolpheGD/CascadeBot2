from bot.ml.classifier import classify_message


if __name__ == "__main__":
    test_text = "test"
    while test_text:
        test_text = input("Enter a message to classify: ")
        classification = classify_message(test_text)
        print(classification)