import pandas as pd


csv_path = "./audio/dialogue.csv"
df = pd.read_csv(csv_path, index_col=0)


def get_dialogue(status):
    print(df['dialogue'][status])
    return df['dialogue'][status]

def get_filename(status):
    print(df['filename'][status])
    return df['filename'][status]

def main():
    get_dialogue("smile again")
    get_filename("smile again")


if __name__ == '__main__':
    main()
        