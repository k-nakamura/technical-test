GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: all
all: deploy

.PHONY: create-cluster
create-cluster:
	gcloud container clusters create facepredictor \
		--scopes "cloud-platform" \
		--num-nodes 2
	gcloud container clusters get-credentials facepredictor

.PHONY: create-bucket
create-bucket:
	gsutil mb gs://$(GCLOUD_PROJECT)
    gsutil defacl set public-read gs://$(GCLOUD_PROJECT)

.PHONY: build
build:
	docker build -t gcr.io/$(GCLOUD_PROJECT)/facepredictor .

.PHONY: push
push: build
	gcloud docker -- push gcr.io/$(GCLOUD_PROJECT)/facepredictor

.PHONY: template
template:
	sed -i ".tmpl" "s/\[GCLOUD_PROJECT\]/$(GCLOUD_PROJECT)/g" facepredictor-frontend.yaml

.PHONY: create-service
create-service:
	kubectl create -f facepredictor-service.yaml

.PHONY: deploy-frontend
deploy-frontend: push template
	kubectl create -f facepredictor-frontend.yaml

.PHONY: deploy
deploy: deploy-frontend create-service

.PHONY: delete
delete:
	-kubectl delete -f facepredictor-service.yaml
	-kubectl delete -f facepredictor-frontend.yaml
