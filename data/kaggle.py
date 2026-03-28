import kaggle

kaggle.api.authenticate()

kaggle.api.dataset_download_files('yashdevladdha/uber-ride-analytics-dashboard', path='.', unzip=True)

