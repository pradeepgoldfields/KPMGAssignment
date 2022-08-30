resource "aws_vpc" "three_tier_app_vpc" {
  cidr_block       = "${var.vpc_cidr}"
  instance_tenancy = "default" //will lead to shared tenancy, we are not using dedicated or dedicated host for this example.
  tags = {
    type = "wordpress application vpc"
  }
}
#internet gateway
resource "aws_internet_gateway" "igy" {
  vpc_id = "${aws_vpc.three_tier_app_vpc.id}"
}

# dhcp
resource "aws_vpc_dhcp_options" "dns_resolver" {
  domain_name_servers = ["AmazonProvidedDNS"]
}

# associate dhcp with vpc
resource "aws_vpc_dhcp_options_association" "dns_resolver" {
  vpc_id          = "${aws_vpc.three_tier_app_vpc.id}"
  dhcp_options_id = "${aws_vpc_dhcp_options.dns_resolver.id}"
}

# Elastic-IP (eip) for NAT
resource "aws_eip" "nat_eip" {
  vpc        = true
  depends_on = [aws_internet_gateway.igy]
}

# NAT
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet_1.id
  depends_on = [aws_subnet.public_subnet_1]
}

# will have 2 public subnets in different AZs for ASG
# we can have count to create subnets that will use element(x, count.index) of cidr list and AZ list to create subnet in a scalable way.
resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = "${aws_vpc.three_tier_app_vpc.id}"
  cidr_block             = "${var.pub_web1_cidr}"
  map_public_ip_on_launch = true
  availability_zone = "eu-west-1a"

}

resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = "${aws_vpc.three_tier_app_vpc.id}"
  cidr_block             = "${var.pub_web2_cidr}"
  map_public_ip_on_launch = true
  availability_zone = "eu-west-1b"
}

# will have 2 private subnets in different AZs for ASG
resource "aws_subnet" "private_subnet_1" {
  vpc_id                  = "${aws_vpc.three_tier_app_vpc.id}"
  cidr_block             = "${var.priv_app1_cidr}"
  map_public_ip_on_launch = false
  availability_zone = "eu-west-1a"

  tags = {
    type = "wordpress application private subnet"
  }
}

resource "aws_subnet" "private_subnet-2" {
  vpc_id                  = "${aws_vpc.three_tier_app_vpc.id}"
  cidr_block             = "${var.priv_app2_cidr}"
  map_public_ip_on_launch = false
  availability_zone = "eu-west-1b"

  tags = {
    type = "wordpress application private subnet"
  }
}

# will have 2 DB subnets in different AZs for ASG
resource "aws_subnet" "database_subnet_1" {
  vpc_id            = "${aws_vpc.three_tier_app_vpc.id}"
  cidr_block        = "${var.priv_db1_cidr}"
  availability_zone = "eu-west-1a"

  tags = {
    type = "wordpress application db subnet"
  }
}

resource "aws_subnet" "database_subnet_2" {
  vpc_id            = "${aws_vpc.three_tier_app_vpc.id}"
  cidr_block        = "${var.priv_db2_cidr}"
  availability_zone = "eu-west-1b"

  tags = {
    type = "wordpress application db subnet"
  }
}


#creating route tables and linking them to subnets
resource "aws_route_table" "public_route_table" {
  vpc_id = "${aws_vpc.three_tier_app_vpc.id}"
route {
      cidr_block = "0.0.0.0/0" //route all traffic to and from internet through igy
      gateway_id = "${aws_internet_gateway.igy.id}"
  }
}

resource "aws_route_table" "private_route_table" {
  vpc_id = "${aws_vpc.three_tier_app_vpc.id}"
route {
      cidr_block = "0.0.0.0/0" //route all traffic to and from internet through igy
      nat_gateway_id = "${aws_nat_gateway.nat.id}"
  }
}

resource "aws_route_table_association" "rt1" {
  subnet_id = "${aws_subnet.public_subnet_1.id}"
  route_table_id = "${aws_route_table.public_route_table.id}"
}

resource "aws_route_table_association" "rt2" {
  subnet_id = "${aws_subnet.public_subnet_2.id}"
  route_table_id = "${aws_route_table.public_route_table.id}"
}

resource "aws_route_table_association" "rt3" {
  subnet_id = "${aws_subnet.database_subnet_1.id}"
  route_table_id = "${aws_route_table.private_route_table.id}"
}

resource "aws_route_table_association" "rt4" {
  subnet_id = "${aws_subnet.database_subnet_2.id}"
  route_table_id = "${aws_route_table.private_route_table.id}"
}

