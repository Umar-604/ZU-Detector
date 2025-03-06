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