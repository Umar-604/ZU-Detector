import pickle

# Take URL input
urls = []
urls.append(input("Input the URL that you want to check (e.g., google.com): "))

# Define a whitelist of trusted domains
whitelist = ['hackthebox.eu', 'root-me.org', 'gmail.com']

# Sanitization function for processing URLs
def improved_sanitization(url):
    url = str(url).lower()  # Ensure input is a string and lowercase it
    url = url.split('://')[-1]  # Remove protocol
    if url.startswith('www.'):
        url = url[4:]  # Remove 'www.'
    parts = url.split('/')
    tokens = []
    for part in parts:
        sub_tokens = part.replace('.', '-').split('-')
        tokens.extend([token for token in sub_tokens if token and token not in ['com', 'org', 'net']])
    return tokens

# Filter URLs that are not in the whitelist
s_url = [i for i in urls if i not in whitelist]

# Classify the URL with probability prediction
if len(s_url) == 0:
    # If URL is in the whitelist, classify as "good"
    predict = ['good']
else:
    try:
        # Load the final model, which contains the vectorizer, SVD, and trained models
        with open("final_model.pkl", 'rb') as f1:
            final_model = pickle.load(f1)
        
        # Extract components from the pickle file
        vectorizer = final_model['vectorizer']  # TF-IDF vectorizer
        svd = final_model['svd']  # TruncatedSVD for dimensionality reduction
        models = final_model['models']  # List of models (RandomForest, Logistic Regression)
        
        # Load the individual models
        rf_model = models[0]  # Random Forest model
        logreg_model = models[1]  # Logistic Regression model
        
        # Ensure models are loaded correctly
        if not hasattr(rf_model, 'predict_proba') or not hasattr(logreg_model, 'predict_proba'):
            raise TypeError("Models are not loaded correctly. Check their contents.")
        
    except FileNotFoundError:
        print("Model file not found. Ensure the file is in the correct directory.")
        exit()
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        exit()

    # Apply sanitization to the URL before vectorization
    sanitized_url = [improved_sanitization(url) for url in s_url]
    sanitized_text = [' '.join(tokens) for tokens in sanitized_url]  # Join tokens for vectorization

    # Apply vectorizer transformation to sanitized URL
    x = vectorizer.transform(sanitized_text)

    # Apply the same TruncatedSVD transformation
    x_reduced = svd.transform(x)  # Apply SVD for dimensionality reduction

    # Get the class probabilities using predict_proba for both models
    rf_proba = rf_model.predict_proba(x_reduced)
    logreg_proba = logreg_model.predict_proba(x_reduced)

    # Combine predictions from both models using majority voting
    final_prediction = []
    for rf_prob, logreg_prob in zip(rf_proba, logreg_proba):
        rf_pred = 'bad' if rf_prob[1] > 0.5 else 'good'
        logreg_pred = 'bad' if logreg_prob[1] > 0.5 else 'good'

        # Majority Voting: Pick the most common result between the models
        final_prediction.append(max([rf_pred, logreg_pred], key=[rf_pred, logreg_pred].count))

    # Final prediction
    predict = final_prediction

# Print the prediction result
print("\nThe entered domain is classified as:", predict[0])
