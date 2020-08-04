# lxcfs-webhook
NOTE: Initializers has been deprecated in Kubernetes 1.14
Please use the version with Admission Webhook in https://v1-18.docs.kubernetes.io/docs/reference/access-authn-authz/webhook/

### Deploy Demo
```
Login required K8s Master 
# git clone git@github.com:The-Last-Name/lxcfs-webhook.git
# bash deployment-lxcfs-demo.sh
```

### Test
```
# kubectl label ns test1 easyk8s.cn/demo=enabled
# kubectl create -f test/deployment.yaml -n test1
# kubectl exec -n test1 -it <pod-name> bash
free -h
```

### undeploy
```
# bash un-deployment-lxcfs-demo.sh
```
