
# Documentação da API `deskewImage`

Este documento descreve os passos necessários para preparar, criar e configurar uma função AWS Lambda para processamento de imagens utilizando Docker, Amazon ECR (Elastic Container Registry) e Amazon API Gateway.

## Preparação da Imagem Docker e Push para ECR

### Docker Image Preparation and ECR Push

1. **Construir Imagem Docker**

   ```shell
   docker build -t lambda-opencv-image .
   ```

2. **Marcar Imagem Docker**

   ```shell
   docker tag lambda-opencv-image:latest <aws-account-id>.dkr.ecr.<region>.amazonaws.com/lambda-opencv-repo:latest
   ```

3. **Login no ECR**

   ```shell
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<region>.amazonaws.com
   ```

4. **Criar Repositório na Amazon ECR**

   ```shell
   aws ecr create-repository --repository-name lambda-opencv-repo --region us-east-2
   ```

5. **Push da Imagem Docker para o ECR**

   ```shell
   docker push <aws-account-id>.dkr.ecr.<region>.amazonaws.com/lambda-opencv-repo:latest
   ```

## Criação de Role IAM para Execução da Lambda

### IAM Role Creation for Lambda Execution

1. **Criar Role IAM**

   ```shell
   aws iam create-role --role-name LambdaExecutionRole --assume-role-policy-document file://trust-policy.json
   ```

2. **Anexar Política à Role IAM**

   ```shell
   aws iam attach-role-policy --role-name LambdaExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
   ```

## Criação e Configuração da Função Lambda

### Lambda Function Creation and Configuration

1. **Criar Função Lambda Usando a Imagem do ECR**

   ```shell
   aws lambda create-function      --function-name deskewImage      --package-type Image      --code ImageUri=<aws-account-id>.dkr.ecr.<region>.amazonaws.com/lambda-opencv-repo:latest      --role arn:aws:iam::<aws-account-id>:role/LambdaExecutionRole      --region <region>
   ```

2. **Configurar Tempo de Execução da Função Lambda na Criação**

   ```shell
   aws lambda update-function-configuration --function-name deskewImage --timeout 30 --region <region>
   ```

## Criação de API no Amazon API Gateway

### Criação e Configuração da API

1. **Acessar o Amazon API Gateway**
2. **Criar uma nova API**
3. **Criar um novo recurso**
4. **Criar um método POST**
5. **Configurar o método POST (Opcional)**
6. **Implantar a API**
7. **Testar a API**

Com esses passos, você configura uma API REST no Amazon API Gateway, cria um método POST para acionar sua função Lambda `deskewImage` e implanta a API para acesso público.

---

Lembre-se de ajustar as configurações conforme necessário para atender às suas necessidades específicas, incluindo autenticação, autorização, limites de taxa e outras considerações de segurança e operacionais.
