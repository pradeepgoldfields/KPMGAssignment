# using a bitnami helm chart to setp wordpress

provider "helm" {
  kubernetes {
	config_path = pathexpand(var.kube_config)
  }
}

provider "kubernetes" {
  config_path = pathexpand(var.kube_config)
}

resource "helm_release" "wordpress" {
  name       = "my_release_wordpress"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "wordpress"
  version    = "15.1.3"
}