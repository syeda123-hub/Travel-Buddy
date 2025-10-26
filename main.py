from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset into a DataFrame
df = pd.read_csv('modified_dataset.csv', dtype=str)

@app.route('/combined', methods=['GET', 'POST'])
def combined():
    positive_reviews = []
    negative_reviews = []
    average_rating = None
    city = ''
    no_negative_reviews = False  # Flag for "no negative reviews"
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            city_reviews = df[df['City'].str.contains(city, case=False, na=False)]
            if not city_reviews.empty:
                positive_reviews = city_reviews['positive_review'].dropna().astype(str).tolist()
                negative_reviews = city_reviews['negative_review'].dropna().astype(str).tolist()
                average_rating = city_reviews['Rating'].astype(float).mean()

    # Handle review alignment
    if not negative_reviews:  
        # Case 1: No negative reviews at all
        no_negative_reviews = True
    else:
        # Case 2: Keep only real reviews (no NaN placeholders)
        negative_reviews = [r for r in negative_reviews if r.strip().lower() != 'nan']
    
    positive_reviews = [r for r in positive_reviews if r.strip().lower() != 'nan']

    # Add numbering for display
    positive_reviews_labeled = [f"{i+1}. {r}" for i, r in enumerate(positive_reviews)]
    negative_reviews_labeled = [f"{i+1}. {r}" for i, r in enumerate(negative_reviews)]

    return render_template(
        'combined.html',
        city=city,
        positive_reviews=positive_reviews_labeled,
        negative_reviews=negative_reviews_labeled,
        average_rating=average_rating,
        no_negative_reviews=no_negative_reviews
    )


if __name__ == '__main__':
    app.run(debug=True)
