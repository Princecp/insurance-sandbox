Insurance Sandbox – Déploiement Kubernetes

# Présentation

Ce projet met en œuvre le déploiement d’une application web conteneurisée sur Kubernetes, avec exposition sécurisée via HTTPS et respect des bonnes pratiques d’infrastructure en environnement de production.
L’application est composée d’un frontend (interface utilisateur) et d’un backend (API), orchestrés sur Kubernetes et exposés via un contrôleur Ingress NGINX, avec une gestion automatique des certificats TLS grâce à cert-manager.

# Objectifs

Conteneuriser les composants applicatifs avec Docker
Déployer l’application sur Kubernetes
Exposer les services via Ingress
Sécuriser les communications en HTTPS (Let’s Encrypt)
Mettre en place une architecture structurée proche de la production


# Architecture

L’application adopte une architecture de type microservices simple :

Frontend : interface utilisateur
Backend : API exposant les endpoints /clients et /health

Flux de trafic
Client (navigateur)
   ↓
Ingress NGINX (HTTPS)
   ↓
Service Frontend (/)
   ↓
Service Backend (/api)
   ↓
Pods (conteneurs Docker)


# Composants principaux

Conteneurisation
Le frontend et le backend sont construits sous forme d’images Docker et stockés dans un registre privé (Scaleway).

# Ressources Kubernetes

Deployments : gestion du cycle de vie des applications
Services : communication interne entre composants
Ingress : exposition externe HTTP/HTTPS
Namespace : isolation des ressources


# Sécurité
La sécurisation des échanges est assurée par :

cert-manager
Let’s Encrypt

Les certificats TLS sont générés automatiquement et renouvelés sans intervention manuelle.

# Organisation du projet
# Structure alignée avec les standards:

k8s/
 ├── namespace.yaml
 ├── deployments/
 ├── services/
 ├── ingress/
 ├── cluster-issuer.yaml
 ├── limits/
 ├── quotas/
 ├── tests/


# Gestion des ressources
Namespaces
Permettent d’isoler les environnements et d’organiser les ressources.
Limits
Définissent les ressources CPU et mémoire allouées à chaque conteneur afin de garantir la stabilité.
Quotas
Imposent des limites globales au niveau du namespace afin de contrôler la consommation des ressources.

# Réseau

Un Ingress Controller NGINX est utilisé pour :

exposer l’application vers l’extérieur
router les requêtes selon les chemins
gérer la terminaison TLS

# Routage

/ → frontend
/api → backend


# Accès

Le projet utilise un DNS dynamique basé sur l’adresse IP du cluster :
https://<ip>.nip.io

Cela permet un accès public sans gestion de domaine dédiée.

# Processus de déploiement

Construction des images Docker
Push vers le registre
Définition des manifestes Kubernetes
Déploiement via kubectl
Exposition via Ingress
Génération automatique du certificat SSL


# Validation

Application accessible en HTTPS
Certificat SSL valide (Let’s Encrypt)
API fonctionnelle
Interface utilisateur accessible


# Bonnes pratiques mises en œuvre

Infrastructure as Code (manifests Kubernetes)
Images immuables
Gestion automatique des certificats
Isolation des environnements
Gouvernance des ressources (limits, quotas)
Séparation claire frontend / backend


# Conclusion
Ce projet démontre la mise en œuvre complète d’une application cloud-native sur Kubernetes, avec exposition sécurisée, gestion des ressources et organisation conforme aux standards d’un environnement d’entreprise.
Il illustre la capacité à concevoir, déployer et opérer une application dans une architecture moderne et scalable.
#################################################################################

# Après cluster on va déployer une application

# installer nginx ingress d'abord

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# Récupérer l'IP publique

kubectl get svc -n ingress-nginx

sudo nano /etc/hosts

EXTERNAL-IP insurance-sandbox.local

# Activer HTTPS (certificat)

# Installer cert-manager

kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml


# Télécharger Docker Desktop

https://www.docker.com/products/docker-desktop/

# clique sur

Download for Mac Apple silicon pour M1, 2, 3 ou M4

# Quand le fichier est téléchargé :

