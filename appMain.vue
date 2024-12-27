<template>
   <el-container :style="backgroundStyle" style="height: 100vh;">
    <el-aside width="200px" style="background-color: #2c3e50; color: white;">
      <el-menu
        default-active="spectrum"
        background-color="#2c3e50"
        text-color="#fff"
        active-text-color="#ffd04b"
        @select="onMenuClick"
      >
      <el-menu-item index="TotalGraph">
          <span>总览表</span>
        </el-menu-item>
        <el-menu-item index="spectrum">
          <span>光谱表</span>
        </el-menu-item>
        <el-menu-item index="LightCurve">
          <span>光变曲线表</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main style="padding: 24px;">
      <router-view />
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: "Main-x",
  data() {
    return {
      backgroundStyle: {
        'background-image': `url(${require('@/assets/sys_index.png')})`,
        'background-size': 'cover',
        'background-position': 'center',
        'background-repeat': 'no-repeat'
      }
    };
  },
  methods: {
    onMenuClick(index) {
      if (index === 'spectrum') {
        this.$router.push('/spectrum');
      }
      if (index === 'TotalGraph') {
        this.$router.push('/TotalGraph');
      }
      if (index === 'LightCurve') {
        this.$router.push('/LightCurve');
      }
    },
  },
};
</script>

<style scoped>
/* 自定义样式可以根据需要添加 */
.el-menu {
  border-right: none;
}
/*  yt_sys_index.jpg   */


</style>