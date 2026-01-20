import pandas as pd

def transform_data(df, transformations):
    for transform in transformations:
        if transform['type'] == 'rename':
            df = df.rename(columns=transform['mapping'])
        elif transform['type'] == 'drop':
            df = df.drop(columns=transform['columns'])
        elif transform['type'] == 'date_format':
            df[transform['column']] = pd.to_datetime(df[transform['column']], format=transform['format'])
    return df