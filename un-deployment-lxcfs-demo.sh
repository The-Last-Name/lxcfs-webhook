kubectl delete -f ./deploy/lxcfs-demo-deploy.yaml
kubectl delete -f ./deploy/lxcfs-demo-svc.yaml
kubectl delete -f ./deploy/lxcfs-demo-mwc-patched.yaml
kubectl delete cm lxcfs-demo-cm
kubectl delete CertificateSigningRequest lxcfs-demo-svc.default
kubectl delete secret lxcfs-demo-certs
kubectl delete -f ./deploy/lxcfs.yaml
