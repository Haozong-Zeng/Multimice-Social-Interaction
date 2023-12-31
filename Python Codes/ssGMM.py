"""
Created on August 12, 2019
@author: mwdunham
Tested with Python versions: 3.6.6 - 3.7.3

SEMI-SUPERVISED GAUSSIAN MIXTURE MODELS (ssGMM)
	This code is based on the implementation given by:
		@Article{Yan_2017,
		  author   = {Yan, H. and Zhou, J. and Pang, C. K.},
		  title    = {Gaussian mixture model using semisupervised learning for probabilistic fault diagnosis under new data categories},
		  journal  = {IEEE Transactions on Instrumentation and Measurement},
		  year     = {2017},
		  volume   = {66},
		  number   = {4},
		  pages    = {723-733},
		  doi      = {10.1109/TIM.2017.2654552},
		  file     = {:Papers\\Yan et al. (2017) - GMM using semi-supervised learning for probabilistic fault diagnosis.pdf:PDF},
		  keywords = {semi-supervised, ssGMM, machine fault diagnosis}}
"""
# NOTE: A test-train-split of the data needs to be performed before calling this function

#Information regarding INPUTS:
    # Xtrain: Training data features (d-dimensional)
    # ytrain: Training data labels 
    # Xtest: Testing data features (d-dimensional)
    # ytest: Testing data labels
    # beta: tradeoff parameter between unlabeled and labeled data. Must be (0 < beta < 1). beta = 1 is equivalent to 100% supervised, beta = 0 is equivalent to 100% unsupervised
    # tol: the tolerance for the ssGMM objective function; it represents the 'percent' change in the objective function. If you wish the algorithm to stop once the obj is only changing by <=1%, then tol=1.0
	# max_iterations: maximum number of iterations to perform for optimzing the ssGMM objective function
    # early_stop: a boolean variable, i.e. 'True' or 'False'. 
        ## if 'True': at any given iteration, if the ssGMM objective function becomes smaller (worse), the algorithm will stop and will use the information recovered from the PREVIOUS iteration   
        ## if 'False': the code will run until the tol or max_iterations is reached

#Information regarding OUTPUTS (given by return statement at the bottom):
    # GMM_label_pred: thresholded predictions for each unlabeled data point derived from the GAMMA matrix
    # GAMMA[L:(L+U),:]: probability matrix for each unlabeled data point belonging to each class, size = (len(U), K)
    # Objective: array containing the value of the objective function at each iteration, the first entry is the starting value of the objective function prior to using the EM algorithm

