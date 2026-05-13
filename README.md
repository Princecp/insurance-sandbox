##############################################################
# Insurance Sandbox – Déploiement Kubernetes #
##############################################################

# Description :

# Cette procédure met en place une architecture complète basée sur Kubernetes et GitOps.

# Elle inclut :
# - Installation de l’infrastructure (Ingress, cert-manager, ArgoCD)
# - Configuration TLS automatique (Let’s Encrypt)
# - Déploiement d’une application via ArgoCD
# - Utilisation de Git comme source de vérité

# Workflow final :
# Build Docker → Push registry → Push Git → ArgoCD déploie automatiquement

# IMPORTANT :
# - Ne pas utiliser kubectl apply pour les ressources applicatives (k8s/*
# - ArgoCD gère tout après application du fichier application.yaml
#####################################################################################

# Vérifier le cluster

kubectl get nodes

# Installer helm

brew install helm

# Ajouter les repos Helm essentiels

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm repo add jetstack https://charts.jetstack.io

helm repo add argo https://argoproj.github.io/argo-helm

helm repo add external-secrets https://charts.external-secrets.io

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo add grafana https://grafana.github.io/helm-charts

# Mettre à jour

helm repo update

# Installer ingress-nginx

helm install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace

#  Vérifier que ingress est prêt

kubectl get pods -n ingress-nginx

# récupérer IP publique

kubectl get svc -n ingress-nginx

EXTERNAL-IP 
51.158.74.49 

# Installer cert-manager

helm install cert-manager jetstack/cert-manager \
  -n cert-manager --create-namespace \
  --set installCRDs=true

# vérifier

kubectl get pods -n cert-manager

# Appliquer ton ClusterIssuer

kubectl apply -f k8s/cluster-issuer.yaml

# Installer ARGO CD

helm install argocd argo/argo-cd \
  -n argocd --create-namespace

# Accéder à ArgoCD

kubectl port-forward svc/argocd-server -n argocd 8080:443

# Dans un navigateur

https://localhost:8080/

# Se connecter à ArgoCD récupérer mot de passe 

kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 -d

Exemple: dTY-jkVsQ5Cdb8vZ%

# Installer ArgoCD CLI

brew install argocd

# Créer repo dans

github.com

# Initialiser le repo local

cd insurance-sandbox

git init

# Ajouter les fichiers au suivi Git

git add .

# Faire un commit

git commit -m "k8s + app"

# Configurer ton identité Git

git config --global user.name "MBENGUE ADAMA Prince"

git config --global user.email "prenom.nom@maif.fr"

# Ajouter le repo distant

git remote add origin git@github.com/Princecp/insurance-sandbox.git

# Définir la branche principale

git branch -M main

# Envoyer le code vers GitHub 

git push -u origin main

# Télécharger Docker Desktop si pas fait

https://www.docker.com/products/docker-desktop/

# clique sur

Download for Mac Apple silicon pour M1, 2, 3 ou M4

# Quand le fichier est téléchargé :

Ouvre le fichier .dmg

Glisse Docker.app dans : Applications

# Sinon:

# Lancer Docker dans terminal

open /Applications/Docker.app

# Test

docker ps

cd insurance-sandbox 

# forcer l’architecture compatible cluster (AMD64): erreur no match for platform

 docker buildx build --platform linux/amd64 -t backend:sandbox ./backend --load

# forcer l’architecture compatible cluster (AMD64): erreur no match for platform

docker buildx build --platform linux/amd64 -t frontend:sandbox ./frontend --load

 # Tag des images

docker tag backend:sandbox rg.fr-par.scw.cloud/insurance-sandbox/backend:sandbox

docker tag frontend:sandbox rg.fr-par.scw.cloud/insurance-sandbox/frontend:sandbox

# Push vers Scaleway

docker push rg.fr-par.scw.cloud/insurance-sandbox/backend:sandbox

docker push rg.fr-par.scw.cloud/insurance-sandbox/frontend:sandbox

# Créer un repo github.com à partir du lien suivant

Création d'un compte Github.com - Cloud Platform Public - Azure

# Vérifier état des fichiers

git status

# Ajouter modifications

git add .

# Commit

git commit -m "update docker images"

# Envoyer vers GitHub

git push origin main

# Appliquer ton argocd

cd insurance-sandbox/argocd

kubectl apply -f application.yaml

# Pour accéder à ArgoCD: https://argocd.51.158.74.49.nip.io sans kubectl port-forward

# Test ouvrir navigateur

https://argocd.51.158.74.49.nip.io

# Ajouter le repository GitHub (source GitOps) si privé

argocd repo add https://github.com/Princecp/insurance-sandbox.git

# Afficher tous les pods du ns

kubectl get pods -n insurance-sandbox

# Vérifier que les pods ArgoCD sont en fonctionnement

kubectl get pods -n argocd

# Vérifier application ArgoCD

argocd app get insurance

# Vérifier ton namespace app

kubectl get ns