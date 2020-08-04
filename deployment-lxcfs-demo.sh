kubectl apply -f ./deploy/lxcfs.yaml

chmod +x ./deploy/*
./deploy/webhook-ssl-cert-gen.sh --service lxcfs-demo-svc --secret lxcfs-demo-certs --namespace default
cat ./deploy/lxcfs-demo-mwc.yaml | ./deploy/webhook-patch-ca-bundle.sh > ./deploy/lxcfs-demo-mwc-patched.yaml
kubectl create cm lxcfs-demo-cm --from-file=script=./app/lxcfs-demo.py

kubectl apply -f ./deploy/lxcfs-demo-deploy.yaml
kubectl apply -f ./deploy/lxcfs-demo-svc.yaml
kubectl apply -f ./deploy/lxcfs-demo-mwc-patched.yaml
