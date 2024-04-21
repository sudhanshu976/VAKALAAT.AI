from flask import Flask, render_template, request, redirect, url_for
import os
from helper import download_hugging_face_embeddings
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from prompt import *
import os
from langchain.vectorstores import FAISS
import pandas as pd
import random

app = Flask(__name__)
embeddings = download_hugging_face_embeddings()


db = FAISS.load_local("faiss_index", embeddings)


PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs={"prompt": PROMPT}

llm=CTransformers(model="model\llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8})


qa=RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=db.as_retriever(search_kwargs={'k': 1}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs
    )


# Load existing data or create a new DataFrame
CSV_FILE = 'lawyers.csv'
if os.path.exists(CSV_FILE):
    lawyers_df = pd.read_csv(CSV_FILE)
else:
    lawyers_df = pd.DataFrame(columns=['id', 'name', 'description', 'image_path'])

def recommend_lawyers(query):
    global lawyers_df

    if query:
        # Filter lawyers based on search query
        filtered_lawyers = lawyers_df[lawyers_df['description'].str.contains(query, case=False)]
        # Convert filtered lawyers to dictionary format
        lawyer_data = filtered_lawyers.to_dict(orient='records')
    else:
        # Randomly select 3 lawyers if no search query is provided
        random_lawyers = lawyers_df.sample(n=3)
        # Convert randomly selected lawyers to dictionary format
        lawyer_data = random_lawyers.to_dict(orient='records')

    return lawyer_data

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/buy_documents.html')
def buy_documents():
    return render_template('buy_documents.html')

@app.route('/lawyers')
def lawyers():
    query = request.args.get('query')
    recommended_lawyers = recommend_lawyers(query)
    return render_template('lawyers.html', lawyers=recommended_lawyers)

@app.route('/join', methods=['POST'])
def join_as_lawyer():
    global lawyers_df

    # Get form data
    name = request.form['name']
    description = request.form['description']
    photo = request.files['photo']

    # Save photo to static/images folder
    photo_path = os.path.join('static', 'images', photo.filename)
    photo.save(photo_path)

    # Generate unique ID
    id = len(lawyers_df) + 1

    # Create a new DataFrame with the new row
    new_row = pd.DataFrame({'id': [id], 'name': [name], 'description': [description], 'image_path': [photo_path]})

    # Concatenate the new DataFrame with the existing DataFrame
    lawyers_df = pd.concat([lawyers_df, new_row], ignore_index=True)

    # Save DataFrame to CSV
    lawyers_df.to_csv(CSV_FILE, index=False)

    return redirect(url_for('success'))

@app.route("/lawgpt")
def index():
    return render_template('chat.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
