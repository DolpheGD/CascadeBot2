from bot.ml.classifier import classify_danger_level


if __name__ == "__main__":
    test_text = "test"
    while test_text:
        test_text = input("Enter a message to classify: ")
        classification = classify_danger_level(test_text)
        print(classification)