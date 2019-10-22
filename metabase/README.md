# install helm from binary

    helm init --wait
    # helm install --name my-release stable/metabase
    # without further configure backend will be lost
    # https://github.com/helm/charts/blob/master/stable/metabase/values.yaml
    helm del --purge my-release
    helm install --name my-release -f metabase-config.yaml stable/metabase