def ss_GaussianMixtureModels(Xtrain, ytrain, Xtest, beta, tol, max_iterations, early_stop):
    cond_tolerance = 1E-15 ##the cutoff for singular values - the default for pinv is 1E-15 which was discovered to be too low through testing
    
    from sklearn.metrics import accuracy_score
    import numpy as np
    from scipy.stats import pearsonr
    from itertools import product
    
    
    ## Custom designed Gaussian Naive Bayes classifier that outputs pi, mu, sigma
    def Bayes(X, y):
        (n, d) = np.shape(X)
        uniq = np.unique(y)
        ####################################################################
        ####          SOLVING FOR THE CLASS PRIOR PROBABILITY          #####
        ####################################################################
        pi = []
        for j in uniq:
            sum = 0
            for i in range(0,n,1):
                if y[i] == j:
                    sum += 1
            pi.append(sum/n)     
        
        ####################################################################
        ####       SOLVING FOR THE CLASS SPECIFIC GAUSSIAN MEAN         ####
        ####################################################################
        mu_y = np.zeros((len(uniq),d))
        for j in range(0,len(uniq),1):
            sum = 0
            counter = 0
            for i in range(0,n,1):
                if np.mean(y[i]) == np.mean(uniq[j]):
                    sum = sum + X[i,:]
                    counter += 1
            mu_y[j,:] = (1/counter)*sum
        
        ####################################################################
        ####     SOLVING FOR THE CLASS SPECIFIC GAUSSAIN COVARIANCE    #####
        ####################################################################
        sigma_dic = {}
        for i in uniq:
            sigma_dic["SIGMA_K_" + str(i)] = np.eye(d)
        #Access an entry in the dictionary using a string key as follows:
        #sigma_ID = "SIGMA_K_" + str(j)
        #sigma_dic[sigma_ID]
        
        for j in range(0,len(uniq),1):
            sum = 0
            counter = 0
            sigma_ID = "SIGMA_K_" + str(uniq[j])
            for i in range(0,n,1):
                if y[i] == uniq[j]:
                    sum = sum + np.outer(np.transpose(X[i,:] - mu_y[j,:]),(X[i,:] - mu_y[j,:]))
                    counter += 1
            sigma_dic[sigma_ID] = (1/counter)*sum
    
        return pi, mu_y, sigma_dic
    
    ###########################################################################
    ###########################################################################
    
    ##########################
    #### Data preparation ####
    ##########################
    
    L = np.size(ytrain) #%%% EQUATION 1 %%%#
    uniq = np.unique(ytrain)
    K = len(uniq) # The number of classes
    uniq = uniq.tolist()
    Xtrain = np.hstack((Xtrain, np.ones((L,1))))
    U = np.size(Xtest[:,0]) #%%% EQUATION 2 %%%#
    print('Number of labeled data: ' + str(L))
    print('Number of unlabeled data: ' + str(U))
    # initialize corr of Xtest with the centers
    Xtest = np.hstack((Xtest, np.ones((U,1))))
    D = np.vstack((Xtrain, Xtest)) #%%% EQUATION 4 %%%#
    (n, d) = np.shape(D)
    
    # ssGMM needs starting values for the Gaussian means & covariances for each class, so a Bayes classifier on the LABELED data is used to determine these
    pi, mu, sigma = Bayes(Xtrain, ytrain) #%%% EQUATION 8 %%%#
    
    
    #### Using a limited number of training data can cause the covariance matrices of the resulting classes 
    #### to be singular. The code below uses an SVD decomposition to compute the determinant and the inverse
    #### of the covariance matrices. These are needed to compute probability density function. 
    sigma_inv = {}
    det_sigma = []
    
    for j in range(0,len(uniq),1):
        sigma_ID = "SIGMA_K_" + str(uniq[j])
        
        [u, s, v] = np.linalg.svd(sigma[sigma_ID])
        rank = len(s[s > cond_tolerance])
        det_sigma.append(np.prod(s[:rank]))
        try:
        # Code that will (maybe) throw an exception
            sigma_inv[sigma_ID] = np.linalg.pinv(sigma[sigma_ID], rcond = cond_tolerance)
            #det_sigma.append(np.linalg.det(sigma[sigma_ID]))
        except np.linalg.LinAlgError:
            print("The covariance matrix associated with Class " + str(uniq[j]) + " is still SINGULAR")
            sigma_inv[sigma_ID] = np.linalg.inv(sigma[sigma_ID], rcond = cond_tolerance)
        except:
            print("Unexpected error")
            raise 
                
    ###########################################################################            
    #########   MULTI-VARIATE GAUSSIAN PROBABILITY DENSITY FUNCTION   #########
    ###########################################################################
    # For the EM algorithm below, the objective function has to be computed MANY times, and the built in function (scipy.stats.multivariate_normal.pdf) recomputes the covariance matrix inverses/determinants, which is computationally inefficient.
    # This function below incorporates the pre-computed covariance matrix inverses and covariance determinants, and this drastically improves the computation time (5-6x faster)
    
    def gaussian_PDF(x,mu,sigma,det_sigma,sigma_inv):
        return (1/np.sqrt((2*np.pi)**(d)*det_sigma))*np.exp(-0.5*np.matmul((x-mu).T, np.matmul(sigma_inv, (x-mu))))
        
    ###########################################################################
    ###################   OBJECTIVE FUNCTION FOR ssGMM   ######################
    ###################            Equation 7            ######################
    ###########################################################################

    def objective_func(L, U, D, ytrain, pi, mu, sigma, det_sigma, sigma_inv): 
        sum_label = 0
        ## FOR THE LABELED PART OF THE OBJECTIVE FUNCTION
        for i in range(0,L,1):
            sigma_ID = "SIGMA_K_" + str(int(ytrain[i]))
            ind = uniq.index(ytrain[i])
            sum_label = sum_label + np.log(pi[ind]*gaussian_PDF(D[i,:], mu[ind,:], sigma[sigma_ID], det_sigma[ind], sigma_inv[sigma_ID]))

        ## FOR THE UNLABELED PART OF THE OBJECTIVE FUNCTION     
        sum_noLabel = 0
        for i in range(L,L+U,1):
            inner_sum = 0
            for j in range(0,len(uniq),1):
                sigma_ID = "SIGMA_K_" + str(uniq[j])
                inner_sum = inner_sum + pi[j]*gaussian_PDF(D[i,:], mu[j,:], sigma[sigma_ID], det_sigma[j], sigma_inv[sigma_ID])
            sum_noLabel = sum_noLabel + np.log(inner_sum)

        return beta*sum_label + (1-beta)*sum_noLabel
    
    Objective = []
    # This is the starting objective function value
    Objective.append(objective_func(L, U, D, ytrain, pi, mu, sigma, det_sigma, sigma_inv))    
    
    GAMMA = np.zeros((n,K))
    obj_change = tol + 1
    t = 0
    
    ###########################################################################
    ####### Solving for the soft labels on unalabeled data using EM ###########
    ###########################################################################
    while (obj_change > tol):
        
        GAMMA_old = np.array(GAMMA) # Saving the previous GAMMA 
        
        ##########################
        ######## E-STEP ##########
        ##########################
        for i in range(0,n,1):
        #%%% EQUATION 9 %%%#
            ## For LABELED instances
            if i < L:
                for j in range(0,len(uniq),1):
                    if ytrain[i] == uniq[j]:
                        GAMMA[i,j] = 1.0
            
            ## For UNLABELED instances
            else:
                sum = 0
                for j in range(0,len(uniq),1):
                    sigma_ID = "SIGMA_K_" + str(uniq[j])
                    GAMMA[i,j] = pi[j]*gaussian_PDF(D[i,:], mu[j,:], sigma[sigma_ID], det_sigma[j], sigma_inv[sigma_ID])
                    sum = sum + GAMMA[i,j]
                GAMMA[i,:] = (1/sum)*GAMMA[i,:]
        
        
        ##########################
        ######## M-STEP ##########
        ##########################
        
        for j in range(0,len(uniq),1):
        #%%% EQUATIONS FROM STEP 3 %%%#    
            nl = 0
            nu = 0
            for i in range(0,L,1):
                nl = nl + GAMMA[i,j]
            for i in range(L,L+U,1):
                nu = nu + GAMMA[i,j]
            C = (beta*nl + (1-beta)*nu) #this is a factor that is common in each of the three parameters below

            #### Updating the cluster prior probabilities, pi ####          
            pi[j] = (C)/(beta*L + (1-beta)*U)
            
            #### Updating the cluster means, mu ####
            mean_sumL = 0
            mean_sumU = 0
            for i in range(0,L,1):
                mean_sumL = mean_sumL + GAMMA[i,j]*D[i,:]
            for i in range(L,L+U,1):
                mean_sumU = mean_sumU + GAMMA[i,j]*D[i,:]       
            mu[j,:] = (beta*mean_sumL + (1-beta)*mean_sumU)/(C)
            
            #### Updating the cluster covariance matrices, sigma ####
            sigma_ID = "SIGMA_K_" + str(uniq[j])
            
            sigma_sumL = 0
            sigma_sumU = 0
            for i in range(0,L,1):
                sigma_sumL = sigma_sumL + GAMMA[i,j]*np.outer(np.transpose(D[i,:] - mu[j,:]),(D[i,:] - mu[j,:]))
            for i in range(L,L+U,1):
                sigma_sumU = sigma_sumU + GAMMA[i,j]*np.outer(np.transpose(D[i,:] - mu[j,:]),(D[i,:] - mu[j,:]))
            
            sigma[sigma_ID] = (beta*sigma_sumL + (1-beta)*sigma_sumU)/(C)
            
            #### Updating the covariance matrix determinants and covariance inverses ####
            try: # Code that will (maybe) throw an exception
                sigma_inv[sigma_ID] = np.linalg.pinv(sigma[sigma_ID], rcond = cond_tolerance)
                [u, s, v] = np.linalg.svd(sigma[sigma_ID])
                rank = len(s[s>cond_tolerance])
                det_sigma[j] = np.prod(s[:rank])
            except np.linalg.LinAlgError:
                #print("The covariance matrix associated with Class " + str(uniq[j]) + " has singular values, so its determinant and inverse has issues")
                sigma_inv[sigma_ID] = np.linalg.inv(sigma[sigma_ID])
            except:
                print("Unexpected error")
                raise 
            
            
        ##############################################################
        ######## Compute Objective Function: Log-likelihood ##########
        ##############################################################
        
        Objective.append(objective_func(L, U, D, ytrain, pi, mu, sigma, det_sigma, sigma_inv))        
        
        ## The early stopping criteria
        if early_stop == 'True': 
            if (Objective[t] - Objective[t+1]) > 0:
                print('Objective function is INCREASING... stopping early and using the GAMMA from the previous iteration')
                GAMMA = np.array(GAMMA_old)
                break
        
        obj_change = abs((Objective[t+1] - Objective[t])/(Objective[t]))*100
        t = t + 1
        
        if t == max_iterations:
            print("Max number of iterations reached")
            break
       
    #print("The number of iterations used: ", t)   
    #print("The objective function: \n", Objective)
    
    ## Using a threshold to assign labels to the unlabeled points with the highest probability
    GMM_label_pred = np.ones(U)*99.99
    k = 0
    for i in range(L,L+U,1):
        #%%% EQUATION 10 %%%#
        cl = GAMMA[i,:].argmax()
        GMM_label_pred[k] = uniq[cl]
        k = k + 1
        
    #semi_GMM_accuracy = accuracy_score(ytest, GMM_label_pred)
    #print("Standard accuracy metric of Semi-supervised GMM using beta = " + str(beta) + ", and tol = " + str(tol) + ": " + str(semi_GMM_accuracy))
    #miss_class_points = accuracy_score(ytest, GMM_label_pred, normalize=False)
    #print("Number of misclassified points: " + str(U - miss_class_points) + "/" + str(U))
    #print("")
    
    return [GMM_label_pred, GAMMA[L:(L+U),:], Objective]