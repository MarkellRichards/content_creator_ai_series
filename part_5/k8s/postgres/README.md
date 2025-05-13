# Overview

In part 5 of this series we are moving our genartive AI application to Kubernetes. Within kubernetes we will be running an instance of Postgres database using cloud-native pg operator.

## Setting up the operator

```bash
helm repo add cnpg https://cloudnative-pg.github.io/charts
helm upgrade --install cnpg \
  --namespace cnpg-system \
  --create-namespace \
  cnpg/cloudnative-pg
```

With the operator installed within our cluster we can now setup our database cluster. Following CloudNative PG recommendations, we will dedicate a single PostgresSQL cluster to a single database, entirely managed by a single microservice applicaiton. Per CNPG FAQ, reserving a PostgreSQL instance to a single microserivce owned database enhances:

- Resource management: each database instance CPU and memory can be constrained with alignment to resource management policies at the pod level.
- Physical continuous backup and Point-In-Time-Recovery(PITR)
- Applicaiton updates: without impacting other datbase owners
- database updates: each application can decide which version of PostgreSQL version to use, independently, and when to upgrade.

## Create database cluster

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: databases
  labels:
    name: databases

---
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: content-db
  namespace: databases
spec:
  instances: 3

  bootstrap:
    initdb:
      database: content-server
      owner: content

  storage:
    size: 5Gi

  monitoring:
    enablePodMonitor: true
```

With this YAML, we create a namespace to place all of our databases. We also create a content-db cluster and boostrap it with a content-server database owned by the content user. We provided 5Gi of local storage. I will be personally replacing this with NFS storage using my NAS but for simplicity this will work. We also enable pod monitoring so we can later view database metrics.

We can then apply our yaml file to the cluster:

```bash
kubectl apply -f content-db.yaml
```

If you run:

```bash
kubectl get pods -A
```

You should see three content-db-{n..3} instances running in the databases namespace. To interact with this database, we need to inspect its credentials. Cnpg operator created a secret we can view.

```bash
kubectl -n databases get secrets
```

You should see `content-db-app`. Each secret is base64 encoded so we need to decode the values to view them. Here's an example on how to grab the database password.

```bash
kubectl -n databases get secret content-db-app -o=jsonpath='{.data.password}' | base64 -d
```

What if you want to view each value decoded? We can use jq. First we export the secret to a file:

Then we use jq to loop over each value in the data dictionary and then for each key-value pair, print the key and decoded value.

```bash
jq -r '.data | to_entries[] | "\(.key): \(.value | @base64d)"' secret.json
```

You can expose the database to interact with locally using the following command:

```bash
k -n databases expose service content-db-rw --name=content-service-db --port=5432 --type=LoadBalancer
```

Ensure your cluster load balancer is setup to assign static ips to exposed services. I use metallb and my cluster is within a VLAN with a range of IPs available for static addressing
