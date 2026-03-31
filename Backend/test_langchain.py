from langchain_faq import load_faq_vectorstore

vs = load_faq_vectorstore()

docs = vs.similarity_search("college timing", k=1)
print(docs[0].metadata["answer"])
