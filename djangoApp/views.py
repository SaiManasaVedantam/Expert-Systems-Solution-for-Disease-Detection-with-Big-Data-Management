from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import TemplateView,ListView

from djangoApp.models import *

from fitmodels import *
import joblib

# class IndexView(ListView):
#     template_name = "index.html"
def get_queryset(request):
    result = Diseases_Symptoms.objects.all()
    result = result.distinct().order_by()
    print("data", type(result))
    return render(request, "index.html", {'result':result, 'disable': False, 'show': True, 'back': False})

def result(request):
    #user_list = []
    # user_list = request.POST.getlist("sevices")
    # Load datasets for all possible combinations & for individual disease's respective symptoms
    user_symptoms = request.GET.getlist('services')
    print("user_symptoms", user_symptoms)
    # Obtains all possible cooccuring symptoms including given symptoms
    cooccuring_symptoms = FindCooccuringSymptomsWithThreshold(user_symptoms)
    # print(cooccuring_symptoms)
    no_of_diseases = 10
    # Process obtained symptoms to create rows compatible with the dataset
    processed_symptoms = [0 for x in range(0, len(all_symptoms))]
    for symptom in cooccuring_symptoms:
    # for symptom in user_symptoms:
        processed_symptoms[all_symptoms.index(symptom)] = 1
    
    lr_cls = joblib.load('log_reg.sav')
    lr_result = lr_cls.predict_proba([processed_symptoms])
    
    rn_cls = joblib.load('random_forest.sav')
    rf_result = rn_cls.predict_proba([processed_symptoms])

    knn_cls = joblib.load('knn.sav')
    knn_result = knn_cls.predict_proba([processed_symptoms])

    mnb_cls = joblib.load('mnb.sav')
    mnb_result = mnb_cls.predict_proba([processed_symptoms])

        # Logistic Regression result
    print("---------- LOGISTIC REGRESSION: ----------\n")

    lr_top10 = lr_result[0].argsort()[-no_of_diseases:][::-1]
    lr_list = ProcessResultAndGenerateDiseases(lr_top10)
    printList(lr_list)

    # Random Forest result
    print("\n---------- RANDOM FOREST: ----------\n")

    rf_top10 = rf_result[0].argsort()[-no_of_diseases:][::-1]
    rf_list = ProcessResultAndGenerateDiseases(rf_top10)
    printList(rf_list)

    # Knn Result
    print("\n---------- KNN CLASSIFIER: ----------\n")

    knn_top10 = knn_result[0].argsort()[-no_of_diseases:][::-1]
    knn_list = ProcessResultAndGenerateDiseases(knn_top10)
    printList(knn_list)

    # Multinomial Naive bayes Result
    print("\n---------- MULTINOMIAL NAIVE BAYES: ----------\n")

    mnb_top10 = mnb_result[0].argsort()[-no_of_diseases:][::-1]
    mnb_list = ProcessResultAndGenerateDiseases(mnb_top10)
    printList(mnb_list)
    dictionary = {}
    for d in lr_list:
        if d not in dictionary:
            dictionary[d] = 0
        dictionary[d] += 1
    for d in rf_list:
        if d not in dictionary:
            dictionary[d] = 0
        dictionary[d] += 1
    for d in knn_list:
        if d not in dictionary:
            dictionary[d] = 0
        dictionary[d] += 1
    for d in mnb_list:
        if d not in dictionary:
            dictionary[d] = 0
        dictionary[d] += 1
    final_dict = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True)[:10])
    print(final_dict)
    for f in final_dict:
        final_dict[f] = "count"+str(final_dict[f])
    return render(request, "index.html", {"final_dict": final_dict, 'disable': True, 'show': False, 'back': True})