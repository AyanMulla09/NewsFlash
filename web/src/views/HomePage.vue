<!--
 * @Author: xuqin.zhan xuqing.zhao@ichainfo.com
 * @Date: 2024-12-19 18:26:13
 * @LastEditors: xuqin.zhan xuqing.zhao@ichainfo.com
 * @LastEditTime: 2024-12-27 22:07:52
 * @FilePath: /COMP41720/src/views/HomePage.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template lang="pug">
  .home
    .homeTitle(@click="reloadPage") Daily News
    <el-tabs v-model="activeName" class="news-tabs" @tab-click="handleClick">
      <el-tab-pane label="Home" name="homepage">
        HomeNews
      </el-tab-pane>
      <el-tab-pane label="AsiaNews" name="asiapage">
        AsianNews(:asiaList="asiaList")
      </el-tab-pane>
      <el-tab-pane label="Guardian" name="guardianpage">
        GuardianNews(:guardianList="guardianList")
      </el-tab-pane>
      <el-tab-pane label="NYTimes" name="nypage">
        NYTimesNews(:nyList="nyList")
      </el-tab-pane>
    </el-tabs>
</template>

<script>
import { ref } from 'vue';
import HomeNews from '@/components/HomeNews.vue'
import AsianNews from '@/components/asianNews/AsianNews.vue';
import GuardianNews from '@/components/guardianNews/GuardianNews.vue';
import NYTimesNews from '@/components/nyTimesNews/NYTimesNews.vue';
import { getAsiaNews, getGuardianNews, getNyNews } from '@/service/newsAPIList/index.js';
import { ElTabs, ElTabPane, ElMessage } from 'element-plus';

export default {
  components: {
    HomeNews,
    AsianNews,
    GuardianNews,
    NYTimesNews,
    ElTabs,
    ElTabPane,
  },
  setup() {
    const activeName = ref('homepage');
    const asiaList = ref([]); // asia news list
    const guardianList = ref([]); // guardian news list
    const nyList = ref([]); // NYTines news list
    // click tab
    const handleClick = async (tab) => {
      console.log(tab);
      if (tab.props.name === 'asiapage' && asiaList.value.length === 0) {
        console.log('enter asiapage');
        try {
          const asiaNewsResponse = await getAsiaNews();
          // test code
          // const asiaNewsResponse = [];
          // console.log(asiaNewsResponse)
          if (asiaNewsResponse && Array.isArray(asiaNewsResponse)) {
            console.log('enter')
            if (asiaNewsResponse.length === 0) {
              ElMessage({
                message: 'No News update from the aisa news API',
                type: 'warning',
              })
              }
            asiaList.value = asiaNewsResponse;
          } else {
            console.error('data exception of asianews');
          }
        } catch (error) {
          console.log(error);
        }
      } else if (tab.props.name === 'guardianpage' && guardianList.value.length === 0) {
          console.log('enter guardianpage');
          try {
            const guardianNewsResponse = await getGuardianNews();
            // console.log(guardianNewsResponse, 'guardianNewsResponse')
            // test code
            // const guardianNewsResponse = [];
            if (guardianNewsResponse && Array.isArray(guardianNewsResponse)) {
              if (guardianNewsResponse.length === 0) {
                ElMessage({
                  message: 'No News update from the guardian news API',
                  type: 'warning',
                })
              }
              guardianList.value = guardianNewsResponse;
            } else {
              console.log('data exception of guardiannews');
            }
          } catch (error) {
            console.log(error);
          }
      } else if (tab.props.name === 'nypage' && nyList.value.length === 0) {
          console.log('enter nypage');
          try {
            const nyNewsResponse = await getNyNews();
            // console.log(nyNewsResponse)
            // test code
            // const nyNewsResponse = [];
            if (nyNewsResponse && Array.isArray(nyNewsResponse)) {
              if (nyNewsResponse.length === 0) {
                ElMessage({
                  message: 'No News update from the NYTimes news API',
                  type: 'warning',
                })
              }
              nyList.value = nyNewsResponse;
            } else {
              console.log('data exception of nynews');
            }
          } catch (error) {
            console.log(error);
          }
      }
    };

    // click headtitle reload page
    const reloadPage = () => {
      window.location.reload();
    }

    return {
      activeName,
      asiaList,
      guardianList,
      nyList,
      handleClick,
      reloadPage
    };
  },
};
</script>

<style lang="stylus" scoped>
.home
  font-size 16px
  padding 20px
  background-color #f9f9f9
  color #333
  font-family 'Arial', sans-serif
  ::v-deep(.el-tabs__nav)
    align-items: center
    justify-content: space-around
    width: 100%
.homeTitle
  font-size 32px
  font-weight bold
  text-align center
  margin-bottom 30px
  color #000
  &:hover
    cursor: pointer
</style>
