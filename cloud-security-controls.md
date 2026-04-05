# Cloud Security Controls & Compliance

Apply security controls and best practices for AWS cloud environments aligned with NIST 800-53r5, FedRAMP (High/Moderate/Low), NIST 800-171, NIST Privacy Framework, and AWS Well-Architected Security Pillar.

## Trigger

Use this skill when:
- Designing or reviewing AWS infrastructure security
- Implementing compliance controls for FedRAMP, NIST, or federal standards
- Writing AWS Config conformance packs or rules
- Auditing cloud environments for security gaps
- Hardening IAM, network, storage, or monitoring configurations

---

## Framework Mapping

| Control Area | NIST 800-53r5 | FedRAMP High | FedRAMP Moderate | FedRAMP Low | NIST 800-171 |
|---|---|---|---|---|---|
| IAM Password Policy | IA-5 | Required | Required | Required | 3.5.7 |
| MFA | IA-2 | Required | Required | Required | 3.5.3 |
| Encryption at Rest | SC-28 | Required | Required | Recommended | 3.13.16 |
| Encryption in Transit | SC-8 | Required | Required | Required | 3.13.8 |
| Audit Logging | AU-2, AU-3 | Required | Required | Required | 3.3.1 |
| Network Segmentation | SC-7 | Required | Required | Required | 3.13.1 |
| Vulnerability Mgmt | SI-2, RA-5 | Required | Required | Recommended | 3.14.1 |
| Backup & Recovery | CP-9 | Required | Required | Required | 3.8.9 |

---

## 1. Identity & Access Management (IAM)

### Password Policy (All Frameworks)
```
Minimum length:       14 characters (High/Moderate/800-53/800-171) | 8 chars (Privacy Framework only)
Max password age:     90 days
Password reuse:       Prevent last 24 passwords
Require uppercase:    true
Require lowercase:    true
Require numbers:      true
Require symbols:      true
```

**AWS Config Rules:**
- `IAM_PASSWORD_POLICY` — enforce all complexity/rotation requirements
- `IAM_USER_UNUSED_CREDENTIALS_CHECK` — disable credentials unused for 90+ days
- `ACCESS_KEYS_ROTATED` — rotate access keys every 90 days

### MFA Requirements
- Require MFA for all IAM console users: `MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS`
- Require MFA for all IAM users: `IAM_USER_MFA_ENABLED`
- Never create root access keys: `IAM_ROOT_ACCESS_KEY_CHECK`

### Least Privilege
- No inline policies on users/roles/groups: `IAM_NO_INLINE_POLICY_CHECK`
- No policies directly attached to users: `IAM_USER_NO_POLICIES_CHECK`
- All users must belong to a group: `IAM_USER_GROUP_MEMBERSHIP_CHECK`
- No wildcard admin policies: `IAM_POLICY_NO_STATEMENTS_WITH_ADMIN_ACCESS`
- Block KMS decrypt/re-encrypt in customer policies: `IAM_CUSTOMER_POLICY_BLOCKED_KMS_ACTIONS`
- Block KMS decrypt/re-encrypt in inline policies: `IAM_INLINE_POLICY_BLOCKED_KMS_ACTIONS`

**Blocked KMS actions (FedRAMP High / NIST 800-53r5):** `kms:Decrypt`, `kms:ReEncryptFrom`, `kms:*`

---

## 2. Encryption at Rest

Enable encryption for **all** data stores. Default to KMS Customer Managed Keys (CMK) for FedRAMP High.

