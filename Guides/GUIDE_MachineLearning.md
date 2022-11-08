# Machine learning glossary (in the context of MVPA)
The following glossary is copied from a paper on describing a matlab toolbox for MVPA: https://www.frontiersin.org/articles/10.3389/fnins.2020.00289/fullMVPA 
For an in-depth introduction to machine learning refer to standard textbooks (Bishop, 2007; Hastie et al., 2009; James et al., 2013).

* **Binary classifier**. A classifier trained on data that contains two classes, such as in the “faces vs. houses” experiment. If there is more than two classes, the classifier is called a multi-class classifier.

* **Classification**. One of the primary applications of MVPA. In classification, a classifier takes a multivariate pattern of brain activity (referred to as feature vector) as input and maps it onto a categorical brain state or experimental condition (referred to as class label). In the “faces vs. houses” experiment, the classifier is used to investigate whether patterns of brain activity can discriminate between faces and houses.

* **Classifier**. An algorithm that performs classification, for instance Linear Discriminant Analysis (LDA) and Support Vector Machine (SVM).

* **Classifier output**. If a classifier receives a pattern of brain activity (feature vector) as input, its output is a predicted class label e.g., “face.” Many classifiers are also able to produce class probabilities (representing the probability that a brain pattern belongs to a specific class) or decision values.

* **Class label**. Categorical variable that represents a label for each sample/trial. In the “faces vs. houses” experiment, the class labels are “face” and “house.” Class labels are often encoded by numbers, e.g., “face” = 1 and “house” = 2, and arranged as a vector. For instance, the class label vector [1, 2, 1] indicates that a subject viewed a face in trial 1, a house in trial 2, and another face in trial 3.

* **Cross-validation**. To obtain a realistic estimate of classification or regression performance and control for overfitting, a model should be tested on an independent dataset that has not been used for training. In most neuroimaging experiments, there is only one dataset with a restricted number of trials. K-fold cross-validation makes efficient use of such data by splitting it into k different folds. In every iteration, one of the k folds is held out and used as test set, whereas all other folds are used for training. This is repeated until every fold served as test set once. Since cross-validation itself is stochastic due to the random assignment of samples to folds, it can be useful to repeat the cross-validation several times and average the results. See Lemm et al. (2011) and Varoquaux et al. (2017) for a discussion of cross-validation and potential pitfalls.

* **Data**. From the perspective of a classifier or regression model, a dataset is a collection of samples (e.g., trials in an experiment). Each sample consists of a brain pattern and a corresponding class label or response. In formal notation, each sample consists of a pair (x, y) where x is a feature vector and y is the corresponding class label or response.

* **Decision boundary**. Classifiers partition feature space into separate regions. Each region is assigned to a specific class. Classifiers make predictions for a test sample by looking up into which region it falls. The boundary between regions is known as decision boundary. For linear classifiers, the decision boundary is also known as a hyperplane.

* **Decision value**. Classifiers such as LDA and SVM produce decision values which can be thresholded to produce class labels. For linear classifiers and kernel classifiers, a decision value represents the distance to the decision boundary. The further away a test sample is from the decision boundary, the more confident the classifier is about it belonging to a particular class. Decision values are unitless.

* **Decoder**. An alternative term for a classifier or regression model that is popular in the neuroimaging literature. The term nicely captures the fact that it tries to invert the encoding process. In encoding e.g., a sensory experience such as viewing a face is translated into a pattern of brain activity. In decoding, one starts from a pattern of brain activity and tries to infer whether it was caused by a face or a house stimulus.

* **Feature**. A feature is a variable that is part of the input to a model. If the dataset is tabular with rows representing samples, it typically corresponds to one of the columns. In the “faces vs. houses” experiment, each voxel represents a feature.

* **Feature space**. Usually a real vector space that contains the feature vectors. The dimensionality of the feature space is equal to the number of features.

* **Feature vector**. For each sample, features are stored in a vector. For example, consider a EEG measurement with three electrodes Fz, Cz, and Oz and corresponding voltages 40, 65, and 97 μV. The voltage at each EEG sensor represents a feature, so the corresponding feature vector is the vector [40, 65, 97] ∈ ℝ3.

* **Fitting (a model)**. Same as training.

* **Hyperparameter**. A parameter of a model that needs to be specified by the user, such as the type and amount of regularization applied, the type of kernel, and the kernel width γ for Gaussian kernels. From the user's perspective, hyperparameters can be nuisance parameters: it is sometimes not clear a priori how to set them, but their exact value can have a substantial effect on the performance of the model.

