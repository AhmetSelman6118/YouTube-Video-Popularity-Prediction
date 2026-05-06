from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, KFold
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def model_results(model, train_data, show_message=True, n_splits=10):
    if show_message:
        print("=" * 10, f"MODEL K-FOLD VALIDATION FOR {model.__class__.__name__.upper()}", "=" * 10, "\n")

    k_fold = KFold(n_splits=n_splits, shuffle=True)
    acc_scores = []
    pre_scores = []
    rec_scores = []
    f1_scores = []
    
    i = 0
    for train_indices, test_indices in k_fold.split(train_data):
        X_train = train_data[train_indices, :-1]
        y_train = train_data[train_indices, -1]
        X_test = train_data[test_indices, :-1]
        y_test = train_data[test_indices, -1]

        model = model.fit(X_train, y_train)
        pred = model.predict(X_test)

        acc_score = accuracy_score(y_test, pred)
        pre_score = precision_score(y_test, pred)
        rec_score = recall_score(y_test, pred)
        f1_scoree = f1_score(y_test, pred)

        if show_message:
            print(f"Fold {i+1}:")
            print(f"Accuracy: {acc_score:.2f}")
            print(f"Precision: {pre_score:.2f}") 
            print(f"Recall: {rec_score:.2f}") 
            print(f"F1 Score: {f1_scoree:.2f}")
            print()

        acc_scores.append(acc_score)
        pre_scores.append(pre_score)
        rec_scores.append(rec_score)
        f1_scores.append(f1_scoree)

    mean = lambda x: sum(x) / len(x)

    results = {
        "model": model.__class__.__name__,
        "accuracy_mean": mean(acc_scores),
        "precision_mean": mean(pre_scores),
        "recall_mean": mean(rec_scores),
        "f1_score_mean": mean(f1_scores)
    }
    results["average"] = (results["accuracy_mean"] + results["precision_mean"] + \
                          results["recall_mean"] + results["f1_score_mean"]) / 4
    
    if show_message:
        print("-- K-FOLD AVERAGE RESULTS --")
        print(f"Avg. Accuracy: {results["accuracy_mean"]}")
        print(f"Avg. Precision: {results['precision_mean']}")
        print(f"Avg. Recall: {results['recall_mean']}")
        print(f"Avg. F1 Score: {results['f1_score_mean']}")
        print(f"Overall Score: {results["average"]}")

    return results

def compare_models(model_list, train_data):
    results = []
    print("=" * 15, "FINDING OPTIMAL MODEL", "=" * 15, "\n")

    for model in model_list:
        model_res = model_results(model, train_data, show_message=False)    

        print()
        print(f"Model name: {model_res["model"]}")
        print(f"Accuracy score: {model_res["accuracy_mean"]}")
        print(f"Precision score: {model_res["precision_mean"]}")
        print(f"Recall score: {model_res["recall_mean"]}")
        print(f"F1 score: {model_res["f1_score_mean"]}")
        print(f"Average score: {model_res["average"]}")
        print()

        results.append((model_res["model"], model_res["precision_mean"]))
    
    sorted_res = sorted(results, key=lambda res: res[1], reverse=True)
    top_3_models = sorted_res[:3]
    model_podium = dict(top_3_models)

    return model_podium

def tune_model(model):
    pass