| Service | Config Rule | CMK Required (FedRAMP High) |
|---|---|---|
| EBS volumes | `ENCRYPTED_VOLUMES` | Yes |
| EBS default | `EC2_EBS_ENCRYPTION_BY_DEFAULT` | Yes |
| S3 buckets | `S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED` | Yes |
| S3 KMS default | `S3_DEFAULT_ENCRYPTION_KMS` | Yes |
| RDS instances | `RDS_STORAGE_ENCRYPTED` | Yes |
| RDS snapshots | `RDS_SNAPSHOT_ENCRYPTED` | Yes |
| DynamoDB | `DYNAMODB_TABLE_ENCRYPTED_KMS` | Yes |
| EFS | `EFS_ENCRYPTED_CHECK` | Yes |
| Redshift | `REDSHIFT_CLUSTER_KMS_ENABLED` | Yes |
| Kinesis Streams | `KINESIS_STREAM_ENCRYPTED` | Yes |
| CloudWatch Logs | `CLOUDWATCH_LOG_GROUP_ENCRYPTED` | Yes |
| SageMaker endpoints | `SAGEMAKER_ENDPOINT_CONFIGURATION_KMS_KEY_CONFIGURED` | Yes |
| SageMaker notebooks | `SAGEMAKER_NOTEBOOK_INSTANCE_KMS_KEY_CONFIGURED` | Yes |
| SNS topics | `SNS_ENCRYPTED_KMS` | Yes |
| Secrets Manager | `SECRETSMANAGER_USING_CMK` | Yes |
| Backup recovery points | `BACKUP_RECOVERY_POINT_ENCRYPTED` | Yes |
| ElasticSearch | `ELASTICSEARCH_ENCRYPTED_AT_REST` | Yes |

---

## 3. Encryption in Transit

- API Gateway stages must use SSL: `API_GW_SSL_ENABLED`
- API Gateway cache must be encrypted: `API_GW_CACHE_ENABLED_AND_ENCRYPTED`
- ELB/ALB listeners must use HTTPS — check listener protocols
- ACM certificates expire check (90-day warning): `ACM_CERTIFICATE_EXPIRATION_CHECK`
- VPC VPN connections require 2 tunnels up: `VPC_VPN_2_TUNNELS_UP`
- Redshift: enforce SSL via parameter group (`require_ssl = true`)

---

## 4. Audit Logging & Monitoring

### CloudTrail (Required for All Frameworks)
- Multi-region trail enabled: `MULTI_REGION_CLOUD_TRAIL_ENABLED`
- CloudTrail enabled: `CLOUD_TRAIL_ENABLED`
- CloudTrail encryption (KMS): `CLOUD_TRAIL_ENCRYPTION_ENABLED`
- Log file validation: `CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED`
- CloudWatch Logs integration: `CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED`
- S3 data events logging: `CLOUDTRAIL_S3_DATAEVENTS_ENABLED`
- Security trail enabled: `CLOUDTRAIL_SECURITY_TRAIL_ENABLED`
- CloudTrail S3 bucket must be private: `CLOUDTRAIL_S3_BUCKET_PUBLIC_ACCESS_PROHIBITED`

### Service-Level Logging
- VPC Flow Logs: `VPC_FLOW_LOGS_ENABLED`
- ELB/ALB access logs: `ELB_LOGGING_ENABLED`
- S3 server access logs: `S3_BUCKET_LOGGING_ENABLED`
- RDS logs to CloudWatch: `RDS_LOGGING_ENABLED`
- API Gateway execution logs: `API_GW_EXECUTION_LOGGING_ENABLED`
- Redshift audit logging: `REDSHIFT_CLUSTER_CONFIGURATION_CHECK` (loggingEnabled=TRUE)
- ElasticSearch logs to CloudWatch: `ELASTICSEARCH_LOGS_TO_CLOUDWATCH`
- WAF logging: `WAFV2_LOGGING_ENABLED`

### Alerting
- CloudWatch Alarms must have actions configured: `CLOUDWATCH_ALARM_ACTION_CHECK`
  - `alarmActionRequired: true`
  - `insufficientDataActionRequired: true`

### Threat Detection
- GuardDuty enabled (centralized): `GUARDDUTY_ENABLED_CENTRALIZED`
- GuardDuty finding SLA response times:
  - High severity: resolve within **1 day**
  - Medium severity: resolve within **7 days**
  - Low severity: resolve within **30 days**
- SecurityHub enabled: `SECURITYHUB_ENABLED`

---

## 5. Network Security

