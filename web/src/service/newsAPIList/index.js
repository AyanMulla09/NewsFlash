import { $http } from '../index';
// const BASE_URL = 'http://127.0.0.1:8000/'; 

// get asianews
export const getAsiaNews = (queryParams = {}) => {
  const url = `asianews/today`;
  return $http({
    url: url,
    method: 'GET',
    params: queryParams,
  });
};
// get categories of asianews
export const getAsiaNewsCategories = (queryParams = {}) => {
  const url = `asianews/categories`;
  return $http({
    url: url,
    method: 'GET',
    params: queryParams,
  });
};

// get asianews list of one categories
export const getSelectCateAsiaNews = (queryParams = {}) => {
  // console.log(queryParams, 'api')
  const {category} = queryParams;
  console.log(category, 'api')
  const url = `asianews/today/${category}`;
  return $http({
    url: url,
    method: 'GET',
    // params: queryParams,
  });
};

// get guardian
export const getGuardianNews = (queryParams = {}) => {
  const url = `guardian/today`;
  return $http({
    url: url,
    method: 'GET',
    params: queryParams,
  });
};

// get categories of guardian
export const getGuardianCategories = (queryParams = {}) => {
  const url = `guardian/categories`;
  return $http({
    url: url,
    method: 'GET',
    params: queryParams,
  });
};

// get guardian of one categories
export const getSelectCateGuardian = (queryParams = {}) => {
  // console.log(queryParams, 'api')
  const {category} = queryParams;
  console.log(category, 'api')
  const url = `guardian/today/${category}`;
  return $http({
    url: url,
    method: 'GET',
    // params: queryParams,
  });
};

// get NYNews
export const getNyNews = (queryParams = {}) => {
  const url = `nytimes/today`;
  return $http({
    url: url,
    method: 'GET',
    params: queryParams,
  });
};

// get categories of NYNews
export const getNyCategories = (queryParams = {}) => {
  const url = `nytimes/categories`;
  return $http({
    url: url,
    method: 'GET',
    params: queryParams,
  });
};
// get guardian list of one categories
export const getSelectCateNy = (queryParams = {}) => {
  // console.log(queryParams, 'api')
  const {category} = queryParams;
  console.log(category, 'api')
  const url = `nytimes/today/${category}`;
  return $http({
    url: url,
    method: 'GET',
    // params: queryParams,
  });
};

// get today news

