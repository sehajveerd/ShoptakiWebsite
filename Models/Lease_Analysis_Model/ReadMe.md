# Code Walk through:

## PDF to Text Conversion and Text Classification

This Python script demonstrates how to extract text from a PDF file and then perform text classification using machine learning techniques. The script uses the PyMuPDF library for PDF text extraction and scikit-learn for building a Naive Bayes text classifier.

## PDF to Text Conversion
The pdf_to_text function in the script extracts text content from a given PDF file using the PyMuPDF library. Each page's text is concatenated to form the complete text content. The extracted text is then saved to a text file.

## Text Classification
The script also showcases text classification using a Naive Bayes classifier from scikit-learn. It uses a simulated dataset of lease agreement examples along with associated insights. The script preprocesses the text data, splits it into training and testing sets, and trains the classifier.

The trained classifier and vectorizer are saved as trained_model.joblib and vectorizer.joblib respectively.

## Predicting Insights from New Lease Agreements
The script demonstrates how to predict insights from new lease agreement text. It loads the trained classifier and vectorizer, reads a new lease agreement from a file, and predicts insights for it. It then extracts the relevant line containing the keyword associated with each predicted insight.

Feel free to modify and adapt the code as needed for your specific use case.
