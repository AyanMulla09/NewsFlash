<template lang="pug">
  .news-content
    .label-content
      <el-radio-group v-model="sortType" @change="changeNewsSort(sortType)">
        <el-radio :value="'source'"> sort by source </el-radio>
        <el-radio :value="'category'"> sort by category </el-radio>
        <el-radio :value="'title'"> sort by title </el-radio>
      </el-radio-group>
    ul.news-list(v-if="homeNewsList.length > 0")
      li(v-for="newsItem in homeNewsList" :key="newsItem.title")
        a.news-item(:href="newsItem.link", target="_blank")
          img.news-image(:src="newsItem.image", :alt="newsItem.title")
          .news-details
            .title {{ newsItem.title }}
            .content-item
              .category {{ newsItem.category }}
              .date {{ newsItem.date }}
            .content-item
              .news_source {{ newsItem.newsSource }}
              .read-more Read More
    .empty-content(v-else)
      .empty-text The array list is empty
</template>

<script>
import { ref, onMounted } from 'vue';
import { getAsiaNews, getGuardianNews, getNyNews } from '@/service/newsAPIList/index.js';
import { ElMessage } from 'element-plus';

export default {
  name: 'HomeNews',
  setup() {
    const homeNewsList = ref([]);
    const sortType = ref('source');
    // request data of news and combine
    const getHomePageData = async () => {
      try {
        // request all news data
        const [asiaNewsList, guardianNewsList, nyNewsList] = await Promise.all([
          getGuardianNews(),
          getAsiaNews(),
          getNyNews()
        ]);
        // console.log(asiaNewsList, guardianNewsList, nyNewsList)
        // test code
        // const asiaNewsList = []
        // const guardianNewsList = []
        // const nyNewsList = [];
        // add source in each list
        const newAsiaList = asiaNewsList.map(newsItem => ({
          ...newsItem,
          newsSource: 'AsiaNews'
        }));
        // console.log('newAsiaList', newAsiaList)
        const newGuardianList = guardianNewsList.map(newsItem => ({
          ...newsItem,
          newsSource: 'Guardian'
        }));
        // console.log(newGuardianList)
        const newNYList = nyNewsList.map(newsItem => ({
          ...newsItem,
          newsSource: 'NYTimes'
        }));
        // console.log(nyNewsList)
        // combine news list
        homeNewsList.value = [
          ...newAsiaList,
          ...newGuardianList,
          ...newNYList
        ];
        // console.log('homeNewsList', homeNewsList.value, homeNewsList.value.length)
        if (homeNewsList.value.length === 0) {
          ElMessage({
            message: 'No News update from the news API',
            type: 'warning',
          })
        }
      } catch (error) {
        console.log('loading fail', error)
      }
    };
    // sort
    const changeNewsSort = (e) => {
      console.log(e)
      if (e === 'source') {
        console.log('sort by source')
        getHomePageData();
      } else if (e === 'category') {
        console.log('sort by category')
        homeNewsList.value = [...homeNewsList.value].sort((a, b) => {
        const categoryA = a.category.toLowerCase();
        const categoryB = b.category.toLowerCase();
            return categoryA.localeCompare(categoryB);
        });
      } else if (e === 'title') {
        console.log('sort by title')
        homeNewsList.value = [...homeNewsList.value].sort((a, b) => {
        const titleA = a.title.toLowerCase();
        const titleB = b.title.toLowerCase();
            return titleA.localeCompare(titleB);
        });
      }
    }
    onMounted(() => {
      getHomePageData()
    });
    return {
      homeNewsList,
      sortType,
      changeNewsSort
    };
  },
};
</script>

<style lang="stylus" scoped>
.news-content
  display: flex
  justify-content: center
  padding: 20px
  flex-wrap: wrap
  background-color: #f7f8fa
  ::v-deep(.el-radio-group)
    flex-direction: column;
    justify-content: space-around;
    align-items: flex-start;
.news-list
  flex: 1
  max-width: 1100px
  margin: 0 auto
  display: flex
  flex-direction: column
  gap: 20px

.news-item
  display: flex
  align-items: flex-start
  background-color: #ffffff
  border-radius: 12px
  overflow: hidden
  &:hover
    cursor: pointer

  .news-image
    width: 200px
    height: 140px
    object-fit: cover
    border-top-left-radius: 12px
    border-bottom-left-radius: 12px

  .news-details
    padding: 20px
    flex: 1
    display: flex
    flex-direction: column
    justify-content: space-between

    .title
      font-size: 20px
      font-weight: 600
      margin-bottom: 12px
      color: #333
      line-height: 1.4
      &:hover
        color: #007bff

    .content-item
      display: flex
      justify-content: space-between
      align-items: center
      margin-bottom: 8px

    .category
      font-size: 14px
      color: #666
      font-weight: 500

    .date
      font-size: 13px
      color: #999

    .news_source
      background-color: #f0f0f0
      color: #555
      font-size: 12px
      padding: 3px 8px
      border-radius: 20px

.read-more
  text-align: end
  font-size: 14px
  margin-top: 12px
  &:hover
    text-decoration: underline
    color: #007bff

.header_title
  font-size: 36px
  font-weight: 700
  text-align: center
  margin-bottom: 40px
  color: #333
  letter-spacing: 1px
.empty-content
  flex: 1
  max-width: 1100px
  margin: auto 30px;
  display: flex
  flex-direction: column
  gap: 20px
</style>