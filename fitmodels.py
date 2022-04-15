import warnings
warnings.filterwarnings("ignore")
import pandas as pd
# Load datasets for all possible combinations & for individual disease's respective symptoms
df_combination = pd.read_csv("./Disease_Symptom_Dataset_For_All_Symptom_Subsets.csv") 
df_independent = pd.read_csv("./Disease_Symptom_Dataset_For_Respective_Symptoms.csv") 

X_combination = df_combination.iloc[:, 1:]
Y_combination = df_combination.iloc[:, 0:1]

X_independent = df_independent.iloc[:, 1:]
Y_independent = df_independent.iloc[:, 0:1]

# List of all possible symptoms
all_symptoms = list(X_independent.columns)
all_diseases = list(set(Y_independent['Disease_Name']))
all_diseases.sort()

# We obtain top 10 possible diseases
no_of_diseases = 10

# Function to display the results from the dictionary
def PrintResults(top10_sorted_dict):
    for (key, value) in top10_sorted_dict.items():
        print(key, "\t", value, "%")


# Function to print list contents
def printList(list_data):
    for item in list_data:
        print(item)

def ProcessResultAndGenerateDiseases(top10_list):
    
    global df_independent, all_symptoms, all_diseases, processed_symptoms
    top10_diseases = []
    #top10_dict = {}

    # Checks for each disease, the matched symptoms & generates probability of having that disease
    for (idx, disease_id) in enumerate(top10_list):
        matched_symptoms = set()
        top10 = df_independent.loc[df_independent['Disease_Name'] == all_diseases[disease_id]].values.tolist()
        
        # Obtains the disease name which is at the top of the dataframe
        disease = top10[0].pop(0)

        # Each row contains 0s & 1s indicating whether a disease is associated with a particular symptom or not
        for (idx, value) in enumerate(top10[0]):
            if value != 0:
                matched_symptoms.add(all_symptoms[idx])
                
        #probability = (len(matched_symptoms.intersection(set(processed_symptoms))) + 1) / (len(set(processed_symptoms)) + 1)
        #top10_dict[disease] = round(probability * mean_score * 100, 2)
        top10_diseases.append(disease)
    
    #top10_sorted = dict(sorted(top10_dict.items(), key=lambda kv: kv[1], reverse=True))
    return sorted(top10_diseases)    #top10_sorted
# Function to find co-occuring symptoms with all the symptoms user chosen
# We use a threshold to check for a 80% match with the given symptoms

def FindCooccuringSymptomsWithThreshold(user_symptoms):
    
    global df_independent, all_symptoms
    threshold = len(user_symptoms)

    # Get all unique possible diseases with the given symptoms
    unique_diseases = set()
    for symptom in user_symptoms:
        possible_diseases_for_symptom = list(df_independent[df_independent[symptom] == 1]['Disease_Name'])
        for disease in possible_diseases_for_symptom:
            unique_diseases.add(disease)
        
    # Get all unique diseases & sort them
    unique_diseases = sorted(list(unique_diseases))
    
    #print(unique_diseases)

    # Obtain co-occuring symptoms with 80% threshold
    # cooccuring_symptoms must have all given symptoms by default
    cooccuring_symptoms = set(user_symptoms)   
    for disease in unique_diseases:
        
        # First, obtain all symptoms associated with each disease in unique diseases obtained
        symptoms_of_disease = df_independent.loc[df_independent['Disease_Name'] == disease].values.tolist().pop(0)

        # Maintain a temporary set of symptoms of the disease & add them only when they meet threshold requirements
        temp_symptoms = set()
        count, add_symptoms = 0, False
        for idx in range(len(symptoms_of_disease)):
            
            # Symptoms of a disease will have 1 in their respective symptom columns
            if symptoms_of_disease[idx] == 1:
                temp_symptoms.add(all_symptoms[idx])
                count = count + 1
                # Our threshold is set to 80% of original symptoms
                if count > threshold:
                    add_symptoms = True

        # Adds temporary symptoms to cooccuring symptoms only if they meet threshold requirements
        if add_symptoms == True:
            for symp in temp_symptoms:
                cooccuring_symptoms.add(symp)

    cooccuring_symptoms = sorted(list(cooccuring_symptoms))
    return cooccuring_symptoms


