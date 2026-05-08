import pickle

files = [
    'pipeline',
    'df'
]

for file_name in files:

    print(f"\nProcessing {file_name}...")

    # load old pickle
    with open(f'{file_name}.pkl', 'rb') as f:
        data = pickle.load(f)

    print(type(data))

    # save new compatible pickle
    with open(f'{file_name}_FIXED.pkl', 'wb') as f:
        pickle.dump(data, f)

    print(f"{file_name} FIXED")

print("\nALL FILES CONVERTED")