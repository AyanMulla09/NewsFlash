<!--
 * @Author: xuqin.zhan xuqing.zhao@ichainfo.com
 * @Date: 2024-12-23 02:30:59
 * @LastEditors: xuqin.zhan xuqing.zhao@ichainfo.com
 * @LastEditTime: 2024-12-24 17:42:56
 * @FilePath: /COMP41720/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# daily-news

## node version
18.12.0

---

## introduction of project
### web page interaction and function
single page with four tab
- click headtitle reload page
- Home
  - news list display
  - Click on the news list to jump to the news page
  - news list sort
  The front end combine the data of three groups of news and implements the sorting function according to title, source and category.
- asia news
  - news list display
  - Click on the news list to jump to the news page
  - news filter (calls the backend API) 
- guardian news
  - news list display
  - Click on the news list to jump to the news page
  - news filter according to category (calls the backend API) 
- NYTimes news
  - news list display
  - Click on the news list to jump to the news page
  - news filter according to category (calls the backend API) 


### about API
The following are the APIs used in this project
```
localhost:8000/asianews/today
localhost:8000/asianews/categories
localhost:8000/asianews/today/{category}
localhost:8000/guardian/today
localhost:8000/guardian/categories
localhost:8000/guardian/today/{category}
localhost:8000/nytimes/today
localhost:8000/nytimes/categories
localhost:8000/nytimes/today/{category}
```
### api docs
http://localhost:8000/docs#

### Technology Stack Used

- vue3
- pug (html)
- stylus (css)
- element-UI https://element.eleme.io/#/en-US
- eslint (code check)
- axios (request api)
- yarn (package and project management tool)
- Nginx (Reverse proxy API requests, as a server to host static resource [html, js, css..])

## Local start Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

---
## frontend project deployment process
1. Frontend packaging and containerization: The Vue3 project is built using Node.js and create the static files.
2. Nginx static resource hosting: Nginx as a server to host packaged frontend pages and static resources.
3. Reverse proxy API requests
4. Containerized deployment with docker
