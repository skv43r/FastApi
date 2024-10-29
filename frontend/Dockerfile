FROM node:20-alpine

COPY package.json package.json
RUN npm install

COPY . .
RUN npm run build

CMD ["npm", "run", "start"]

EXPOSE 3000