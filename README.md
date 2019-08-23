# Taming the AI DevOps Pipeline

Operationalizing AI models has its challenges.  Many organizations have successfully delivered AI proofs of concept and taken the next step to operationalize machine learning models only to find that very complex. Organizations are looking for guidance on a seamless handoff of the AI model from development to production and on the management of its lifecycle – essentially continuous integration / continuous delivery for AI. This hands-on workshop offers some practical experience of applying DevOps techniques to AI models, with the goal of building and deploying an automated AI pipeline.
This workshop will use Azure DevOps, Azure Machine Learning Services, and assumes knowledge of python.

## Key Take-aways

- A technique for applying CI/CD to AI models
- Implement a CI/CD pipeline

## Pre-Requisites

- An active Azure subscription  
- At least contributor role access to the Azure subscription
- Access to an Azure DevOps account
- With contributor level access, create a service principal in the Azure portal (see *MandatoryLabPreReq* document in this repository)
- Assign contributor role access to the service principal. A service principal and credentials will be used for authentication within the AML pipelines. Because a service principal is created outside of the subscription (in Azure Active Directory), in order to use it for AML Pipelines, the service principal needs to be assigned to a contributor role within the Azure subscription (see *MandatoryLabPreReq* document in this repository).   

## Agenda

| Time          | Topic                                                       |
| ------------- | ----------------------------------------------------------- |
| 8:30 - 9:00   | Breakfast & Registration                                    |
| 9:00 - 10:00  | Session: Overview of AML Pipelines                          |
| 10:00 - 11:00 | Session: Intro to Lifecycle Mgt with Azure DevOps/YAML      |
| 11:00 - 12:00 | Session: YAML and AML pipeline integration                  |
| 12:00 – 1:00  | Lunch / Group Discussion                                    |                                
| 1:00 – 3:30   | Lab: Implement a build, retrain, and deployment pipeline    |
| 3:30 - 4:00   | Wrap-up                                                     |

