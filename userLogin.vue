<template>
  <div class="login-container">
    <el-card class="box-card" style="width: 400px; margin: auto;">
      <!-- 使用具名插槽 #header -->
      <template #header>
        <h3 class="card-header">用户登录页面</h3>
      </template>
      <!-- 移除 .native 修饰符，并使用 @submit.prevent -->
      <el-form :model="form" @submit.prevent="onSubmit">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="Enter username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="form.password"
            placeholder="Enter password"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit" block>登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  name: 'LoginXxcc',
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    async onSubmit() {
      if (!this.form.username || !this.form.password) {
        ElMessage.error('Please fill in all fields.');
        return;
      }
      try {
        // 使用完整的 URL 进行请求
        const response = await axios.post('http://localhost:5000/api/login', this.form, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        localStorage.setItem('token', response.data.access_token);
        this.$router.push('/main');
        ElMessage.success('Login successful!');
      } catch (error) {
        ElMessage.error('Login failed. Please check your username and password.');
      }
    },
  },
};
</script>

<style>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
}
</style>