import pickle

# load old pipeline
with open('pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)

print(type(pipeline))

# re-save correctly
with open('pipeline_fixed.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

print("PIPELINE FIXED")