resource "aws_alb" "alb" {
  subnets = ["${aws_subnet.public_subnet_1.id}", "${aws_subnet.public_subnet_2.id}"]
  internal = false
  security_groups = ["${aws_security_group.WebSg.id}"]
  
  depends_on = [aws_internet_gateway.igy, 
  aws_vpc_dhcp_options_association.dns_resolver]
}

resource "aws_alb_target_group" "alb_target" {
  port = 8080
  protocol = "HTTP"
  vpc_id = "${aws_vpc.three_tier_app_vpc.id}"
  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    path                = "/"
    interval            = 30
    port                = 80
    matcher             = "200-399"
  }
  stickiness {
    type = "lb_cookie"
    enabled = true
  }

  depends_on = [
    aws_alb.alb
  ]
}

resource "aws_alb_target_group_attachment" "attach_web1" {
  target_group_arn = "${aws_alb_target_group.alb_target.arn}"
  target_id = aws_instance.web_instance_1.id
  port = 80

  depends_on = [
    aws_alb.alb,
    aws_alb_target_group.alb_target
  ]
}
resource "aws_alb_target_group_attachment" "attach_web2" {
  target_group_arn = "${aws_alb_target_group.alb_target.arn}"
  target_id = aws_instance.web_instance_2.id
  port = 80
  depends_on = [
    aws_alb.alb,
    aws_alb_target_group.alb_target
  ]
}

resource "aws_lb_listener" "external_elb" {
  load_balancer_arn = aws_alb.alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.alb_target.arn
  }
  depends_on = [
    aws_alb.alb,
    aws_alb_target_group.alb_target,
    aws_alb_target_group_attachment.attach_web1,
    aws_alb_target_group_attachment.attach_web2
  ]
}