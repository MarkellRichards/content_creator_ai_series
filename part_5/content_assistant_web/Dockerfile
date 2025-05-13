FROM --platform=linux/amd64 node:24-slim as builder
WORKDIR /src
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM --platform=linux/amd64 nginx:1.28
EXPOSE 80
# Copy the build artifacts to the NGINX html directory
COPY --from=builder /src/dist /usr/share/nginx/html
# Copy the custom NGINX configuration into the container
COPY nginx.conf /etc/nginx/conf.d/default.conf