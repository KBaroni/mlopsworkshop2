docker run -v $(System.DefaultWorkingDirectory)/_ci-build/mlops-pipelines/ml_service/pipelines:/pipelines \

-w=\pipelines -e MODEL_NAME=$MODEL_NAME -e EXPERIMENT_NAME=$EXPERIMENT_NAME \

-e TENANT_ID=$TENANT_ID -e SP_APP_ID=$SP_APP_ID -e SP_APP_SECRET=$(SP_APP_SECRET) \
mcr.microsoft.com/mlops/python:latest python run_train_pipeline.py
