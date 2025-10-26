from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the modified dataset
df = pd.read_csv('modified_dataset.csv', dtype=str)

@app.route('/frontend', methods=['GET', 'POST'])
def home():
    positive_reviews = []
    negative_reviews = []
    city = ''
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            city_reviews = df[df['City'].str.contains(city, case=False, na=False)]
            if not city_reviews.empty:
                positive_reviews = city_reviews['positive_review'].astype(str).tolist()
                negative_reviews = city_reviews['negative_review'].astype(str).tolist()

    # Add numeric labels
    positive_reviews_labeled = [f"{i+1}. {review}" for i, review in enumerate(positive_reviews)]
    negative_reviews_labeled = [f"{i+1}. {review}" for i, review in enumerate(negative_reviews)]

    return render_template('frontend.html', city=city, positive_reviews=positive_reviews_labeled, negative_reviews=negative_reviews_labeled)




if __name__ == '__main__':

    app.run(debug=True)
