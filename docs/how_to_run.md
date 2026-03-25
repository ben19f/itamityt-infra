

# усстановка helm
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

# получение токена для воркеров
sudo cat /var/lib/rancher/k3s/server/node-token

# Запуск агента на воркере
curl -sfL https://get.k3s.io | K3S_URL=https://YOUR_MASTER_IP:6443 \
K3S_TOKEN=TOKEN sh -


