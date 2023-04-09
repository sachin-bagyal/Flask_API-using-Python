import pandas as pd


def process_data():
    data = pd.read_csv('data.csv')
    data = data.reset_index()
    data.columns = ['id', 'native_english_speaker', 'course_instructor','course','semester','class_size','performance_score']
    # data.to_csv('processed_data.csv', index=False)
    return data