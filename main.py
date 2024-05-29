import os
import os.path
import sqlite3
import pandas as pd
from typedstream.stream import TypedStreamReader


# The textual contents of some messages are encoded in a special attributedBody
# column on the message row; this attributedBody value is in Apple's proprietary
# typedstream format, but can be parsed with the pytypedstream package
# (<https://pypi.org/project/pytypedstream/>)
def decode_message_attributedbody(data):
    if not data:
        return None
    for event in TypedStreamReader.from_data(data):
        # The first bytes object is the one we want
        if type(event) is bytes:
            return event.decode("utf-8")


def main():
    db_path = os.path.expanduser("./chat.db")
    with sqlite3.connect(db_path) as connection:
        messages_df = pd.read_sql_query(
            sql="SELECT handle_id, text, is_from_me, attributedBody FROM message ORDER BY date DESC",
            con=connection,
            parse_dates={"datetime": "ISO8601"},
        )
        # Decode any attributedBody values and merge them into the 'text' column
        messages_df["text"] = messages_df["text"].fillna(
            messages_df["attributedBody"].apply(decode_message_attributedbody)
        )
        # Drop the attributedBody column
        messages_df.drop(columns=["attributedBody"], inplace=True)

        # Write the DataFrame to a CSV file
        csv_filename = "chats.csv"
        messages_df.to_csv(csv_filename, index=False)
        print(f"CSV file '{csv_filename}' has been created successfully.")


if __name__ == "__main__":
    main()
