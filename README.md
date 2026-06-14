# AWS Serverless Assignments

This repository contains hands-on assignments demonstrating AWS Serverless Architecture concepts using AWS Lambda, Amazon EC2, IAM, CloudWatch, and other AWS services.

## Author

**Vivek Rajendran**

Lead Software Engineer | Java | Spring Boot | Cloud | AWS

---

## Repository Structure

```text
aws-serverless-assignments/
│
├── README.md
│
├── Assignment-1_Automated_Instance_Management/
│   ├── README.md
│   ├── lambda_function.py
│   └── Assignment1_Screenshots.docx
│
├── Assignment-2/
│
├── Assignment-3/
│
└── Assignment-4/
```

---

## Assignments

| Assignment   | Description                                              | Status    |
| ------------ | -------------------------------------------------------- | --------- |
| Assignment 1 | Automated Instance Management Using AWS Lambda and Boto3 | Completed |
| Assignment 2 | To Be Added                                              | Pending   |
| Assignment 3 | To Be Added                                              | Pending   |
| Assignment 4 | To Be Added                                              | Pending   |

---

## Assignment 1 – Automated Instance Management Using AWS Lambda and Boto3

### Objective

Automate the management of Amazon EC2 instances using AWS Lambda and Boto3 based on instance tags.

### Features

* Detect EC2 instances tagged with `Action=Auto-Stop`
* Stop running EC2 instances automatically
* Detect EC2 instances tagged with `Action=Auto-Start`
* Start stopped EC2 instances automatically
* Log execution details in Amazon CloudWatch
* Implemented using Python and Boto3

### AWS Services Used

* AWS Lambda
* Amazon EC2
* AWS IAM
* Amazon CloudWatch
* Boto3 SDK

### Assignment Location

```text
Assignment-1_Automated_Instance_Management/
```

---

## Technologies Used

* Python 3.x
* AWS Lambda
* Amazon EC2
* AWS IAM
* Amazon CloudWatch
* Boto3
* Git
* GitHub

---

## How to Clone the Repository

```bash
git clone https://github.com/vivek-rajendran/aws-serverless-assignments.git
```

Navigate to the project:

```bash
cd aws-serverless-assignments
```

---

## Future Enhancements

* EventBridge Scheduler integration
* Multi-region EC2 management
* Automated reporting using SNS
* Cost optimization automation
* Serverless monitoring dashboards

---

## License

This repository is created for learning and assignment submission purposes.