### Public Access Prevention
- EC2 instances must be in VPC: `INSTANCES_IN_VPC`
- Subnets must not auto-assign public IPs: `SUBNET_AUTO_ASSIGN_PUBLIC_IP_DISABLED`
- AutoScaling launch configs must not assign public IPs: `AUTOSCALING_LAUNCH_CONFIG_PUBLIC_IP_DISABLED`
- EKS API endpoint must not be public: `EKS_ENDPOINT_NO_PUBLIC_ACCESS`
- Lambda must not have public access: `LAMBDA_FUNCTION_PUBLIC_ACCESS_PROHIBITED`
- Lambda must be inside VPC: `LAMBDA_INSIDE_VPC`
- RDS instances must not be publicly accessible: `RDS_INSTANCE_PUBLIC_ACCESS_CHECK`
- Redshift clusters must not be public: `REDSHIFT_CLUSTER_PUBLIC_ACCESS_CHECK`
- EMR master nodes must not have public IPs: `EMR_MASTER_NO_PUBLIC_IP`
- SageMaker notebooks must not have direct internet: `SAGEMAKER_NOTEBOOK_NO_DIRECT_INTERNET_ACCESS`

### Security Groups
- Default VPC security group must have no rules: `VPC_DEFAULT_SECURITY_GROUP_CLOSED`
- SSH (port 22) must not be open to 0.0.0.0/0: `INCOMING_SSH_DISABLED`
- Security groups open only to authorized ports (443): `VPC_SG_OPEN_ONLY_TO_AUTHORIZED_PORTS`

---

## 6. Backup & Resilience

### Backup Policy Minimums
```
Frequency:     Daily (1 day)
Retention:     35 days minimum
```

| Resource | Config Rule |
|---|---|
| Backup plan frequency/retention | `BACKUP_PLAN_MIN_FREQUENCY_AND_MIN_RETENTION_CHECK` |
| Recovery point minimum retention | `BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK` |
| Recovery points are encrypted | `BACKUP_RECOVERY_POINT_ENCRYPTED` |
| Recovery point deletion disabled | `BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED` |
| DynamoDB PITR enabled | `DYNAMODB_PITR_ENABLED` |
| DynamoDB in backup plan | `DYNAMODB_IN_BACKUP_PLAN` |
| EBS in backup plan | `EBS_IN_BACKUP_PLAN` |
| EFS in backup plan | `EFS_IN_BACKUP_PLAN` |
| RDS in backup plan | `RDS_IN_BACKUP_PLAN` |
| S3 cross-region replication | `S3_BUCKET_CROSS_REGION_REPLICATION_ENABLED` |
| S3 versioning enabled | `S3_BUCKET_VERSIONING_ENABLED` |
| S3 version lifecycle policy | `S3_VERSION_LIFECYCLE_POLICY_CHECK` |
| Aurora protected by backup plan | `AURORA_RESOURCES_PROTECTED_BY_BACKUP_PLAN` |
| EC2 instances in backup plan | `EC2_RESOURCES_PROTECTED_BY_BACKUP_PLAN` |
| ElastiCache Redis automatic backup | `ELASTICACHE_REDIS_CLUSTER_AUTOMATIC_BACKUP_CHECK` |
| Redshift backup enabled | `REDSHIFT_BACKUP_ENABLED` |

### High Availability
- RDS Multi-AZ: `RDS_MULTI_AZ_SUPPORT` and `RDS_CLUSTER_MULTI_AZ_ENABLED`
- RDS deletion protection: `RDS_INSTANCE_DELETION_PROTECTION_ENABLED`
- DynamoDB autoscaling: `DYNAMODB_AUTOSCALING_ENABLED`
- DynamoDB throughput limit check: `DYNAMODB_THROUGHPUT_LIMIT_CHECK` (80% threshold)

---

## 7. Vulnerability & Patch Management

- EC2 instances managed by SSM: `EC2_INSTANCE_MANAGED_BY_SSM`
- SSM association compliance: `EC2_MANAGEDINSTANCE_ASSOCIATION_COMPLIANCE_STATUS_CHECK`
- SSM patch compliance: `EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK`
- Inspector EC2 scanning enabled: `INSPECTOR_EC2_SCAN_ENABLED`
- Inspector ECR container scanning: `INSPECTOR_ECR_SCAN_ENABLED`
- Inspector Lambda scanning: `INSPECTOR_LAMBDA_STANDARD_SCAN_ENABLED`

---

## 8. FedRAMP Impact Level Requirements

### FedRAMP High (Most Restrictive)
All controls above plus:
- CMK required for all encrypted services (no AWS-managed keys)
- KMS decrypt/re-encrypt blocked in all IAM policies
- Password length: 14 chars minimum
- DynamoDB throughput threshold: 80%
- EC2 volumes deleted on termination: required
- All backup/retention controls at maximum
- Both Part 1 and Part 2 conformance packs required

