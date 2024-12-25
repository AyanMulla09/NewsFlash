<!--
 * @Author: xuqin.zhan xuqing.zhao@ichainfo.com
 * @Date: 2024-11-21 20:46:44
 * @LastEditors: xuqin.zhan xuqing.zhao@ichainfo.com
 * @LastEditTime: 2024-12-03 23:27:37
 * @FilePath: /daily-news/src/App.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div id="app" class="app">
    <suspense>
      <router-view></router-view>
    </suspense>
  </div>
</template>

<script>

export default {
  name: 'App',
}
</script>

<style lang="stylus">
@import './styles/_reset.styl'
@import './styles/_base.styl'
.ipad.landscape
  .app
    height 100%
    box-sizing border-box
    width calc(80vh)
    margin auto
.ipad.portrait
  .app
    height 100%
    box-sizing border-box
    width 80%
    margin auto
</style>
