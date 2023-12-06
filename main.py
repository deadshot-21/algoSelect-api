from flask import Flask, jsonify, render_template, request
import random 
import pandas as pd
from joblib import load
import json
app = Flask(__name__)

questions = [
   'What level of security do you require? Are there any known vulnerabilities you need to avoid?',
    'How quickly do you need the algorithm to encrypt and decrypt data? Is speed a crucial factor for your use case?',
    'Do you have the resources and expertise to implement complex algorithms, or do you need something that is easy to implement?',
    'What is your specific use case? Some algorithms are better suited for certain applications than others.',
    'Do you need an algorithm that can be adapted for different uses and applications, or do you have a specific use case in mind?',
    'Will the amount of data you need to encrypt increase over time? If so, how well does the algorithm scale with increasing data size?',
    'How secure do you need the encryption to be? Larger keys generally provide more security, but they can also slow down the algorithm.',
    'What is the size of the data blocks that you will be working with? Does your data naturally fit into a certain block size?',
    'Are there specific types of attacks you are concerned about? Different algorithms have different vulnerabilities.'

]

answers = [["High","Low"],["Fast","Moderate","Slow"],["Moderate"],[
    "Military Communications",
    "Online Banking",
    "Secure Communications",
    "Personal Projects", #
    "Financial Institutions",
    "Software Development",
    "Sensitive Data Encryption", #
    "File and Folder Encryption", #
    "Cloud Storage",
    "Network Protocols",
    "Password Hashing",
    "File Encryption", #
    "Disk Encryption",
    "Email Encryption",
    "Secure Shell"
],["High","Moderate"], ["High","Moderate"], [56,112,128,168,192,256,"adaptive"], [128,64], [
    "Brute-force Attack",
    "Differential Attack",
    "Related-key Attack",
    "Sweet32 Attack",
    "Meet-in-the-Middle Attack",
    "Truncated Differential Cryptanalysis",
    "Impossible Differential Attack",
    "Side-channel Attack",
    "Second-order Differential Attack",
    "Weak Key Attack",
    "Known-plaintext Attack"
]]

question_encoding = {
    'What level of security do you require? Are there any known vulnerabilities you need to avoid?': 0,
    'How quickly do you need the algorithm to encrypt and decrypt data? Is speed a crucial factor for your use case?': 1,
    'Do you have the resources and expertise to implement complex algorithms, or do you need something that is easy to implement?': 2,
    'What is your specific use case? Some algorithms are better suited for certain applications than others.': 3,
    'Do you need an algorithm that can be adapted for different uses and applications, or do you have a specific use case in mind?': 4,
    'Will the amount of data you need to encrypt increase over time? If so, how well does the algorithm scale with increasing data size?': 5,
    'How secure do you need the encryption to be? Larger keys generally provide more security, but they can also slow down the algorithm.': 6,
    'What is the size of the data blocks that you will be working with? Does your data naturally fit into a certain block size?': 7,
    'Are there specific types of attacks you are concerned about? Different algorithms have different vulnerabilities.': 8
}
answer_encoding = {
    "High": 10,
    "Low": 11,
    "Fast": 12,
    "Moderate": 13,
    "Slow": 14,
    "Doesn't Matter": 15,
    "Military Communications": 16,
    "Online Banking": 17,
    "Secure Communications": 18,
    "Personal Projects": 19,
    "Financial Institutions": 20,
    "Software Development": 21,
    "Sensitive Data Encryption": 22,
    "File and Folder Encryption": 23,
    "Cloud Storage": 24,
    "Network Protocols": 25,
    "Password Hashing": 26,
    "File Encryption": 27,
    "Disk Encryption": 28,
    "Email Encryption": 29,
    "Secure Shell": 30,
    56: 31,
    112: 32,
    128: 33,
    168: 34,
    192: 35,
    256: 36,
    "adaptive": 37,
    64: 38,
    "Brute-force Attack": 39,
    "Differential Attack": 40,
    "Related-key Attack": 41,
    "Sweet32 Attack": 42,
    "Meet-in-the-Middle Attack": 43,
    "Truncated Differential Cryptanalysis": 44,
    "Impossible Differential Attack": 45,
    "Side-channel Attack": 46,
    "Second-order Differential Attack": 47,
    "Weak Key Attack": 48,
    "Known-plaintext Attack": 49
}
def encode_list_pair(lis):
  encoded_list=[]
  for y1,y2 in lis:
    t=[]
    t.append(question_encoding[y1])
    t.append(answer_encoding[y2])
    encoded_list.append(t)
  return encoded_list
def encode_list(lis):
  encoded_list=[]
  for x in lis:
    if x=="end":
      encoded_list.append(-1)
    else:
      encoded_list.append(question_encoding[x])
  return encoded_list

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/nextQuestion', methods=['POST'])
def addCafe():
    if request.method == 'POST':
        # logic here
        print(request.form)
        new_pair_encoded = encode_list_pair([[questions[int(request.form.get('current_question'))], answers[int(request.form.get('current_question'))][int(request.form.get('user_answer'))]]])
        clf = load('question-tree.joblib')
        predicted = clf.predict(new_pair_encoded)
        return jsonify(response={"next_question": str(predicted[0])})
    
@app.route('/results', methods=['POST'])
def updatePrice():
    if request.method == 'POST':
        df = pd.read_csv('data.csv')
        # list(df.iloc[5])
        print(json.loads(request.form.get('responses')))
        algos=[]
        for i in range(6):
          algos.append(list(df.iloc[i]))
        # print(algos)
        weights=[100,100,10,200,50,50,100,10,10]
        score=[]
        for i in range(len(algos)):
          s=0
          for c,r in json.loads(request.form.get('responses')):
            if algos[i][c+1] == r or str(r) in str(algos[i][c+1]):
              s+=weights[c]
          score.append(s)

        # algos[score.index(max(score))]
        return jsonify(result={"algo_details":algos[score.index(max(score))]}), 200
    return jsonify(error={"Error": "404"}), 404

if __name__ == '__main__':
    app.run(debug=True)
