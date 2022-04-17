from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from djangoApp.models import *
from fitmodels import *
import joblib
import os

def get_queryset(request):
    result = Diseases_Symptoms.objects.all()
    result = result.distinct().order_by()
    print("data", type(result))
    return render(request, "index.html", {'result':result, 'disable': False, 'show': True, 'back': False})

def result(request):
    #user_list = request.POST.getlist("sevices")
    user_symptoms = request.GET.getlist("services")
    user_symptoms_len = len(set(user_symptoms))
    print("user_symptoms", user_symptoms)
    
    # Get possible subsets with minimum 80% count
    processed_symptoms = GetPossibleSubsets(user_symptoms)

    # Obtains all possible cooccuring symptoms including given symptoms
    cooccuring_symptoms = FindCooccuringSymptomsWithThreshold(user_symptoms)
    processed_symptoms2 = [0 for x in range(0, len(all_symptoms))]
    for symptom in cooccuring_symptoms:
        processed_symptoms2[all_symptoms.index(symptom)] = 1

    processed_symptoms.append(processed_symptoms2)
    #print(processed_symptoms)
    
    no_of_diseases = 10
    
    # Get file path for SAV files
    current_directory = os.getcwd()
    sav_path = current_directory + "/Model-Weights/"
    
    print("Processing with Logistic Regression...")
    lr_cls = joblib.load(sav_path + "log_reg.sav")
    lr_mean_score = joblib.load(sav_path + "log_reg_cv.sav")
    lr_dict = GetTop10BySubsets(lr_cls, lr_mean_score, user_symptoms, processed_symptoms)
    print("Done\n")
    PrintDictionary(lr_dict)

    print("Processing with Random Forest Classifier...")
    rf_cls = joblib.load(sav_path + "rand_forest.sav")
    rf_mean_score = joblib.load(sav_path + "rand_forest_cv.sav")
    rf_dict = GetTop10BySubsets(rf_cls, rf_mean_score, user_symptoms, processed_symptoms)
    print("Done\n")
    PrintDictionary(rf_dict)

    print("Processing with KNN Classifier...")
    knn_cls = joblib.load(sav_path + "knn.sav")
    knn_mean_score = joblib.load(sav_path + "knn_cv.sav")
    knn_dict = GetTop10BySubsets(knn_cls, knn_mean_score, user_symptoms, processed_symptoms)
    print("Done\n")
    PrintDictionary(knn_dict)

    print("Processing with Multinomial Naive Bayes...")
    mnb_cls = joblib.load(sav_path + "mnb.sav")
    mnb_mean_score = joblib.load(sav_path + "mnb_cv.sav")
    mnb_dict = GetTop10BySubsets(mnb_cls, mnb_mean_score, user_symptoms, processed_symptoms)
    print("Done\n")
    PrintDictionary(mnb_dict)

    # We use joint probabilities for the final dictionary & probabilities
    final_dict = {}
    
    # For Logistic Regression
    for (key, val) in lr_dict.items():
        if key not in final_dict:
            final_dict[key] = [lr_dict[key], 1]
        else:
            prob, count = final_dict[key]
            final_dict[key] = [lr_dict[key] + prob, 1 + count]

    # For Random Forest
    for (key, val) in rf_dict.items():
        if key not in final_dict:
            final_dict[key] = [rf_dict[key], 1]
        else:
            prob, count = final_dict[key]
            final_dict[key] = [rf_dict[key] + prob, 1 + count]

    # For KNN Classifier
    for (key, val) in knn_dict.items():
        if key not in final_dict:
            final_dict[key] = [knn_dict[key], 1]
        else:
            prob, count = final_dict[key]
            final_dict[key] = [knn_dict[key] + prob, 1 + count]

    # For Multinomial Naive Bayes
    for (key, val) in mnb_dict.items():
        if key not in final_dict:
            final_dict[key] = [mnb_dict[key], 1]
        else:
            prob, count = final_dict[key]
            final_dict[key] = [mnb_dict[key] + prob, 1 + count]

            
    # Obtain probability over max.count possible
    processed_dict = {}
    max_prob = 0
    for (key, val) in final_dict.items():
        processed_dict[key] = round(final_dict[key][0] / 4, 2)
        if processed_dict[key] > max_prob:
            max_prob = processed_dict[key]
        #print(key, "...", processed_dict[key], "...", final_dict[key][1])

    # Obtain likeliness range
    prob_100 = round(max_prob, 2)
    prob_50 = round(prob_100 / 2, 2)
    prob_25 = round(prob_50 / 2, 2)
    prob_75 = round(prob_50 + prob_25)

    # Visualize the probability ranges
    print("100% ", prob_100, "\t75% ", prob_75, "\t50% ", prob_50, "\t25% ", prob_25, "\n")

    # Sort dictionary by probabilities & leave off the less possible ones
    final_dict = dict(sorted(processed_dict.items(), key=lambda item: item[1], reverse=True)[:15])
    #PrintDictionary(final_dict)

    # Set count values by range
    for key in final_dict.keys():
        prob, count = final_dict[key], 0
        if prob <= prob_100 and prob > prob_75:
            count = 4
        elif prob <= prob_75 and prob > prob_50:
            count = 3
        elif prob <= prob_50 and prob > prob_25:
            count = 2
        else:
            count = 1
        final_dict[key] = "count" + str(count)
        print(key, ":\t", final_dict[key])
        
    # Sort diseases by count labels & then by their names
    #final_dict = dict(sorted(final_dict.items(), key=lambda x: (x[1],x[0]), reverse=False))
    
    # Pass the final_dict to the UI
    return render(request, "index.html", {"final_dict": final_dict, 'disable': True, 'show': False, 'back': True})