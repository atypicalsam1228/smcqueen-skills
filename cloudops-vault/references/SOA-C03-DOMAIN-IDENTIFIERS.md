# SOA-C03 Domain Identifiers

Use this reference to map content to the correct Sources/ subdirectory.

## Domain 1 — Monitoring, Logging, and Remediation (22%)
**Directory:** `Sources/Monitoring-Logging/`

Keywords: CloudWatch, metrics, alarms, composite alarm, Logs Insights, X-Ray, tracing, CloudTrail, EventBridge, SSM Automation, runbook, remediation, Container Insights, metric filter, log group, dashboard, monitoring, observability, alert fatigue, PII redaction, data protection policy

Key services: CloudWatch, X-Ray, CloudTrail, EventBridge, SSM Automation, Compute Optimizer, Trusted Advisor (cost/performance angle)

## Domain 2 — Reliability and Business Continuity (22%)
**Directory:** `Sources/Reliability/`

Keywords: Auto Scaling, ASG, scaling policy, step scaling, warm-up, SQS decoupling, Multi-AZ, Multi-Region, RDS failover, Aurora replica, DynamoDB Global Tables, backup, restore, AWS Backup, DLM, snapshot, S3 versioning, CRR, cross-region replication, disaster recovery, RPO, RTO, pilot light, warm standby, active-active, Route 53 health check, calculated health check, FSx, failover, high availability, fault tolerance, resilience

Key services: EC2 Auto Scaling, SQS, RDS, Aurora, DynamoDB, AWS Backup, DLM, S3, Route 53, FSx

## Domain 3 — Deployment, Provisioning, and Automation (22%)
**Directory:** `Sources/Deployment-Automation/`

Keywords: CloudFormation, CDK, Cloud Development Kit, IaC, infrastructure as code, drift detection, stack policy, StackSets, nested stacks, cfn-init, cfn-signal, SSM Run Command, SSM Session Manager, SSM Patch Manager, SSM Parameter Store, Secrets Manager, OpsWorks, CodeDeploy, blue-green, canary, traffic splitting, Elastic Beanstalk, EC2 Image Builder, AMI, deployment strategy, immutable infrastructure, patch management, maintenance window

Key services: CloudFormation, AWS CDK, SSM, CodeDeploy, CodePipeline, Elastic Beanstalk, OpsWorks, EC2 Image Builder

## Domain 4 — Networking and Content Delivery (18%)
**Directory:** `Sources/Networking/`

Keywords: VPC, subnet, route table, NACL, network ACL, security group, VPC endpoint, PrivateLink, VPN, Direct Connect, DX, Transit Gateway, Route 53, routing policy, latency routing, geolocation, geoproximity, CloudFront, CDN, Global Accelerator, ALB, NLB, load balancer, egress-only internet gateway, NAT gateway, IPv6, VPC Flow Logs, ENI, peering, connectivity, DNS, SSL, ACM certificate

Key services: VPC, Route 53, CloudFront, Global Accelerator, Direct Connect, Transit Gateway, ALB, NLB, AWS WAF, AWS Shield

## Domain 5 — Security and Compliance (16%)
**Directory:** `Sources/Security-Compliance/`

Keywords: IAM, role, policy, permission boundary, SCP, service control policy, AWS Organizations, Control Tower, KMS, CMK, customer master key, ACM, certificate, GuardDuty, Security Hub, Inspector, Macie, AWS Config, conformance pack, WAF, web application firewall, Shield, DDoS, encryption, SAML, federated identity, iam:PassRole, cross-account, compliance, audit, threat detection

Key services: IAM, AWS Organizations, KMS, ACM, GuardDuty, Security Hub, Inspector, Macie, AWS Config, WAF, Shield

## Domain 6 — Cost and Performance Optimization (integrated into Domain 1)
**Directory:** `Sources/Cost-Performance/`

Keywords: Cost Explorer, AWS Budgets, billing alarm, cost allocation tag, Savings Plans, Reserved Instances, Spot Instance, interruption, right-sizing, Compute Optimizer, Trusted Advisor, S3 lifecycle, storage class, Standard-IA, Glacier, Transfer Acceleration, multipart upload, RDS Performance Insights, RDS Proxy, EC2 right-sizing, instance family, memory metric, EC2 Image Builder, Fargate cost, operational overhead

Key services: Cost Explorer, AWS Budgets, Compute Optimizer, Trusted Advisor, S3, RDS Performance Insights

## Exam-Prep
**Directory:** `Sources/Exam-Prep/`

Keywords: exam guide, study guide, practice exam, practice question, sample question, Tutorials Dojo, Stephane Maarek, Adrian Cantrill, Andrew Brown, Whizlabs, Skill Builder, passing score, mind map, flashcard, gotcha, cheat sheet, domain weight, exam tip

## Domain Disambiguation Rules

| Keyword | Primary Domain | Notes |
|---------|---------------|-------|
| CloudWatch | Monitoring-Logging | Unless in cost context → Cost-Performance |
| Trusted Advisor | Cost-Performance | Unless security check context |
| Compute Optimizer | Cost-Performance | Also appears in Monitoring gotchas |
| Route 53 health check | Reliability | Unless routing policy context → Networking |
| SSM Automation | Both Deployment-Automation AND Monitoring-Logging | File in domain most relevant to content |
| AWS Config | Security-Compliance | Config auto-remediation → also Monitoring |
| KMS | Security-Compliance | Unless CloudFormation Parameter Store → Deployment |
| EventBridge | Monitoring-Logging (remediation patterns) | — |
| VPC endpoints | Networking | Unless security context → Security-Compliance |
