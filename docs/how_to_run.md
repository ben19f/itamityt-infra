

# download helm
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update


# Усстановка мастер ноды
curl -sfL https://get.k3s.io | sh -
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable=traefik" sh -
which k3s
k3s --version
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
export KUBECONFIG=~/.kube/config




# запуск сервера
sudo k3s server   \
    --tls-san 192.168.95.100   \
    --node-external-ip 192.168.95.100   \
    --bind-address 192.168.95.100   \
    --advertise-address 192.168.95.100   \
    --cluster-cidr 10.42.0.0/16   \
    --service-cidr 10.43.0.0/16


# установка ингресс поды
helm install ingress-nginx ingress-nginx/ingress-nginx \
    --namespace ingress-nginx --create-namespace \
    --set controller.replicaCount=1 \
    --set controller.nodeSelector."kubernetes\.io/hostname"=k3nhost \
    --set defaultBackend.nodeSelector."kubernetes\.io/hostname"=k3nhost


# получение токена для воркеров
sudo cat /var/lib/rancher/k3s/server/node-token

# Запуск агента на воркере
curl -sfL https://get.k3s.io | K3S_URL=https://YOUR_MASTER_IP:6443 \
K3S_TOKEN=TOKEN sh -



# создаем yaml конфигфайлы и применяем их на мастер ноде
sudo kubectl apply -f ingress.yaml




## работа с подами
# Список под
sudo kubectl get pod -o wide
# Смотри описание pod 
sudo kubectl describe pod backend-xxxxxxxxxx
# перезагрузить образ
sudo kubectl rollout restart deployment/redirect
sudo kubectl rollout restart deployment/<deployment-name> -n <namespace>
# зайти в поду
sudo kubectl exec -it frontend-6b7f7c5f4c-s6xwg -- sh


# ингресс поды
sudo kubectl get pods -A | grep -i ingress
sudo kubectl get deployments -n ingress-nginx
sudo kubectl get pods -n ingress-nginx -o wide
# получить переменные пода
sudo kubectl exec -it redirect-7496776fc6-q2pfk -- printenv
# сервисы поды
sudo kubectl describe svc backend-service
sudo kubectl get svc -n ingress-nginx
# получение нод
sudo kubectl get nodes

sudo k3s kubectl get nodes

# удаление
sudo /usr/local/bin/k3s-uninstall.sh
ыsudo  helm uninstall ingress-nginx -n ingress-nginx


# удаление конфига и пода
sudo kubectl delete -f old-deployment.yaml
=================



я удалил файл создания неймспейсов он в папке с секретами


ansibleadmin@k8s-master1:~/itamityt-infra$ kubectl apply -f ~/itamityt-secrets/.
namespace/devspaceita created
namespace/prodspaceita created
secret/projectsecrets created
Error from server (NotFound): error when creating "/home/ansibleadmin/itamityt-secrets/dev-secrets.yaml": namespaces "devspaceita" not found
ansibleadmin@k8s-master1:~/itamityt-infra$ kubectl apply -f ~/itamityt-secrets/.
secret/projectsecrets created
namespace/devspaceita unchanged
namespace/prodspaceita unchanged
secret/projectsecrets configured

~/itamityt-secrets


helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress \
  --create-namespace


  
helm install dev-release ./helm/itamityt -f values-dev.yaml