### FedRAMP Moderate
- Same as High but CMK not mandated for every service
- KMS actions blocked in customer/inline policies
- Password length: 14 chars
- All logging, monitoring, and network controls apply

### FedRAMP Low (Baseline)
- Core IAM, logging, network segmentation required
- Password policy: 14 chars
- GuardDuty, SecurityHub, CloudTrail required
- Encryption strongly recommended but some flexibility

---

## 9. AWS Config Conformance Pack Deployment Pattern

```yaml
# Minimal conformance pack structure
AWSTemplateFormatVersion: "2010-09-09"
Description: Security Controls Conformance Pack

Parameters:
  IamPasswordPolicyParamMinimumPasswordLength:
    Default: '14'
    Type: String
  IamPasswordPolicyParamMaxPasswordAge:
    Default: '90'
    Type: String
  IamPasswordPolicyParamPasswordReusePrevention:
    Default: '24'
    Type: String
  AccessKeysRotatedParamMaxAccessKeyAge:
    Default: '90'
    Type: String
  GuarddutyNonArchivedFindingsParamDaysHighSev:
    Default: '1'
    Type: String
  GuarddutyNonArchivedFindingsParamDaysMediumSev:
    Default: '7'
    Type: String
  GuarddutyNonArchivedFindingsParamDaysLowSev:
    Default: '30'
    Type: String

Resources:
  # Add rules referencing Parameters above
  IamPasswordPolicy:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: iam-password-policy
      Source:
        Owner: AWS
        SourceIdentifier: IAM_PASSWORD_POLICY
      InputParameters:
        MinimumPasswordLength: !Ref IamPasswordPolicyParamMinimumPasswordLength
        MaxPasswordAge: !Ref IamPasswordPolicyParamMaxPasswordAge
        PasswordReusePrevention: !Ref IamPasswordPolicyParamPasswordReusePrevention
        RequireUppercaseCharacters: 'true'
        RequireLowercaseCharacters: 'true'
        RequireNumbers: 'true'
        RequireSymbols: 'true'
```

---

## 10. Priority Order for Implementation

When hardening an AWS environment, implement in this order:

1. **Root account hardening** — disable root access keys, enable MFA on root
2. **IAM baseline** — password policy, MFA enforcement, user/group structure
3. **CloudTrail** — enable multi-region, encrypt, send to CloudWatch Logs
4. **GuardDuty + SecurityHub** — enable threat detection and aggregation
5. **Encryption at rest** — enable EBS default encryption, S3 SSE, RDS encryption
6. **Network hardening** — close default SGs, block public subnets, enable VPC Flow Logs
7. **Backup policies** — daily backups, 35-day retention, enable PITR for DynamoDB
8. **Patch management** — onboard EC2 to SSM, configure patch baselines, enable Inspector
9. **Service-level logging** — ELB, S3, RDS, API GW, WAF logs
10. **Encryption in transit** — enforce TLS on all endpoints, rotate ACM certs

---

## 11. Key Parameter Defaults by Framework

| Parameter | FedRAMP High | FedRAMP Moderate | FedRAMP Low | NIST 800-53r5 | NIST 800-171 |
|---|---|---|---|---|---|
| Min password length | 14 | 14 | 14 | 14 | 14 |
| Max password age (days) | 90 | 90 | 90 | 90 | 90 |
| Password reuse prevention | 24 | 24 | 24 | 24 | 24 |
| Access key rotation (days) | 90 | 90 | 90 | 90 | 90 |
| Unused credentials (days) | 90 | 90 | 90 | 90 | 90 |
| ACM cert expiry warning (days) | 90 | 90 | 90 | 90 | 90 |
| GuardDuty High SLA (days) | 1 | 1 | 1 | 1 | 1 |
| GuardDuty Medium SLA (days) | 7 | 7 | 7 | 7 | 7 |
| GuardDuty Low SLA (days) | 30 | 30 | 30 | 30 | 30 |
| Backup retention (days) | 35 | 35 | 35 | 35 | 35 |
| Backup frequency | Daily | Daily | Daily | Daily | Daily |
| DynamoDB throughput threshold | 80% | 80% | 80% | — | — |
| Authorized TCP ports (SG) | 443 | 443 | 443 | 443 | 443 |
