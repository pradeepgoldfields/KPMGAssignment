#web servers
resource "aws_instance" "web_instance_1" {
  ami                         = "ami-09e2d756e7d78558d"
  instance_type               = "t2.micro"
  vpc_security_group_ids      = ["${aws_security_group.WebSg.id}"]
  subnet_id                   = "${aws_subnet.public_subnet_1.id}"
  associate_public_ip_address = true
  user_data                   = "${file("data.sh")}"
}

# Creating 2nd EC2 instance in Public Subnet
resource "aws_instance" "web_instance_2" {
  ami                         = "ami-09e2d756e7d78558d"
  instance_type               = "t2.micro"
  vpc_security_group_ids      = ["${aws_security_group.WebSg.id}"]
  subnet_id                   = "${aws_subnet.public_subnet_2.id}"
  associate_public_ip_address = true
  user_data                   = "${file("data.sh")}"    
}