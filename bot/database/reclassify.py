from sqlalchemy.orm import Session
from bot.database.session import SessionLocal
from bot.database.models.user_model import UserProfile, DangerMessage
from bot.ml.classifier import classify_danger_level


def reclassify_all():
    db: Session = SessionLocal()

    try:
        print("Starting reclassification...")

        # Get all stored dangerous messages
        messages = db.query(DangerMessage).all()

        for msg in messages:
            try:
                # Reclassify the message content
                result = classify_danger_level(msg.content)

                # Update stored scores
                msg.hate_score = result["Hate"]
                msg.sexual_score = result["Sexual"]
                msg.concern_score = result["Concern"]
                msg.danger_score = result["Danger"]

                print(
                    f"Reclassified message {msg.message_id} "
                    f"(Danger: {msg.danger_score:.2f})"
                )

            except Exception as e:
                print(
                    f"Failed to classify message {msg.message_id}: {e}"
                )

        db.commit()

        print("Finished message reclassification.")
        print("Recalculating user danger scores...")

        # Recalculate all user danger scores
        users = db.query(UserProfile).all()

        for user in users:
            top_messages = sorted(
                user.messages,
                key=lambda x: x.danger_score,
                reverse=True
            )[:10]

            if top_messages:
                user.danger_score = (
                    sum(msg.danger_score for msg in top_messages)
                    / len(top_messages)
                )
            else:
                user.danger_score = 0.0

            print(
                f"Updated user {user.discord_id} "
                f"(Danger: {user.danger_score:.2f})"
            )

        db.commit()

        print("Reclassification complete.")

    finally:
        db.close()


if __name__ == "__main__":
    reclassify_all()