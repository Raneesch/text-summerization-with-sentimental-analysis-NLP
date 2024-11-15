def summerizer(rowdata):
    import spacy
    from spacy.lang.en.stop_words import STOP_WORDS
    from string import punctuation
    from heapq import nlargest
 

    # Load stopwords and NLP model
    stopword = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    
    # Process text with NLP model
    doc = nlp(rowdata)
    tokens = [token.text for token in doc]
    punctuation = punctuation + "\n"

    # Compute word frequencies, excluding stop words and punctuation
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopword and word.text not in punctuation:
            word_frequencies[word.text] = word_frequencies.get(word.text, 0) + 1
    # normalize word frequencies
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] /= max_frequency

    # Score sentences based on word frequencies
    sentences_tokens = [sent for sent in doc.sents]
    sentences_scores = {}
    for sent in sentences_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                sentences_scores[sent] = sentences_scores.get(sent, 0) + word_frequencies[word.text.lower()]

    # Select top sentences for summary
    select_length = int(len(sentences_tokens) * 0.3)
    summary_sentences = nlargest(select_length, sentences_scores, key=sentences_scores.get)
    final_summary = " ".join([sent.text for sent in summary_sentences])

    # Sentiment analysis
    from transformers import pipeline
    
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    sentiment = sentiment_analyzer(final_summary)

    return final_summary,doc,len(rowdata.split(' ')),len(final_summary.split(' ')),sentiment



# Example usage:
# rowdata = """Happiness is a profound and often elusive state of being, a feeling that resonates deeply within us and shapes our perceptions, decisions, and relationships. It is more than just the joy we feel in moments of celebration or achievement. Happiness is a complex tapestry woven from threads of contentment, satisfaction, and peace, each thread reflecting aspects of our values, goals, and experiences. Some describe happiness as a sense of being truly alive, fully engaged in the present moment, and free from the burdens of past regrets or future worries. It may emerge in the stillness of a morning sunrise, where the quiet beauty of nature speaks to the soul, or in the laughter shared with friends and family, where connection and belonging nourish the spirit.

# Happiness is influenced by countless factors, both internal and external. Our environment, health, relationships, and sense of purpose play vital roles in shaping our happiness, yet it remains something deeply personal and subjective. For one person, happiness might mean a fulfilling career and a secure future; for another, it could be the simple pleasures of life, like spending time with loved ones or pursuing a beloved hobby. In the pursuit of happiness, people often seek fulfillment in various ways – through travel, self-discovery, personal growth, and acts of kindness, each endeavor adding to their understanding of joy.

# Some philosophical perspectives suggest that happiness lies not in external accomplishments or material possessions but in our inner approach to life. By cultivating gratitude, mindfulness, and compassion, we can foster a mindset that embraces life’s imperfections and finds joy in the present. True happiness often comes from a sense of balance and acceptance – an understanding that while life may bring challenges and hardships, we have the power to respond with resilience and optimism."""
# summary, sentiment, word_count = summerizer(rowdata)
# print("Summary:", summary)
# print("Sentiment:", sentiment)
# print("Word Count:", word_count)




