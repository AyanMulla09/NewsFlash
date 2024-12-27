<template lang="pug">
  .news-content
    el-select(v-model="value" placeholder="Select" style="width: 240px" @change="selectNewsCategory")
      el-option(
        v-for="item in options"
        :key="item.value"
        :label="changeValueFormat(item.label)"
        :value="item.value"
      )
    ul.news-list(v-if="guardianNewsList.length > 0")
      li(v-for="newsItem in guardianNewsList" :key="newsItem.title")
        a.news-item(:href="newsItem.link", target="_blank")
          img.news-image(:src="newsItem.image", :alt="newsItem.title")
          .news-details
            .title {{ newsItem.title }}
            .content-item
              .category {{ newsItem.category }}
              .date {{ newsItem.date }}
            .read-more Read More
    .empty-content(v-else)
      .empty-text The array list is empty
</template>

<script>
import { ref, watch, nextTick, onMounted } from 'vue';
import { getGuardianCategories, getSelectCateGuardian } from '@/service/newsAPIList/index.js';

export default {
  name: 'guardianNews',
  props: {
    guardianList: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const guardianNewsList = ref([]);
    const value = ref('All'); // default select "All"
    const options = ref([{ value: 'All', label: 'All Categories' }]); // default including "All Categories"
    const changeValueFormat = (categories) => {
      // console.log('value', value.replace('_', ' '))
      return categories.replace('_', ' ');
    }
    // click select
    const selectNewsCategory = async (category) => {
      guardianNewsList.value = [];
      // wait dom update
      await nextTick();
      console.log(guardianNewsList.value)
      // clean array
      if (category === 'All') {
        guardianNewsList.value = [...props.guardianList];
      } else {
        console.log(category)
        try {
          // Calling the specific category api
          const response = await getSelectCateGuardian({ category });
          console.log('response.categories', response);
          if (response && Array.isArray(response)) {
            guardianNewsList.value = response;
          } else {
            console.log(response);
          }
        } catch (error) {
          console.log(`Failed to fetch news category: "${category}":`, error);
        }
      }
    };
    // Loading category of news
    const getCategoriesData = async () => {
      try {
        const categoriesData = await getGuardianCategories();
        // console.log(categoriesData.categories)
        const categoriesList = categoriesData.categories;
        if (categoriesList && Array.isArray(categoriesList)) {
          options.value = [
            { value: 'All', label: 'All Categories' }, // default option
            ...categoriesList.map((category) => ({
              value: category,
              label: category,
            })),
          ];
        } else {
          console.error('Invalid categories data:', categoriesList);
        }
      } catch (error) {
        console.error('Failed to fetch categories of guardian', error);
      }
    };
    // update news list
    watch(
      () => props.guardianList,
      (newList) => {
        guardianNewsList.value = [...newList];
      },
      { immediate: true }
    );

    onMounted(() => {
      getCategoriesData();
    });

    return {
      changeValueFormat,
      guardianNewsList,
      selectNewsCategory,
      value,
      options,
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

.news-list
  flex: 1
  max-width: 1100px
  margin: auto 30px;
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