# class B cidr for vpc
variable "vpc_cidr" {
  default = "10.0.0.0/16"
}
# class C cidr for subnets
variable "pub_web1_cidr" {
  default = "10.0.1.0/24"
}
variable "pub_web2_cidr" {
  default = "10.0.2.0/24"
}
variable "priv_app1_cidr" {
  default = "10.0.3.0/24"
}
variable "priv_app2_cidr" {
  default = "10.0.4.0/24"
}
variable "priv_db1_cidr" {
  default = "10.0.5.0/24"
}
variable "priv_db2_cidr" {
  default = "10.0.6.0/24"
}