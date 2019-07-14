GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: all
all: deploy

.PHONY: create-cluster
create-cluster:
	gcloud container clusters create facepredictor \
		--scopes "cloud-platform" \
		--num-nodes 2
	gcloud container clusters get-credentials facepredictor

.PHONY: build
build:
	docker build -t gcr.io/$(GCLOUD_PROJECT)/facepredictor-frontend ./nginx/
	docker build -t gcr.io/$(GCLOUD_PROJECT)/facepredictor-worker ./worker/

.PHONY: push
push: build
	gcloud docker -- push gcr.io/$(GCLOUD_PROJECT)/facepredictor-frontend
	gcloud docker -- push gcr.io/$(GCLOUD_PROJECT)/facepredictor-worker

.PHONY: create-service
create-service:
	kubectl create -f facepredictor-service.yaml

.PHONY: create-deploy
create-deploy: push
	kubectl create -f facepredictor-deploy.yaml

.PHONY: deploy
deploy: create-deploy create-service

.PHONY: delete
delete:
	-kubectl delete -f facepredictor-deploy.yaml
	-kubectl delete -f facepredictor-service.yaml