* **Hyperparameter tuning**. If it is unclear how a hyperparameter should be set, multiple candidate values can be tested. Typically, this is done via nested cross-validation: the training set is again split into separate folds. A model is trained for each of the candidate values and its performance is evaluated on the held-out fold, called validation set. Only the model with the best performance is then taken forward to the test set.

* **Hyperplane**. For linear classifiers, the decision boundary is a hyperplane. In the special case of a two-dimensional feature space, a hyperplane corresponds to a straight line. In three dimensions, it corresponds to a plane.

* **Loss function**. A function that is used for training. The model parameters are optimized such that the loss function attains a minimum value. For instance, in Linear Regression the sum of squares of the residuals serves as a loss function.

* **Metric**. A quantitative measure of the performance of a model on a test set. For example, precision/recall for classification or mean squared error for regression.

* **Model**. In the context of this paper, a model is a classifier or regression model.

* **Multi-class classifier**. A classifier trained on data that contains three or more classes. For instance, assume that in the “faces vs. houses” experiment additional images have been presented depicting “animals” and “tools.” This would define four classes in total, hence classification would require a multi-class classifier.

* **Overfitting**. Occurs when a model over-adapts to the training data. As a consequence, it will perform well on the training set but badly on the test set. Generally speaking, overfitting is more likely to occur if the number of features is larger than the number of samples, and more likely for complex non-linear models than for linear models. Regularization can serve as an antidote to overfitting.

* **Parameters**. Models are governed by parameters e.g., beta coefficients in Linear Regression or the weight vector w and bias b in a linear classifier.

* **Regression**. One of the primary applications of MVPA (together with classification). Regression is very similar to classification, but it aims to predict a continuous variable rather than a class label. For instance, in the ‘faces vs. houses' experiment, assume that the reaction time of the button press has been recorded, too. To investigate the question “Does the pattern of brain activity in each trial predict reaction time?,” regression can be performed using reaction time as responses.

* **Regression model**. An algorithm that performs regression, for instance Ridge Regression and Support Vector Regression (SVR).

* **Regularization**. A set of techniques that aim to reduce overfitting. Regularization is often directly incorporated into training by adding a penalty term to the loss function. For instance, L1 and L2 penalty terms are popular regularization techniques. They reduce overfitting by preventing coefficients from taking on too large values.

* **Response**. In regression, responses act as the target values that a model tries to predict. They play the same role that class labels play in classification. Unlike class labels, responses are continuous e.g., reaction time.

* **Searchlight analysis**. In neuroimaging analysis, a question such as “Does brain activity differentiate between faces and houses?” is usually less interesting than the question “Which brain regions differentiate between faces and houses?.” In other words, the goal of MVPA is to establish the presence of an effect and localize it in space or time. Searchlight analysis intends to marry statistical sensitivity with localizability. It is a well-established technique in the fMRI literature, where a searchlight is defined e.g., as a sphere of 1 cm radius, centered on a voxel in the brain (Kriegeskorte et al., 2006). All voxels within the radius serve as features for a classification or regression analysis. The result of the analysis is assigned to the central voxel. If the analysis is repeated for all voxel positions, the resultant 3D map of classification accuracies can be overlayed on a brain image. Brain regions that have discriminative information then light up as peaks in the map. Searchlight analysis is not limited to spatial coordinates. The same idea can be applied to other dimensions such as time points and frequencies.

* **Testing**. The process of applying a trained model to the test set. The performance of the model can then be quantified using a metric.

* **Test set**. Part of the data designated for testing. Like with training sets, test sets are automatically defined in cross-validation, or they can arise naturally in multi-site studies or in experiments with different phases.

* **Training**. The process of optimizing the parameters of a model using a training set.

* **Training set**. Part of the data designated for training. In cross-validation, a dataset is automatically split into training and test sets. In other cases, a training set may arise naturally. For instance, in experiments with different phases (e.g., memory encoding and memory retrieval) one phase may serve as training set and the other phase as test set. Another example is multi-site studies, where a model can be trained on data from one site and tested on data from another site.

* **Underfitting**. Occurs when a classifier or regression model is too simple to explain the data. For example, imagine a dataset wherein the optimal decision boundary is a circle, with samples of class 1 being inside the circle and samples of class 2 outside. A linear classifier is not able to represent a circular decision boundary, hence it will be unable to adequately solve the task. Underfitting can be checked by fitting a complex model (e.g., kernel SVM) to data. If the complex model performs much better than a more simple linear model (e.g., LDA) then it is likely that the simple model underfits the data. In most neuroimaging datasets, overfitting is more of a concern than underfitting.
