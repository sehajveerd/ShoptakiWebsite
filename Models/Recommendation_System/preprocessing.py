import numpy as np
import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from torch.nn import functional as F




class DataPreprocessor:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)
    
    def preprocess(self):
        content_features = self.data[['bathrooms', 'bedrooms', 'livingArea', 'lotAreaValue', 'price', 'rentZestimate', 'taxAssessedValue', 'Average Score', 'investment_risk']]
        
        scaler = MinMaxScaler()
        normalized_content_features = scaler.fit_transform(content_features)
        
        return normalized_content_features




class CategoricalEmbedding:
    def __init__(self, data):
        self.data = data
        self.embedding_dims = {
            'city': 16,
            'homeType': 4,
            'state': 8,
            'newConstructionType': 2,
            'Average Risk Level': 3
        }
    
    def create_embeddings(self):
        embeddings = {}
        for feature, dim in self.embedding_dims.items():
            self.unique_values = self.data[feature].unique()
            embedding = torch.nn.Embedding(len(self.unique_values), dim)
            embeddings[feature] = embedding
        return embeddings
    
    def convert_to_embeddings(self, embeddings):
        embedded_categorical_features = []
        for feature, embedding in embeddings.items():
            values = self.data[feature].values
            indices = [np.where(self.unique_values == value)[0][0] if value in self.unique_values else 0 for value in values]
            indices = torch.tensor(indices)
            embedded = embedding(indices)
            embedded_categorical_features.append(embedded.detach().numpy())
        return np.concatenate(embedded_categorical_features, axis=1)



class RecommendationSystem:

   
    def __init__(self, normalized_content_features, embedded_categorical_features, data_file, similarities 
):
        self.normalized_content_features = normalized_content_features
        self.embedded_categorical_features = embedded_categorical_features
        self.data = pd.read_csv(data_file)
        self.content_features = self.data[['bathrooms', 'bedrooms', 'livingArea', 'lotAreaValue', 'price', 'rentZestimate', 'taxAssessedValue', 'Average Score', 'investment_risk']]
        self.similarities = similarities


    def calculate_similarity(self, zpid):
        property_index = self.data[self.data['zpid'] == zpid].index[0]
        combined_features = pd.DataFrame(self.normalized_content_features, columns=self.content_features.columns)
        combined_features = pd.concat([combined_features, pd.DataFrame(self.embedded_categorical_features)], axis=1)
        property_features = combined_features.iloc[property_index]
        
        similarities = cosine_similarity([property_features], combined_features)
        return similarities[0]


    def get_recommendations(self, zpid, num_recommendations=10):
        property_index = self.data[self.data['zpid'] == zpid].index[0]
        similar_properties = self.similarities[property_index]
        sorted_indices = similar_properties.argsort()[::-1]
        top_recommendations = sorted_indices[1:num_recommendations + 1]
        
        recommended_zpids = self.data.iloc[top_recommendations]['zpid'].tolist()
        return recommended_zpids


