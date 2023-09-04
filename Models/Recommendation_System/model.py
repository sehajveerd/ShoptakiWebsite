import pandas as pd

from preprocessing import DataPreprocessor, CategoricalEmbedding, RecommendationSystem
from sklearn.metrics.pairwise import cosine_similarity


# Load and preprocess data
data_preprocessor = DataPreprocessor("/Users/rasikagulhane/Desktop/real-estate-ai-be/Models/Recommendation_System/final_data.csv")
normalized_content_features = data_preprocessor.preprocess()
content_features = data_preprocessor.data[['bathrooms', 'bedrooms', 'livingArea', 'lotAreaValue', 'price', 'rentZestimate', 'taxAssessedValue', 'Average Score', 'investment_risk']]

# Create and convert categorical embeddings
categorical_embedding = CategoricalEmbedding(data_preprocessor.data)
embeddings = categorical_embedding.create_embeddings()
embedded_categorical_features = categorical_embedding.convert_to_embeddings(embeddings)

# Calculate cosine similarity between properties
combined_features = pd.DataFrame(normalized_content_features, columns=content_features.columns)
combined_features = pd.concat([combined_features, pd.DataFrame(embedded_categorical_features)], axis=1)
similarities = cosine_similarity(combined_features)

# Build recommendation system
recommendation_system = RecommendationSystem(normalized_content_features, embedded_categorical_features, "/Users/rasikagulhane/Desktop/real-estate-ai-be/Models/Recommendation_System/final_data.csv", similarities)

# Property zpid for which you want recommendations
property_zpid = 2075615600    #make changes  while deploying as per click of user 

# Calculate similarity for the specified property zpid
property_similarity = recommendation_system.calculate_similarity(property_zpid)
print("Similarity for property with zpid:", property_similarity)

# Get recommendations for the specified property zpid
num_recommendations = 10        #change no. of recommendation as per needed to display
recommended_zpids = recommendation_system.get_recommendations(property_zpid, num_recommendations)
print("Top recommended property IDs:", recommended_zpids)