Ouvre le fichier .dmg
Glisse Docker.app dans : Applications

# Lancer Docker dans terminal

open /Applications/Docker.app

# Test

docker ps

# Création image backend:sandbox 

 docker build -t backend:sandbox ./backend

# forcer l’architecture compatible cluster (AMD64): erreur no match for platform

 docker buildx build --platform linux/amd64 -t backend:sandbox ./backend --load

 # Création image frontend:sandbox

docker build -t frontend:sandbox ./frontend

# forcer l’architecture compatible cluster (AMD64): erreur no match for platform

docker buildx build --platform linux/amd64 -t frontend:sandbox ./frontend --load

 # Tag des images

docker tag backend:sandbox rg.fr-par.scw.cloud/insurance-sandbox/backend:sandbox
docker tag frontend:sandbox rg.fr-par.scw.cloud/insurance-sandbox/frontend:sandbox

# Push vers Scaleway

docker push rg.fr-par.scw.cloud/insurance-sandbox/backend:sandbox
docker push rg.fr-par.scw.cloud/insurance-sandbox/frontend:sandbox

# Créer le secret registry pour récupérer les images dans scaleway

kubectl create secret docker-registry scw-registry-secret \
  --docker-server=rg.fr-par.scw.cloud \
  --docker-username=nologin \
  --docker-password="$SCW_SECRET_KEY" \
  --namespace=insurance-sandbox

# Ajouter le secret dans les deployments

spec:
  imagePullSecrets:
    - name: scw-registry-secret

# Déploiement Kubernetes

kubectl apply -f k8s/

# Vérifier les pods

kubectl get pods -n insurance-sandbox

# TEST Frontend

kubectl port-forward svc/insurance-frontend -n insurance-sandbox 8080:80

# ouvre navigateur :

http://localhost:8080

# TEST Backend

kubectl port-forward svc/insurance-backend -n insurance-sandbox 8081:80

curl http://localhost:8081/clients

# redémarrer tous les pods du deployment insurance-backend
# recréer les containers avec la dernière config/image
# appliquer les changements (env, image, secret…)

kubectl rollout restart deployment insurance-backend -n insurance-sandbox

kubectl rollout restart deployment insurance-frontend -n insurance-sandbox

**************************************************************************

# Consulter état nodes

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

# se connecter à ArgoCD récupérer mot de passe 

kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 -d

dTY-jkVsQ5Cdb8vZ%

# Créer repo dans

github.maif.io

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

# Corriger un commit invalide

git commit --amend --no-edit --reset-author

# Ajouter le repo distant

git remote add origin git@github.maif.io:prince-mbengue-adama/insurance-sandbox.git

# Définir la branche principale

git branch -M main

# Envoyer le code vers GitHub 

git push -u origin main

# Appliquer ton argocd

kubectl apply -f argocd-app.yaml

# Pour test local dans un terminal

kubectl port-forward svc/argocd-server -n argocd 8080:443

# Et

Recharger la page argocd

# Pour accéder à ArgoCD: https://argocd.51.158.74.49.nip.io sans kubectl port-forward

# Vérifie

kubectl get svc -n ingress-nginx

# prends

EXTERNAL-IP = 51.158.74.49

nano argocd-ingress.yaml

# Appliquer ton argocd-ingress

kubectl apply -f argocd-ingress.yaml

# Test ouvrir navigateur

https://argocd.51.158.74.49.nip.io

SelfSignedCert Blocked by SSL_SELF_SIGNED

# On ajoute un certificat réel

nano argocd-cert.yaml

# Appliquer ton argocd-cert

kubectl apply -f argocd-cert.yaml

# Modifier ingress pour HTTPS

nano argocd-ingress.yaml

# Ajouter

tls:
- hosts:
  - argocd.51.158.74.49.nip.io
  secretName: argocd-tls

# Appliquer

kubectl apply -f argocd-ingress.yaml

# Ouvrir navigateur 

https://argocd.51.158.74.49.nip.io

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


# Vérifier ton namespace app

kubectl get ns

# Appliquer ton namespace

kubectl apply -f k8s/namespace.yaml